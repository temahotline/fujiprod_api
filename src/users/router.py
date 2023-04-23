from uuid import UUID
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException

from src.users.actions import _create_new_user, _get_user_by_id
from src.users.schemas import UserCreate, ShowUser
from src.database import AsyncSession, get_db


logger = getLogger(__name__)

users_router = APIRouter()


@users_router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db),) -> ShowUser:
    return await _create_new_user(body, db)


@users_router.get("/{user_id}", response_model=ShowUser)
async def show_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
