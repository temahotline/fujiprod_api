from uuid import UUID
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from src.releases.models import ReleaseType


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowRelease(TunedModel):
    release_id: UUID
    user_id: UUID
    licensor_id: UUID
    release_type: ReleaseType
    title: str
    artist: str
    release_date: Optional[date]
    on_sale_date: date
    cover: str
    genre: str
    upc: Optional[str]


class ReleaseCreate(BaseModel):
    user_id: UUID
    licensor_id: UUID
    release_type: ReleaseType
    title: str
    artist: str
    release_date: Optional[date]
    on_sale_date: date
    cover: str
    genre: str
    upc: Optional[str]


class ShowTrack(TunedModel):
    track_id: UUID
    release_id: UUID
    title: str
    artist: str
    music_writer: str
    text_writer: str
    track: str
    number_on_tracklist: int
    tiktok_timing: int
    explicit_content: bool
    text: Optional[str]
    karaoke_text: Optional[str]
    isrc: Optional[str]


class TrackCreate(BaseModel):
    release_id: UUID
    title: str
    artist: str
    music_writer: str
    text_writer: str
    track: str
    number_on_tracklist: int
    tiktok_timing: int
    explicit_content: bool
    text: Optional[str]
    karaoke_text: Optional[str]
    isrc: Optional[str]
