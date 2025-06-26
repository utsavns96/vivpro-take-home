import pytest
from api import app
from unittest.mock import patch

@pytest.fixture
#Flask test client
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ----------------------------
# 1. Test GET /songs
# ----------------------------
@patch('api.fetch_all_songs') # Mocking the fetch_all_songs function
def test_get_all_songs(mock_fetch_all, client):
    # Simulating data returned from database
    mock_fetch_all.return_value = [
        {"id": "001", "title": "Test Song", "rating": 4.0}
    ]
    # Making a GET request to the /songs endpoint
    response = client.get('/songs?page=1&limit=10')
    # Checking if the response is successful and contains the expected data structure
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    # Checking if the data is a list and contains the expected song
    assert isinstance(data["data"], list)
    assert data["data"][0]["title"] == "Test Song"
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 1

# ------------------------------------
# 2. Test GET /songs/<song_id> success
# ------------------------------------
@patch('api.fetch_song_by_id') # Mocking the fetch_song_by_id function
def test_get_song_by_id_found(mock_fetch, client):
    # Simulating data returned from database
    mock_fetch.return_value = {"id": "001", "title": "Test Song", "rating": 4.0}
    # Making a GET request to the /songs/<song_id> endpoint
    response = client.get('/songs/001')
    # Checking if the response is successful and contains the expected song data
    assert response.status_code == 200
    assert response.json['title'] == "Test Song"

# ------------------------------------
# 3. Test GET /songs/<song_id> failure
# ------------------------------------
@patch('api.fetch_song_by_id') # Mocking the fetch_song_by_id function
# Test for song not found
def test_get_song_by_id_not_found(mock_fetch, client):
    mock_fetch.return_value = None # Simulating a song that does not exist
    response = client.get('/songs/999')
    # Checking if the response indicates that the song was not found
    assert response.status_code == 404
    assert "error" in response.json

# ------------------------------------------
# 4. Test POST /songs/<song_id>/rate success
# ------------------------------------------
# Mocking the update_rating function to simulate database interaction
@patch('api.update_rating')
def test_rate_song_success(mock_update, client):
    # Simulating a successful rating update
    mock_update.return_value = 1
    # Making a POST request to the /songs/<song_id>/rate endpoint with a valid rating
    response = client.post('/songs/001/rate', json={"rating": 4.5})
    # Checking if the response indicates success
    assert response.status_code == 200
    assert "message" in response.json

# --------------------------------------------------
# 5. Test POST /songs/<song_id>/rate missing rating
# --------------------------------------------------
# Mocking the update_rating function to simulate database interaction
@patch('api.update_rating')
def test_rate_song_missing_rating(mock_update, client):
    response = client.post('/songs/001/rate', json={})
    assert response.status_code == 400
    assert "error" in response.json


# --------------------------------------------------
# 6. Test POST /songs/<song_id>/rate invalid rating
# --------------------------------------------------
@patch('api.update_rating')
def test_rate_song_invalid_rating(mock_update, client):
    response = client.post('/songs/001/rate', json={"rating": 7.5})
    assert response.status_code == 400
    assert "error" in response.json


# --------------------------------------------------
# 7. Test POST /songs/<song_id>/rate song not found
# --------------------------------------------------
@patch('api.update_rating')
def test_rate_song_not_found(mock_update, client):
    mock_update.return_value = 0
    response = client.post('/songs/001/rate', json={"rating": 3.5})
    assert response.status_code == 404
    assert "error" in response.json


# ------------------------------------------------------
# 8. Test POST /songs/<song_id>/rate data is not a json
# ------------------------------------------------------
def test_rate_song_non_json(client):
    response = client.post('/songs/001/rate', data="not-json")
    assert response.status_code == 400
    assert "error" in response.json
