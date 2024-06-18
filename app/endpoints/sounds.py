from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import ManySoundResponse, ManySoundRecommendation, \
    GlobalSoundStatistics, PlaylistSoundStatistics

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
    except LookupError as e:
        raise HTTPException(status_code=404, detail=e.__str__())
    if len(sounds) == 0:
        raise HTTPException(status_code=404, detail="No sounds available")
    return {"data": sounds}


@router.get("/sounds/statistics/global",
            response_model=GlobalSoundStatistics)
def get_recommended_sound(db: Session = (
    Depends(get_db))):
    stats = crud.get_global_statistics(db=db)
    return stats


@router.get("/sounds/statistics",
            response_model=PlaylistSoundStatistics)
def get_recommended_sound(playlistId: str, db: Session = (
    Depends(get_db))):
    try:
        stats = crud.get_statistics_for_playlist(db=db,
                                                 playlist_id=playlistId)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=e.__str__())
    return stats
