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


def test_create_sound_one_valid_sound(client: TestClient, test_db: Session):
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

    response = client.post("/admin/sounds", json=sound_data)
    assert response.status_code == 201

    created_sound = response.json()["data"][0]
    assert created_sound["title"] == "New song"
    assert created_sound["bpm"] == 120
    assert created_sound["genres"] == ["pop"]
    assert created_sound["duration_in_seconds"] == 130
    assert len(created_sound["credits"]) == 2
    assert created_sound["credits"][0]["name"] == "King Sis"
    assert created_sound["credits"][0]["role"] == "VOCALIST"
    assert created_sound["credits"][1]["name"] == "Ooyy"
    assert created_sound["credits"][1]["role"] == "PRODUCER"


def test_create_sound_multiple_valid_sounds(client: TestClient, test_db:
Session):
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
            },
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

    response = client.post("/admin/sounds", json=sound_data)
    assert response.status_code == 201

    created_sounds = response.json()["data"]
    assert isinstance(created_sounds, list)
    assert len(created_sounds) == 2


def test_create_sound_invalid_input(client: TestClient, test_db: Session):
    sound_data = {
        "data":
            {
                "bpm": 120,
                "genres": ["pop"],
                "duration_in_seconds": 130,
                "credits": [
                    {"name": "King Sis", "role": "VOCALIST"},
                    {"name": "Ooyy", "role": "PRODUCER"}
                ]
            }

    }
    response = client.post("/admin/sounds", json=sound_data)
    assert response.status_code == 422
