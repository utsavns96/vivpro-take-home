import json
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import logging
import sqlite3
import os

'''
Data ingestion and validation pipeline for music playlist data.
This script reads a JSON file containing music playlist data, validates each entry against a predefined schema using Pydantic,
and saves the validated data to a SQLite database. It also logs the process, including any validation errors encountered.
This script is designed to be run as a standalone module, and it expects a configuration file named 'config.json' to specify input and output paths.
It uses Pydantic for data validation, Pandas for data manipulation, and logging for tracking the process.
'''

'''
The comments are in greater detail to explain each step of the code
'''

# Set up logging
os.makedirs('logs', exist_ok=True)
# Logging is configured to log messages to both a file and the console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logs/dataParsing.log'),
                              logging.StreamHandler()])

# Define the Song model using Pydantic
# This model will be used to validate the data structure of each song entry
class Song(BaseModel):
    id: str
    title: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    num_bars: int
    num_sections: int
    num_segments: int
    class_: int = Field(alias='class')
    rating: Optional[float] = None

    model_config = {
        "populate_by_name": True
    }


# Function to load data from a JSON file into a Pandas DataFrame
# It reads the JSON file, converts it to a DataFrame, and logs the number of records loaded
# If the file does not exist or is empty, it will log an error
def load_data(file_path):
    logging.info(f"Loading data from {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded {len(data)} records")
    return pd.DataFrame.from_dict(data)

# Function to validate each song in the DataFrame against the Song model
# It iterates through each row, attempts to create a Song instance, and logs any validation errors
# Valid songs are collected in a list and returned as a list of Song instances
def validate_songs(df):
    #start_time=time.perf_counter()
    logging.info("Validating data from JSON")
    valid_rows=[] #dict to store valid rows
    # Iterate through each row in the DataFrame
    # Not using iterrows() for better performance (theoretically), instead using a range loop 
    # Did not see significant performance difference in practice for this dataset size - 0.00585960 vs 0.00576640
    for index in range(len(df)):
        try:
            song = Song(**df.iloc[index].to_dict())  # Convert row to dict, unpack and validate against Song model
            valid_rows.append(song)  # Add to valid rows if validated
        except ValidationError as e:
            logging.error(f"Validation error in Row {index}: {e}")
    # Log the number of valid rows found
    logging.info(f"{len(valid_rows)} valid rows out of {len(df)}")
    #end_time=time.perf_counter()
    #logging.info(f"Validation completed in {end_time-start_time:.8f} seconds")
    return valid_rows


# Function to save the validated DataFrame to a SQLite database
# It connects to the database, saves the DataFrame as a table named 'songs', and logs the process
# If the database file does not exist, it will be created
def save_to_db(df, db_path='data/playlist.db'):
    logging.info(f"Saving data to database at {db_path}")
    conn = sqlite3.connect(db_path)
    df.to_sql('songs', conn, if_exists='replace', index=False) #(table name, connection object, if_exists='replace' to overwrite existing table, index=false to drop index)
    conn.close()
    logging.info("Data saved to database successfully")

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

# Main function to execute the data ingestion and validation process
if __name__ == "__main__":
    #get configuration settings
    config = load_config('config.json')
    #get input and output paths from config or use defaults
    input_path = config.get("input_path", 'data/playlist.json')
    db_path=config.get("db_path", 'data/playlist.db')
    #output_path = config.get("output_path", 'data/playlist.csv')
    logging.info("Starting data ingestion and validation process")
    # Load the data from the JSON file
    df = load_data(input_path)
    # Ensure the column names are stripped of whitespace and converted to lowercase
    df.columns = df.columns.str.strip().str.lower()
    # Validate the songs in the DataFrame
    validated_df = validate_songs(df)
    # print(validated_df.head(10))
    validated_df = pd.DataFrame([song.model_dump(by_alias=True) for song in validated_df])
    validated_df["rating"] = None
    #validated_df.to_csv(output_path, index=False)
    save_to_db(validated_df, db_path)
    logging.info(f"Saved validated data to database at {db_path}")
    #logging.info(f"Saved validated data to {output_path}")