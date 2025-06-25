import sqlite3
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logs/db.log'),
                              logging.StreamHandler()])

DB_PATH = 'data/playlist.db'

def get_connection():
    # Establish a connection to the SQLite database
    logging.info("Establishing database connection")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    logging.info("Database connection established")
    return conn

def fetch_all_songs():
    # Fetch all songs from the database
    logging.info("Fetching all songs from the database")
    with get_connection() as conn:
        return conn.execute("SELECT * FROM songs").fetchall()

def fetch_song_by_id(song_id):
    # Fetch a single song by its ID
    logging.info(f"Fetching song with ID {song_id}")
    with get_connection() as conn:
        return conn.execute("SELECT * FROM songs WHERE id = ?", (song_id,)).fetchone()

def filter_songs(class_=None, rating=None):
    query = "SELECT * FROM songs WHERE 1=1"
    params = []

    if class_:
        query += " AND class = ?"
        params.append(class_)
    if rating:
        query += " AND rating >= ?"
        params.append(float(rating))

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()

def update_rating(song_id, rating):
    # Update the rating of a song by its ID
    logging.info(f"Updating rating for song ID {song_id} to {rating}")
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE songs SET rating = ? WHERE id = ?", (rating, song_id)
            )
            conn.commit()
            return cursor.rowcount  # Returns number of rows updated
    except Exception as e:
        logging.error(f"Failed to update rating: {e}")
        raise
