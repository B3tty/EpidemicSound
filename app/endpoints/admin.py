from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sounds/", response_model=List[schemas.Sound])
def create_sound(request_body: dict, db: Session = Depends(get_db)):
    sounds_data = request_body.get("data")
    if not isinstance(sounds_data, list):
        raise HTTPException(status_code=422,
                            detail="Invalid input: 'data' should be a list")

    created_sounds = []
    for sound_data in sounds_data:
        sound = schemas.SoundCreate(**sound_data)
        created_sound = crud.create_sound(db=db, sound=sound)
        created_sound.genres = created_sound.genres_list
        created_sounds.append(created_sound)

    return created_sounds
