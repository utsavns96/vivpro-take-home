import json
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

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
    allow_population_by_field_name = True

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame.from_dict(data)

def validate_songs(df):
    valid_rows=[]
    for i, row in df.iterrows():
        try:
            song = Song(**row.to_dict())
            valid_rows.append(song)
        except ValidationError as e:
            print(f"Validation error in Row {i}: {e}")
    return valid_rows


if __name__ == "__main__":
    df = load_data('data/playlist.json')
    # Validate the songs in the DataFrame
    validated_df = validate_songs(df)
    # print(validated_df.head(10))
    validated_df = pd.DataFrame([song.model_dump(by_alias=True) for song in validated_df])
    validated_df.to_csv('data/playlist.csv', index=False)