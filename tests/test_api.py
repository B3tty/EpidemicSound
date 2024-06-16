from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_create_sound():
    response = client.post(
        "/admin/sounds/",
        json={
            "data": [
                {
                    "title": "New song 2",
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
    )
    assert response.status_code == 200
    assert response.json()[0]["title"] == "New song 2"
    assert response.json()[0]["genres"] == ["pop"]


def test_create_playlist():
    response = client.post(
        "/playlists/",
        json={
            "data": [
                {
                    "title": "New playlist 1",
                    "sounds": ["1", "2", "3"]
                },
                {
                    "title": "New playlist 2",
                    "sounds": ["4", "5", "6"]
                }
            ]
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 2  # Ensure two playlists were created
    assert all("id" in playlist for playlist in
               response.json())  # Check if each playlist has an 'id'
    assert response.json()[0]["title"] == "New playlist 1"
    assert response.json()[1]["title"] == "New playlist 2"


def test_get_recommended_sound():
    response = client.get("/sounds/recommended")
    assert response.status_code == 200


def test_get_sounds():
    response = client.get("/sounds")
    assert response.status_code == 200
