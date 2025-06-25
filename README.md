# vivpro-take-home
This repository contains my solution for Vivpro's Backend Take Home assignment

---

## Overview:
This project aims to:
1. Normalize a nested JSON dataset of songs into a clean, tabular format.
2. Store this data in a sqlite database for use in a backend API.
3. Provide API endpoints to:
   - Retrieve all songs with pagination.
   - Look up a song by title.
   - Add rating to a song

---

## Setup:
I like to use Chocolatey since I'm on a Windows machine. The steps to install chocolatey can be found [here](https://chocolatey.org/install).
1. In an elevated terminal, run the command `choco install python` (installs latest available package - use `choco install python --versionx.xx.x` if you need a specific version). It will ask if you want to run the script - enter `Y` to proceed.
2. After the installation is complete, run `python --version` to verify that it has been installed correctly.
3. Now, install the following packages for this project:
    
    i. pandas: `pip install pandas` <br>
    ii. pydantic: `pip install pydantic` <br>
    iii. flask: `pip install flask`

The environment should now be set up.

## Technical Description:

The project is split into 2 parts: The data ingestion and the API backend, to decouple the steps for better flexibility.

### 1. dataParsing.py

This module is responsible for the ingestion, validation and persistence of the music playlist data. The input is a raw JSON file in a columnised format, and the data is stored in a persistent SQLite database after processing. It uses standard python librarires, along with pydantic for validation, pandas for easily handling the data and sqlite3 for the database, creating a robust ETL process.

It works as follows:
1. Read the input JSON file specified in config.json
2. Validate each row of the dataset using a pydantic modfel.
    - A `Song` model is defined using the Pydantic library.
    - Each row of the data must conform to the expected datatypes. If any field is missing or invalid, the row is skipped and an error is logged. 
3. Convert valid entries into a pandas DataFrame.
4. Save the cleaned and structured data into a SQLite database specified in config.json, for persistence.

Additionally, Logging is implemented at console level and to a file in the `/logs` directory. Each step of the process is logged, from function invocations to validation errors with a specific row of data. The code uses a config file instead of hardcoded variables, to ensure ease of managing envrionment variables. The `ratings` field is 'Optional' in the Pydantic model, so that songs can be validated even if they don't have ratings, and it can be added later through the API or an updated JSON. One issue I had to work around is that the reserved keyword `class` was also a field name, necessitating the use of an alias `class_`.

The operations are split into 3 separate functions - `load_data`, `validate_songs` and `save_to_db` for readability, maintainability and easier testing.


Output Files
- Validated and clean song data is saved to:<br>
    SQLite DB: data/playlist.db (table: songs)
- Logs are written to:<br>
    Log file: logs/dataParsing.log