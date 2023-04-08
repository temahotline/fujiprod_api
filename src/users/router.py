from logging import getLogger
from fastapi import APIRouter, Depends

from src.users.actions import _create_new_user
from src.users.schemas import UserCreate, ShowUser
from src.database import AsyncSession, get_db

logger = getLogger(__name__)

users_router = APIRouter()


@users_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate,  db: AsyncSession = Depends(get_db),) -> ShowUser:
    return await _create_new_user(body, db)
