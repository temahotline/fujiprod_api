from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from src.releases.actions import (_create_new_release,
                                  _get_release_by_id,
                                  _update_release, _get_releases)
from src.releases.schemas import (ReleaseCreate, ShowRelease,
                                  UpdatedReleaseResponse)
from src.database import AsyncSession, get_db

releases_router = APIRouter()


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
    release = await _get_release_by_id(release_id, db)
    if not release:
        raise HTTPException(
            status_code=404, detail="Release not found")
    return await _get_release_by_id(release_id, db)


@releases_router.patch("/{release_id}")
async def update_release_by_id(
        release_id: UUID,
        body: UpdatedReleaseResponse,
        db: AsyncSession = Depends(get_db),
) -> UUID:
    updated_release_params = body.dict(exclude_unset=True)
    update_release = await _update_release(
        updated_release_params=updated_release_params,
        release_id=release_id,
        db=db
    )
    if not update_release:
        raise HTTPException(
            status_code=404, detail="Release not found")
    return update_release


@releases_router.get("/", response_model=List[ShowRelease])
async def get_releases_list(
    user_id: Optional[UUID] = None,
    licensor_id: Optional[UUID] = None,
    title: Optional[str] = None,
    artist: Optional[str] = None,
    genre: Optional[str] = None,
    sort_by_release_date: Optional[str] = None,
    sort_by_on_sale_date: Optional[str] = None,
    page: int = 1,
    db: AsyncSession = Depends(get_db),
) -> List[ShowRelease]:
    return await _get_releases(
        user_id=user_id,
        licensor_id=licensor_id,
        title=title,
        artist=artist,
        genre=genre,
        sort_by_release_date=sort_by_release_date,
        sort_by_on_sale_date=sort_by_on_sale_date,
        page=page,
        db=db
    )
