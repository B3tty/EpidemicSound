import random
import uuid
from collections import Counter
from statistics import mean
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models
from app.models import Sound, Playlist
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
        raise LookupError(f"Playlist {playlist_id} not found")

    top_genres = get_top_playlist_genres(playlist)
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


def get_global_statistics(db: Session):
    total_sounds = db.query(func.count(Sound.id)).scalar()
    total_playlists = db.query(func.count(models.Playlist.id)).scalar()
    if total_sounds==0:
        return {
            "total_sounds": 0,
            "avg_bpm": 0,
            "top_genres": [],
            "avg_duration_in_seconds": 0,
            "total_playlists": total_playlists
        }

    genre_counts = db.query(Sound.genres, func.count(Sound.genres)).group_by(
        Sound.genres).order_by(func.count(Sound.genres).desc()).all()
    top_genres = [genre for genre, count in genre_counts][:3]
    average_bpm = db.query(func.avg(Sound.bpm)).scalar()
    average_duration = db.query(func.avg(Sound.duration_in_seconds)).scalar()
    return {
        "total_sounds": total_sounds,
        "avg_bpm": average_bpm,
        "top_genres": top_genres,
        "avg_duration_in_seconds": average_duration,
        "total_playlists": total_playlists
    }


def get_statistics_for_playlist(db: Session, playlist_id: str):
    playlist = db.query(models.Playlist).filter(models.Playlist.id ==
                                                playlist_id.replace("-",
                                                                    "")).first()
    if not playlist:
        raise LookupError(f"Playlist {playlist_id} not found")

    sounds = playlist.sounds
    if not sounds:
        return {
            "total_sounds": 0,
            "avg_bpm": 0,
            "top_genres": [],
            "avg_duration_in_seconds": 0,
            "total_duration_in_seconds": 0
        }

    nb_sounds = len(playlist.sounds)
    return {
        "total_sounds": nb_sounds,
        "avg_bpm": int(sum(sound.bpm for sound in sounds) / nb_sounds),
        "top_genres": get_top_playlist_genres(playlist),
        "avg_duration_in_seconds": int(sum(sound.duration_in_seconds for sound in sounds) /
                                       nb_sounds),
        "total_duration_in_seconds": sum(sound.duration_in_seconds for sound
                                         in sounds)
    }


def get_top_playlist_genres(playlist: Playlist, top=3):
    playlist_genres = []
    for sound in playlist.sounds:
        if sound.genres_list:
            playlist_genres.extend(sound.genres_list)
    if not playlist_genres:
        return []

    return [genre for genre, _ in Counter(playlist_genres).most_common(
        top)]

