import random
import uuid
from collections import Counter
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.models import Sound
from app.schemas import SoundCreate, PlaylistCreate


def create_sounds(db: Session, sounds: List[SoundCreate]):
    created_db_sounds = []
    for sound in sounds:
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
        created_db_sounds.append(db_sound)

    db.commit()
    return created_db_sounds


def get_sounds(db: Session):
    sounds = db.query(models.Sound).all()
    for sound in sounds:
        sound.genres = sound.genres_list
    return sounds


def create_playlist(db: Session, playlist: PlaylistCreate):
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


def get_recommendations_by_playlist(db: Session, playlist_id: str,
    limit: int = 5):
    playlist = db.query(models.Playlist).filter(models.Playlist.id ==
                                                playlist_id.replace("-",
                                                                    "")).first()
    if not playlist:
        raise Exception(f"Playlist {playlist_id} not found")

    playlist_genres = []
    for sound in playlist.sounds:
        if sound.genres_list:
            playlist_genres.extend(sound.genres_list)
    if not playlist_genres:
        return []

    top_genres = [genre for genre, _ in Counter(playlist_genres).most_common(3)]
    filtered_sounds = list(filter(lambda s:
                                  (has_genre_in_list(s, top_genres) &
                                   (s not in playlist.sounds)),
                                  get_sounds(db)))

    recommended_sounds = random.sample(filtered_sounds,
                                       min(limit, len(filtered_sounds)))

    return recommended_sounds


def has_genre_in_list(sound: Sound, genres: [str]):
    for genre in sound.genres:
        if genre in genres:
            return True
    return False
