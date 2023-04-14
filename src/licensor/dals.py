from uuid import UUID
from datetime import date
from typing import Union
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.licensor.models import Licensor


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
            self, licensor_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(Licensor)
            .where(Licensor.licensor_id == licensor_id)
            .values(kwargs)
            .returning(Licensor.licensor_id)
        )
        res = await self.db_session.execute(query)
        updated_licensor_id_row = res.fetchone()
        if updated_licensor_id_row is not None:
            return updated_licensor_id_row[0]
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
