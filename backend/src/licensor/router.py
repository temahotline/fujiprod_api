from uuid import UUID
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException

from src.licensor.actions import (_create_new_licensor,
                                  _get_licensor_by_id,
                                  _update_licensor)
from src.licensor.schemas import (LicensorCreate, ShowLicensor,
                                  UpdatedLicensorResponse)
from src.database import AsyncSession, get_db


logger = getLogger(__name__)

licensor_router = APIRouter()


@licensor_router.post("/")
async def create_licensor(
        body: LicensorCreate,
        db: AsyncSession = Depends(get_db),) -> ShowLicensor:
    return await _create_new_licensor(body, db)


@licensor_router.get("/{licensor_id}")
async def show_licensor(
        licensor_id: UUID,
        db: AsyncSession = Depends(get_db),) -> ShowLicensor:
    licensor = await _get_licensor_by_id(licensor_id, db)
    if not licensor:
        raise HTTPException(
            status_code=404, detail="Licensor not found"
        )
    return licensor


@licensor_router.patch("/{licensor_id}")
async def update_licensor_by_id(
        licensor_id: UUID,
        body:  UpdatedLicensorResponse,
        db: AsyncSession = Depends(get_db),) -> UUID:
    updated_licensor_params = body.dict(exclude_unset=True)
    update_licensor = await _update_licensor(
        updated_licensor_params=updated_licensor_params,
        licensor_id=licensor_id,
        db=db
    )
    if not update_licensor:
        raise HTTPException(
            status_code=404, detail="Licensor not found"
        )
    return update_licensor
