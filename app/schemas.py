from typing import List

from pydantic import BaseModel


class CreditBase(BaseModel):
    name: str
    role: str


class CreditCreate(CreditBase):
    pass


class Credit(CreditBase):
    id: int
    sound_id: int

    class Config:
        from_attributes = True


class SoundBase(BaseModel):
    title: str
    bpm: int
    genres: List[str]
    duration_in_seconds: int
    credits: List[CreditCreate]


class SoundCreate(SoundBase):
    pass


class Sound(SoundBase):
    id: int

    class Config:
        from_attributes = True


class PlaylistBase(BaseModel):
    title: str
    sounds: List[int]


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: int

    class Config:
        from_attributes = True
