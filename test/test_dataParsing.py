import pytest
from dataParsing import Song, load_config, load_data, validate_songs
import pandas as pd
from pydantic import ValidationError
import json
import logging

# Set up logging for testing
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


# ----------------------
# 1. Test Data Loading
# ----------------------
def test_load_data(tmp_path):
    # Create a temporary JSON with valid data for testing
    test_data = {
        "id": {"0": "001"},
        "title": {"0": "Valid Song"},
        "danceability": {"0": 0.7},
        "energy": {"0": 0.8},
        "key": {"0": 5},
        "loudness": {"0": -5.2},
        "mode": {"0": 1},
        "acousticness": {"0": 0.2},
        "instrumentalness": {"0": 0.1},
        "liveness": {"0": 0.15},
        "valence": {"0": 0.6},
        "tempo": {"0": 120.0},
        "duration_ms": {"0": 210000},
        "time_signature": {"0": 4},
        "num_bars": {"0": 80},
        "num_sections": {"0": 10},
        "num_segments": {"0": 240},
        "class": {"0": 1},
        "rating": {"0": 4.5}
    }
    # Create a temporary file to store the test data
    test_file = tmp_path / "test_data.json"
    # Write the test data to the file
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Test loading a valid JSON file
    df = load_data(test_file)
    # Check if the DataFrame is created correctly
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'id' in df.columns

    # Test loading a non-existent file
    with pytest.raises(FileNotFoundError):
        load_data('non_existent_file.json')


# -----------------------------
# 2. Test Config Loader
# -----------------------------
def test_load_config(tmp_path):
    # Create a temporary JSON config file
    config_content = {
        "input_path": "data/sample.json",
        "output_path": "data/output.csv",
        "db_path": "data/test.db"
    }
    # Write the config content to a temporary file
    config_path = tmp_path / "test_config.json"
    with open(config_path, "w") as f:
        json.dump(config_content, f)
    # Load the config using the load_config function
    config = load_config(config_path)
    # Check if the config is loaded correctly
    assert config["input_path"] == "data/sample.json"
    assert config["db_path"] == "data/test.db"


# -----------------------------
# 3. Test Data Validation
# -----------------------------

def test_validate_songs_valid():
    # Create valid song data
    data = {
        "id": ["001"],
        "title": ["Valid Song"],
        "danceability": [0.7],
        "energy": [0.8],
        "key": [5],
        "loudness": [-5.2],
        "mode": [1],
        "acousticness": [0.2],
        "instrumentalness": [0.1],
        "liveness": [0.15],
        "valence": [0.6],
        "tempo": [120.0],
        "duration_ms": [210000],
        "time_signature": [4],
        "num_bars": [80],
        "num_sections": [10],
        "num_segments": [240],
        "class": [1],
    }
    # Convert the data to a DataFrame and validate
    df = pd.DataFrame(data)
    # Validate the songs using the validate_songs function
    validated = validate_songs(df)
    # Check if the validation returns the correct number of valid songs
    assert len(validated) == 1
    assert validated[0].title == "Valid Song"

# -----------------------------
# 4. Test Data Validation with Invalid Data
# -----------------------------
def test_validate_songs_invalid():
    # Create invalid song data
    data = {
        "id": ["002"],
        # title is missing
        "danceability": [1.5],  # Invalid value
        "energy": [0.8],
        "key": [5],
        "loudness": [-5.2],
        "mode": [1],
        "acousticness": [0.2],
        "instrumentalness": [0.1],
        "liveness": [0.15],
        "valence": [0.6],
        "tempo": [120.0],
        "duration_ms": [210000],
        "time_signature": [4],
        "num_bars": [80],
        "num_sections": [10],
        "num_segments": [240],
        "class": [1]
    }
    # Convert the data to a DataFrame and validate
    df = pd.DataFrame(data)
    validated = validate_songs(df)
    # Check if the validation catches the error and returns no valid songs
    assert len(validated) == 0