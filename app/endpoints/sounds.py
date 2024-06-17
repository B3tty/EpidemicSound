from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import SessionLocal
from app.schemas import ManySoundResponse, ManySoundRecommendation

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sounds/", response_model=ManySoundResponse)
def get_sounds(db: Session = Depends(get_db)):
    sounds = crud.get_sounds(db=db)
    if sounds is None:
        raise HTTPException(status_code=404, detail="No sounds found")
    return {"data": sounds}


@router.get("/sounds/recommended",
            response_model=ManySoundRecommendation)
def get_recommended_sound(playlistId: str, limit: int = 5, db: Session = (
    Depends(get_db))):
    try:
        sounds = crud.get_recommendations_by_playlist(db=db,
                                                      playlist_id=playlistId,
                                                      limit=limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.__str__())
    if len(sounds) == 0:
        raise HTTPException(status_code=404, detail="No sounds available")
    return {"data": sounds}
