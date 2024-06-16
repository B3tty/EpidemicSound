import random

from sqlalchemy.orm import Session

from app import models, schemas
from app.models import playlist_sounds


def create_sound(db: Session, sound: schemas.SoundCreate):
    db_sound = models.Sound(
        title=sound.title,
        bpm=sound.bpm,
        genres=",".join(sound.genres),
        duration_in_seconds=sound.duration_in_seconds
    )
    db.add(db_sound)
    db.commit()
    db.refresh(db_sound)

    for credit in sound.credits:
        db_credit = models.Credit(
            name=credit.name,
            role=credit.role,
            sound_id=db_sound.id
        )
        db.add(db_credit)

    db.commit()
    return db_sound


def get_sounds(db: Session):
    sounds = db.query(models.Sound).all()
    for sound in sounds:
        sound.genres = sound.genres_list
    return sounds


def create_playlist(db: Session, playlist: schemas.PlaylistCreate):
    db_playlist = models.Playlist(title=playlist.title)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    for sound_id in playlist.sounds:
        db.execute(playlist_sounds.insert().values(playlist_id=db_playlist.id,
                                                   sound_id=sound_id))

    db.commit()
    db.refresh(db_playlist)
    db_playlist = db.query(models.Playlist).filter(models.Playlist.id == db_playlist.id).first()

    return db_playlist


def get_random_sound(db: Session):
    sounds = db.query(models.Sound).all()
    if sounds:
        sound = random.choice(sounds)
        sound.genres = sound.genres_list
        return sound
    return None
