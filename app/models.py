from typing import List

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

playlist_sounds = Table(
    'playlist_sounds',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('sound_id', Integer, ForeignKey('sounds.id'))
)


class Sound(Base):
    __tablename__ = 'sounds'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title = mapped_column(String, index=True)
    bpm = mapped_column(Integer)
    genres = mapped_column(String)  # Storing genres as a comma-separated string
    duration_in_seconds = mapped_column(Integer)
    credits = relationship("Credit", back_populates="sound")

    @property
    def genres_list(self):
        return self.genres.split(",") if self.genres else []

    playlists: Mapped[List["Playlist"]] = relationship(
        secondary=playlist_sounds,
        back_populates="sounds")


class Credit(Base):
    __tablename__ = 'credits'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = mapped_column(String, index=True)
    role = mapped_column(String)
    sound_id = mapped_column(Integer, ForeignKey('sounds.id'))

    sound: Mapped[List["Sound"]] = relationship(back_populates="credits")


class Playlist(Base):
    __tablename__ = 'playlists'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title = mapped_column(String, index=True)

    sounds: Mapped[List["Sound"]] = relationship(
        secondary=playlist_sounds,
        back_populates="playlists")
