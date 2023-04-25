from uuid import UUID
from typing import Union
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, sign_up_source: str, id_on_source: str) -> User:
        stmt = (
            select(User)
            .where(User.sign_up_source == sign_up_source)
            .where(User.id_on_source == id_on_source)
        )
        result = await self.db_session.execute(stmt)
        user = result.scalar()
        if user is not None:
            return user
        new_user = User(
            sign_up_source=sign_up_source,
            id_on_source=id_on_source,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(
            self, user_id: UUID, **kwargs) -> Union[User, None]:
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(kwargs)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        update_user_row = res.fetchone()
        if update_user_row is not None:
            return update_user_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
