from uuid import UUID
from fastapi import APIRouter, Depends

from src.releases.actions import (_create_new_release,
                                  _get_release_by_id,
                                  _update_release)
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
    return await _get_release_by_id(release_id, db)


@releases_router.patch("/{release_id}")
async def update_release_by_id(
        release_id: UUID,
        body: UpdatedReleaseResponse,
        db: AsyncSession = Depends(get_db),
) -> UUID:
    updated_release_params = body.dict(exclude_unset=True)
    return await _update_release(
        updated_release_params=updated_release_params,
        release_id=release_id,
        session=db
    )
