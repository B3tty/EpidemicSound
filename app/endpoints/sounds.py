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


@router.get("/sounds/", response_model=List[schemas.Sound])
def get_sounds(db: Session = Depends(get_db)):
    sounds = crud.get_sounds(db=db)
    if sounds is None:
        raise HTTPException(status_code=404, detail="No sounds found")
    return sounds


@router.get("/sounds/recommended", response_model=schemas.Sound)
def get_recommended_sound(db: Session = Depends(get_db)):
    sound = crud.get_random_sound(db=db)
    if not sound:
        raise HTTPException(status_code=404, detail="No sounds available")
    return sound
