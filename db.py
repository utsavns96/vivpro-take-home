import sqlite3
import logging
import os
import json
from contextlib import closing

'''
The comments are in greater detail to explain each step of the code
'''

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

#DB_PATH = 'data/playlist.db'

# Function to load configuration settings from a JSON file
# It reads the configuration file and returns the settings as a dictionary
def load_config(path='config.json'):
    try:
        with open(path, 'r') as file:
            config = json.load(file)
        logging.info(f"Loaded config from {path}")
        return config
    except Exception as e:
        logging.error(f"Error loading config from {path}: {e}")
        return {}

# Function to establish a connection to the SQLite database
def get_connection():
    # Load configuration settings
    config=load_config()
    # Establish a connection to the SQLite database
    logger.info("Establishing database connection")
    # Check if the database path is provided in the config, otherwise use default
    conn = sqlite3.connect(config.get('db_path', 'data/playlist.db'))
    conn.row_factory = sqlite3.Row # This allows us to access columns by name
    logger.info("Database connection established")
    return conn

def fetch_all_songs():
    # Fetch all songs from the database
    logger.info("Fetching all songs from the database")
    with closing(get_connection()) as conn:
        # Fetch all is a SELECT * query
        return conn.execute("SELECT * FROM songs").fetchall()

def fetch_song_by_id(song_id):
    # Fetch a single song by its ID
    logger.info(f"Fetching song with ID {song_id}")
    with closing(get_connection()) as conn:
        # Fetching a song by ID is a SELECT query with a WHERE clause
        query = "SELECT * FROM songs WHERE title LIKE ?"
        return conn.execute(query,(f"%{song_id}%",)).fetchall()
        #return conn.execute(, (song_id,)).fetchone()


def update_rating(song_id, rating):
    # Update the rating of a song by its ID
    logger.info(f"Updating rating for song ID {song_id} to {rating}")
    try:
        with closing(get_connection()) as conn:
            # Update rating is an UPDATE query with a WHERE clause
            cursor = conn.execute(
                "UPDATE songs SET rating = ? WHERE id = ?", (rating, song_id)
            )
            conn.commit()
            return cursor.rowcount  # Returns number of rows updated
    except Exception as e:
        logger.error(f"Failed to update rating: {e}")
        raise
