from uuid import UUID
from logging import getLogger
from fastapi import APIRouter, Depends

from src.users.actions import (_create_new_user,
                               _get_user_by_id,
                               _create_new_licensor,
                               _get_licensor_by_id)
from src.users.schemas import (UserCreate,
                               ShowUser,
                               LicensorCreate,
                               ShowLicensor)
from src.database import AsyncSession, get_db


logger = getLogger(__name__)

users_router = APIRouter()
licensor_router = APIRouter()


@users_router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db),) -> ShowUser:
    return await _create_new_user(body, db)


@users_router.get("/{user_id}", response_model=ShowUser)
async def show_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),) -> ShowUser:
    return await _get_user_by_id(user_id, db)


@licensor_router.post("/")
async def create_licensor(
        body: LicensorCreate,
        db: AsyncSession = Depends(get_db),) -> ShowLicensor:
    return await _create_new_licensor(body, db)


@licensor_router.get("/{licensor_id}")
async def show_licensor(
        licensor_id: UUID,
        db: AsyncSession = Depends(get_db),) -> ShowLicensor:
    return await _get_licensor_by_id(licensor_id,db)
