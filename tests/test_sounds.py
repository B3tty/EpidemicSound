from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_sounds():
    response = client.get("/sounds")
    assert response.status_code == 200

    sounds = response.json()["data"]

    assert isinstance(sounds, list)
    for sound in sounds:
        assert "id" in sound
        assert "title" in sound
        assert "bpm" in sound
        assert "genres" in sound
        assert "duration_in_seconds" in sound
        assert "credits" in sound


def test_get_recommended_sound():
    playlist_id = "1d007db5-743c-48e8-a6e7-35c276b69c8c"
    response = client.get(f"/sounds/recommended?playlist_id={playlist_id}")
    assert response.status_code == 200
    recommended_sounds = response.json()["data"]

    assert isinstance(recommended_sounds, list)
    for sound in recommended_sounds:
        assert "id" in sound
        assert "title" in sound
        assert "bpm" in sound
        assert "genres" in sound
        assert "duration_in_seconds" in sound
        assert "credits" in sound
