from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

random_uuid = "1d007db5-743c-48e8-a6e7-35c276b69c8c"


def insert_sound():
    sound_data = {
        "data": [
            {
                "title": "New song",
                "bpm": 120,
                "genres": ["pop"],
                "duration_in_seconds": 130,
                "credits": [
                    {"name": "King Sis", "role": "VOCALIST"},
                    {"name": "Ooyy", "role": "PRODUCER"}
                ]
            }
        ]
    }
    return client.post("/admin/sounds", json=sound_data).json()[
        "data"][0]


def insert_playlist(sound_id: str):
    playlist_data = {
        "data":
            [
                {
                    "title": "New playlist",
                    "sounds": [f"{sound_id}"]
                }
            ]
    }
    return client.post("/playlists", json=playlist_data).json()[
        "data"][0]


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


def test_get_recommended_sounds_non_existing_playlist():
    response = client.get(f"/sounds/recommended?playlistId={random_uuid}")
    assert response.status_code == 404
    assert response.text.__contains__(f"Playlist {random_uuid} not found")


def test_get_recommended_sounds_no_match():
    created_playlist = insert_playlist(random_uuid)
    response = client.get(f"/sounds/recommended?playlistId="
                          f"{created_playlist["id"]}")
    assert response.status_code == 404
    assert response.text.__contains__("No sounds available")


def test_get_recommended_sounds_existing_playlist():
    created_sound = insert_sound()
    created_playlist = insert_playlist(created_sound["id"])
    insert_sound()
    response = client.get(f"/sounds/recommended?playlistId="
                          f"{created_playlist["id"]}")
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
