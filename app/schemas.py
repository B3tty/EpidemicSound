import uuid
from typing import List

from pydantic import BaseModel


class CreditBase(BaseModel):
    name: str
    role: str


class CreditCreate(CreditBase):
    pass


class Credit(CreditBase):
    id: uuid.UUID
    sound_id: uuid.UUID

    class ConfigDict:
        from_attributes = True


class SoundBase(BaseModel):
    title: str
    bpm: int
    genres: List[str]
    duration_in_seconds: int
    credits: List[CreditCreate]


class SoundCreate(SoundBase):
    pass


class ManySoundCreate(BaseModel):
    data: List[SoundCreate]


class Sound(SoundBase):
    id: uuid.UUID

    class ConfigDict:
        from_attributes = True


class ManySoundResponse(BaseModel):
    data: List[Sound]


class PlaylistBase(BaseModel):
    title: str
    sounds: List[uuid.UUID]


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    id: uuid.UUID

    class ConfigDict:
        from_attributes = True


class ManyPlaylistCreate(BaseModel):
    data: List[PlaylistCreate]


class ManyPlaylistResponse(BaseModel):
    data: List[Playlist]
