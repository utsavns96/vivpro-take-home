import pytest
from api import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ----------------------------
# 1. Test GET /songs
# ----------------------------
@patch('api.fetch_all_songs')
def test_get_all_songs(mock_fetch_all, client):
    mock_fetch_all.return_value = [
        {"id": "001", "title": "Test Song", "rating": 4.0}
    ]
    response = client.get('/songs?page=1&limit=10')
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data


    assert isinstance(data["data"], list)
    assert data["data"][0]["title"] == "Test Song"
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 1
# ----------------------------
# 2. Test GET /songs/<song_id>
# ----------------------------
@patch('api.fetch_song_by_id')
def test_get_song_by_id_found(mock_fetch, client):
    mock_fetch.return_value = {"id": "001", "title": "Test Song", "rating": 4.0}
    response = client.get('/songs/001')
    assert response.status_code == 200
    assert response.json['title'] == "Test Song"

@patch('api.fetch_song_by_id')
def test_get_song_by_id_not_found(mock_fetch, client):
    mock_fetch.return_value = None
    response = client.get('/songs/999')
    assert response.status_code == 404
    assert "error" in response.json

# ----------------------------
# 3. Test POST /songs/<song_id>/rate
# ----------------------------
@patch('api.update_rating')
def test_rate_song_success(mock_update, client):
    mock_update.return_value = 1
    response = client.post('/songs/001/rate', json={"rating": 4.5})
    assert response.status_code == 200
    assert "message" in response.json

@patch('api.update_rating')
def test_rate_song_missing_rating(mock_update, client):
    response = client.post('/songs/001/rate', json={})
    assert response.status_code == 400
    assert "error" in response.json

@patch('api.update_rating')
def test_rate_song_invalid_rating(mock_update, client):
    response = client.post('/songs/001/rate', json={"rating": 7.5})
    assert response.status_code == 400
    assert "error" in response.json

@patch('api.update_rating')
def test_rate_song_not_found(mock_update, client):
    mock_update.return_value = 0
    response = client.post('/songs/001/rate', json={"rating": 3.5})
    assert response.status_code == 404
    assert "error" in response.json

def test_rate_song_non_json(client):
    response = client.post('/songs/001/rate', data="not-json")
    assert response.status_code == 400
    assert "error" in response.json
