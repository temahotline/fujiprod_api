import uuid
from typing import Optional, Union
from uuid import UUID
from datetime import date
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.releases.models import Release, ReleaseType


class ReleaseDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_release(
        self,
        user_id: UUID,
        licensor_id: UUID,
        release_type: ReleaseType,
        title: str,
        artist: str,
        on_sale_date: date,
        cover: str,
        genre: str,
        release_date: Optional[date] = None,
        upc: Optional[str] = None,
    ) -> Release:
        new_release = Release(
            user_id=user_id,
            licensor_id=licensor_id,
            release_type=release_type,
            title=title,
            artist=artist,
            on_sale_date=on_sale_date,
            cover=cover,
            genre=genre,
            release_date=release_date,
            upc=upc,
        )
        self.db_session.add(new_release)
        await self.db_session.flush()
        return new_release

    async def update_release(
            self, release_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(Release)
            .where(Release.release_id == release_id)
            .values(kwargs)
            .returning(Release.release_id)
        )
        res = await self.db_session.execute(query)
        updated_release_id_row = res.fetchone()

        if updated_release_id_row is not None:
            return updated_release_id_row[0]
        return None

    async def get_release_by_id(self, release_id: UUID) -> Union[Release, None]:
        query = select(Release).where(Release.release_id == release_id)
        res = await self.db_session.execute(query)
        release_row = res.unique().fetchone()
        if release_row is not None:
            return release_row[0]
        return None
