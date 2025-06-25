from flask import Flask, jsonify, request
from db import fetch_all_songs, fetch_song_by_id, update_rating
import logging
import os

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     handlers=[logging.FileHandler('logs/api.log'),
#                               logging.StreamHandler()])

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure named logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/api.log')
stream_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

app = Flask(__name__)


# Fetch all songs from the database
@app.route('/songs', methods=['GET'])
def get_all():
    logger.info("API call: GET /songs")

    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    if page < 1 or limit < 1:
        logger.warning("Invalid pagination parameters")
        return jsonify({"error": "Page and limit must be positive integers"}), 400
    logger.info(f"Pagination parameters: page={page}, limit={limit}")
    all_songs = [dict(row) for row in fetch_all_songs()]
    start = (page - 1) * limit
    end = start + limit
    paginated = all_songs[start:end]
    return jsonify(
        {"page": page, "limit": limit, "total": len(all_songs), "data": paginated}
    )


# Fetch a song by its ID
@app.route('/songs/<string:song_id>', methods=['GET'])
def get_by_id(song_id):
    logger.info(f"API call: GET /songs/{song_id}")
    song = fetch_song_by_id(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404 # Return 404 if song not found
    return jsonify(dict(song))


# Update the rating of a song
@app.route('/songs/<song_id>/rate', methods=['POST'])
def rate_song(song_id):
    logger.info(f"API call: POST /songs/{song_id}/rate")
    #Error handling for JSON content-type
    if not request.is_json:
        logger.warning("Request content-type not JSON")
        return jsonify({"error": "Request must be JSON"}), 400 # Return 400 if content-type is not JSON
    # Extracting the rating from the request body
    data = request.get_json()
    rating = data.get("rating")
    
    # Error handling for missing or invalid rating
    if rating is None:
        logger.warning("Missing 'rating' in request JSON")
        return jsonify({"error": "Missing 'rating' in request body"}), 400 # Return 400 if rating is missing
    
    # Error handling for invalid rating datatype
    if not isinstance(rating, (int, float)):
        logger.warning(f"Invalid rating type: {type(rating)}")
        return jsonify({"error": "Rating must be a number"}), 400 # Return 400 if rating is not a number

    try:
        rating = float(rating)
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
    except ValueError as e:
        logger.warning(f"Invalid rating value: {rating}")
        return jsonify({"error": str(e)}), 400 # Return 400 if rating is invalid

    # Update the rating in the database
    updated = update_rating(song_id, rating)
    if updated == 0:
        logger.warning(f"No song found with ID {song_id}")
        return jsonify({"error": "Song not found"}), 404 # Return 404 if song not found

    logger.info(f"Rating updated successfully for song ID {song_id}")
    return jsonify({"message": "Rating updated successfully"}), 200 # Return 200 if rating updated successfully


if __name__ == '__main__':
    app.run(debug=True)
