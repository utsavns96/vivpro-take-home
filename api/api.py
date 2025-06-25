from flask import Flask, jsonify, request
from db import fetch_all_songs, fetch_song_by_id, filter_songs
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logs/api.log'),
                              logging.StreamHandler()])
app = Flask(__name__)

@app.route('/songs')
def get_all():
    logging.info("API call: GET /songs")
    return jsonify([dict(row) for row in fetch_all_songs()])

@app.route('/songs/<string:song_id>')
def get_by_id(song_id):
    logging.info(f"API call: GET /songs/{song_id}")
    song = fetch_song_by_id(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(dict(song))

@app.route('/songs/filter')
def get_filtered():
    logging.info("API call: GET /songs/filter")
    return jsonify([dict(row) for row in filter_songs(
        class_=request.args.get("class"),
        rating=request.args.get("rating")
    )])

from flask import Flask, request, jsonify
from db import fetch_song_by_id, fetch_all_songs, filter_songs, update_rating
# logging setup already present

@app.route('/songs/<song_id>/rate', methods=['POST'])
def rate_song(song_id):
    logging.info(f"API call: POST /songs/{song_id}/rate")
    
    if not request.is_json:
        logging.warning("Request content-type not JSON")
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    rating = data.get("rating")
    
    if rating is None:
        logging.warning("Missing 'rating' in request JSON")
        return jsonify({"error": "Missing 'rating' in request body"}), 400

    try:
        rating = float(rating)
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
    except ValueError as e:
        logging.warning(f"Invalid rating value: {rating}")
        return jsonify({"error": str(e)}), 400

    updated = update_rating(song_id, rating)
    if updated == 0:
        logging.warning(f"No song found with ID {song_id}")
        return jsonify({"error": "Song not found"}), 404

    logging.info(f"Rating updated successfully for song ID {song_id}")
    return jsonify({"message": "Rating updated successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
