from uuid import UUID
from typing import Optional
from pydantic import BaseModel, conint


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


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
    number_on_tracklist: conint(ge=1)
    tiktok_timing: conint(ge=0)
    explicit_content: bool
    text: Optional[str]
    karaoke_text: Optional[str]
    isrc: Optional[str]


class UpdatedTrackResponse(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    music_writer: Optional[str] = None
    text_writer: Optional[str] = None
    track: Optional[str] = None
    number_on_tracklist: Optional[int] = None
    tiktok_timing: Optional[int] = None
    explicit_content: Optional[bool] = None
    text: Optional[str] = None
    karaoke_text: Optional[str] = None
    isrc: Optional[str] = None
