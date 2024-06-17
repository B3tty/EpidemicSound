from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import SessionLocal

from app.schemas import ManySoundResponse, ManySoundCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sounds/", response_model=ManySoundResponse)
def create_sound(batch_sound_create: ManySoundCreate, db: Session = Depends(get_db)):
    if not isinstance(batch_sound_create.data, list):
        raise HTTPException(status_code=422,
                            detail="Invalid input: 'data' should be a list")

    created_sounds = []
    for sound_create in batch_sound_create.data:
        created_sound = crud.create_sound(db=db, sound=sound_create)
        created_sound.genres = created_sound.genres_list
        created_sounds.append(created_sound)

    return {"data": created_sounds}
