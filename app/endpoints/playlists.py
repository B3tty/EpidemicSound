from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from app.schemas import ManyPlaylistResponse, ManyPlaylistCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/playlists/", response_model=ManyPlaylistResponse, status_code=201)
def create_playlist(batch_playlist_create: ManyPlaylistCreate, db: Session =Depends(get_db)):
    if not isinstance(batch_playlist_create.data, list):
        raise HTTPException(status_code=422,
                            detail="Invalid input: 'data' should be a list")

    playlist_responses = []
    for playlist_create in batch_playlist_create.data:
        playlist = schemas.PlaylistCreate(title=playlist_create.title,
                                          sounds=playlist_create.sounds)
        created_playlist = crud.create_playlist(db=db, playlist=playlist)

        playlist_response = schemas.Playlist(
            id=created_playlist.id,
            title=created_playlist.title,
            sounds=[sound.id for sound in created_playlist.sounds]
        )
        playlist_responses.append(playlist_response)

    return {"data": playlist_responses}
