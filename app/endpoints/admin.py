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


@router.post("/sounds/", response_model=ManySoundResponse, status_code=201)
def create_sound(batch_sound_create: ManySoundCreate, db: Session = Depends(get_db)):
    if not isinstance(batch_sound_create.data, list):
        raise HTTPException(status_code=422,
                            detail="Invalid input: 'data' should be a list")

    created_db_sounds = crud.create_sounds(db=db, sounds=batch_sound_create.data)
    for created_sound in created_db_sounds:
        created_sound.genres = created_sound.genres_list

    return {"data": created_db_sounds}
