import random
import uuid

from sqlalchemy.orm import Session

from app import models, schemas


def create_sound(db: Session, sound: schemas.SoundCreate):
    db_sound = models.Sound(
        id=str(uuid.uuid4()).replace("-", ""),
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
            id=str(uuid.uuid4()).replace("-", ""),
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
    db_playlist = models.Playlist(id=str(uuid.uuid4()).replace("-", ""),
                                  title=playlist.title)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    if playlist.sounds:
        sound_objects = db.query(models.Sound).filter(models.Sound.id.in_(
            [str(sound_id).replace("-", "") for sound_id in
             playlist.sounds])).all()
        db_playlist.sounds = sound_objects
        db.commit()
        db.refresh(db_playlist)

    return db_playlist


def get_random_sound(db: Session):
    sounds = db.query(models.Sound).all()
    if sounds:
        sound = random.choice(sounds)
        sound.genres = sound.genres_list
        return sound
    return None
