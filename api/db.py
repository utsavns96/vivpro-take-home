import sqlite3
import logging
import os

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     handlers=[logging.FileHandler('logs/db.log'),
#                               logging.StreamHandler()])

# Configure named logger
logger = logging.getLogger("db_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/db.log')
stream_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

DB_PATH = 'data/playlist.db'

def get_connection():
    # Establish a connection to the SQLite database
    logger.info("Establishing database connection")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    logger.info("Database connection established")
    return conn

def fetch_all_songs():
    # Fetch all songs from the database
    logger.info("Fetching all songs from the database")
    with get_connection() as conn:
        return conn.execute("SELECT * FROM songs").fetchall()

def fetch_song_by_id(song_id):
    # Fetch a single song by its ID
    logger.info(f"Fetching song with ID {song_id}")
    with get_connection() as conn:
        return conn.execute("SELECT * FROM songs WHERE id = ?", (song_id,)).fetchone()


def update_rating(song_id, rating):
    # Update the rating of a song by its ID
    logger.info(f"Updating rating for song ID {song_id} to {rating}")
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE songs SET rating = ? WHERE id = ?", (rating, song_id)
            )
            conn.commit()
            return cursor.rowcount  # Returns number of rows updated
    except Exception as e:
        logger.error(f"Failed to update rating: {e}")
        raise
