from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.releases.models import ReleaseType
from src.tracks.schemas import ShowTrack


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
    release_date: date
    on_sale_date: date
    cover: str
    genre: str
    upc: Optional[str]
    tracks: Optional[ShowTrack]


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


class UpdatedReleaseResponse(BaseModel):
    user_id: Optional[UUID] = None
    licensor_id: Optional[UUID] = None
    release_type: Optional[ReleaseType] = None
    title: Optional[str] = None
    artist: Optional[str] = None
    release_date: Optional[date] = None
    on_sale_date: Optional[date] = None
    cover: Optional[str] = None
    genre: Optional[str] = None
    upc: Optional[str] = None
