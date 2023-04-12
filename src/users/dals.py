from uuid import UUID
from datetime import date
from typing import Union
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User, Licensor


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


class LicensorDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_licensor(
            self,
            user_id: UUID,
            full_name: str,
            birthday: date,
            passport_number: str,
            passport_issue_date: date,
            registration: str,
    ) -> Licensor:
        new_licensor = Licensor(
            user_id=user_id,
            full_name=full_name,
            birthday=birthday,
            passport_number=passport_number,
            passport_issue_date=passport_issue_date,
            registration=registration,
        )
        self.db_session.add(new_licensor)
        await self.db_session.flush()
        return new_licensor

    async def update_licensor(
            self, licensor_id: UUID, **kwargs) -> Union[Licensor, None]:
        query = (
            update(Licensor)
            .where(Licensor.licensor_id == licensor_id)
            .values(kwargs)
            .returning(Licensor)
        )
        res = await self.db_session.execute(query)
        updated_licensor_row = res.fetchone()
        if updated_licensor_row is not None:
            return updated_licensor_row[0]
        return None

    async def get_licensor_by_id(
            self, licensor_id: UUID) -> Union[Licensor, None]:
        query = (
            select(Licensor)
            .where(Licensor.licensor_id == licensor_id)
        )
        res = await self.db_session.execute(query)
        licensor = res.fetchone()
        if licensor is not None:
            return licensor[0]
