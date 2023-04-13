from uuid import UUID
from fastapi import APIRouter, Depends

from src.releases.actions import (_create_new_release,
                                  _get_release_by_id,
                                  _get_track_by_id,
                                  _create_new_track)
from src.releases.schemas import (ReleaseCreate, ShowRelease,
                                  TrackCreate, ShowTrack)
from src.database import AsyncSession, get_db

releases_router = APIRouter()
tracks_router = APIRouter()


@releases_router.post("/", response_model=ShowRelease)
async def create_release(
    body: ReleaseCreate,
    db: AsyncSession = Depends(get_db),
) -> ShowRelease:
    return await _create_new_release(body, db)


@releases_router.get("/{release_id}", response_model=ShowRelease)
async def show_release(
    release_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ShowRelease:
    return await _get_release_by_id(release_id, db)


@tracks_router.post("/", response_model=ShowTrack)
async def create_track(
    body: TrackCreate,
    db: AsyncSession = Depends(get_db),
) -> ShowTrack:
    return await _create_new_track(body, db)


@tracks_router.get("/{track_id}", response_model=ShowTrack)
async def show_track(
    track_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ShowTrack:
    return await _get_track_by_id(track_id, db)
