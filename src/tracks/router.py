from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.tracks.actions import (_get_track_by_id,
                                _create_new_track,
                                _update_track)
from src.tracks.schemas import (TrackCreate, ShowTrack,
                                UpdatedTrackResponse)
from src.database import AsyncSession, get_db


tracks_router = APIRouter()


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
    track = await _get_track_by_id(track_id, db)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@tracks_router.patch("/{track_id}")
async def update_track_by_id(
        track_id: UUID,
        body:  UpdatedTrackResponse,
        db: AsyncSession = Depends(get_db),) -> UUID:
    updated_track_params = body.dict(exclude_unset=True)
    update_track = await _update_track(
        updated_track_params=updated_track_params,
        track_id=track_id,
        db=db
    )
    if not update_track:
        raise HTTPException(status_code=404, detail="Track not found")
    return update_track
