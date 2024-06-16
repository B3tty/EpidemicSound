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


@router.post("/playlists/", response_model=List[schemas.Playlist])
def create_playlist(request_body: dict, db: Session = Depends(get_db)):
    playlists_data = request_body.get("data")
    if not isinstance(playlists_data, list):
        raise HTTPException(status_code=422,
                            detail="Invalid input: 'data' should be a list")

    created_playlists = []
    for playlist_data in playlists_data:
        playlist = schemas.PlaylistCreate(title=playlist_data.get("title"),
                                          sounds=playlist_data.get("sounds"))
        db_playlist = crud.create_playlist(db=db, playlist=playlist)

        playlist_response = schemas.Playlist(
            id=db_playlist.id,
            title=db_playlist.title,
            sounds=[sound.id for sound in db_playlist.sounds]
        )
        created_playlists.append(playlist_response)

    return created_playlists
