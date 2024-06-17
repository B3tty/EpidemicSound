import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.fixture(scope="module")
def test_db():
    from sqlalchemy.orm import sessionmaker
    from app.database import Base, engine

    testing_session_local = sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_session_local()
    yield db
    db.close()


@pytest.fixture
def client(test_db):
    return TestClient(app)


def test_create_playlist_one_valid_playlist(client: TestClient, test_db:
Session):
    playlist_data = {
        "data":
            [
                {
                    "title": "New playlist",
                    "sounds": ["f91a7e06-85fa-41ae-813a-62c4fff1f67b"]
                }
            ]
    }

    response = client.post("/playlists", json=playlist_data)
    assert response.status_code == 201

    created_playlists = response.json()["data"]
    assert isinstance(created_playlists, list)
    assert len(created_playlists) == 1

    playlist = created_playlists[0]
    assert playlist["title"] == "New playlist"


def test_create_playlist_multiple_valid_playlists(client: TestClient, test_db:
Session):
    playlist_data = {
        "data":
            [
                {
                    "title": "New playlist",
                    "sounds": ["f91a7e06-85fa-41ae-813a-62c4fff1f67b"]
                },
                {
                    "title": "Another playlist",
                    "sounds": ["f91a7e06-85fa-41ae-813a-62c4fff1f67b",
                               "20b0f4ee-bad2-479d-a0c9-020abf17ff55"]
                }
            ]
    }

    response = client.post("/playlists", json=playlist_data)
    assert response.status_code == 201

    created_playlists = response.json()["data"]
    assert isinstance(created_playlists, list)
    assert len(created_playlists) == 2


def test_create_playlist_invalid_playlist(client: TestClient, test_db: Session):
    playlist_data = {
        "data":
            {
                "title": "New playlist",
                "sounds": ["f91a7e06-85fa-41ae-813a-62c4fff1f67b"]
            }

    }
    response = client.post("/playlists", json=playlist_data)
    assert response.status_code == 422
