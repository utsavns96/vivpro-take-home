import json
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logs/dataParsing.log'),
                              logging.StreamHandler()])

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

    class Config:
        populate_by_name  = True

def load_data(file_path):
    logging.info(f"Loading data from {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded {len(data)} records")
    return pd.DataFrame.from_dict(data)

def validate_songs(df):
    logging.info("Validating data from JSON")
    valid_rows=[]
    for i, row in df.iterrows():
        try:
            song = Song(**row.to_dict())
            valid_rows.append(song)
        except ValidationError as e:
            logging.error(f"Validation error in Row {i}: {e}")
    logging.info(f"{len(valid_rows)} valid rows out of {len(df)}")
    return valid_rows

def load_config(path='config.json'):
    try:
        with open(path, 'r') as file:
            config = json.load(file)
        logging.info(f"Loaded config from {path}")
        return config
    except Exception as e:
        logging.error(f"Error loading config from {path}: {e}")
        return {}

if __name__ == "__main__":
    #get configuration settings
    config = load_config('config.json')
    #get input and output paths from config or use defaults
    input_path = config.get("input_path", 'data/playlist.json')
    output_path = config.get("output_path", 'data/playlist.csv')
    logging.info("Starting data ingestion and validation process")
    # Load the data from the JSON file
    df = load_data(input_path)
    # Validate the songs in the DataFrame
    validated_df = validate_songs(df)
    # print(validated_df.head(10))
    validated_df = pd.DataFrame([song.model_dump(by_alias=True) for song in validated_df])
    validated_df.to_csv(output_path, index=False)
    logging.info(f"Saved validated data to {output_path}")