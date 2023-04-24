import uuid
from typing import Optional, Union
from uuid import UUID
from datetime import date
from sqlalchemy import update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.releases.models import Release, ReleaseType


PAGE_SIZE: int = 10


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

    async def get_releases(
            self,
            user_id: Optional[UUID] = None,
            licensor_id: Optional[UUID] = None,
            title: Optional[str] = None,
            artist: Optional[str] = None,
            genre: Optional[str] = None,
            sort_by_release_date: Optional[str] = None,
            sort_by_on_sale_date: Optional[str] = None,
            page: int = 1
    ) -> list[Release]:
        query = select(Release)
        conditions = []
        if user_id is not None:
            conditions.append(Release.user_id == user_id)
        if licensor_id is not None:
            conditions.append(Release.licensor_id == licensor_id)
        if title is not None:
            conditions.append(Release.title == title)
        if artist is not None:
            conditions.append(Release.artist == artist)
        if genre is not None:
            conditions.append(Release.genre == genre)

        if conditions:
            query = query.where(and_(*conditions))

        if sort_by_release_date:
            if sort_by_release_date.lower() == 'asc':
                query = query.order_by(Release.release_date.asc())
            elif sort_by_release_date.lower() == 'desc':
                query = query.order_by(Release.release_date.desc())
        elif sort_by_on_sale_date:
            if sort_by_on_sale_date.lower() == 'asc':
                query = query.order_by(Release.on_sale_date.asc())
            elif sort_by_on_sale_date.lower() == 'desc':
                query = query.order_by(Release.on_sale_date.desc())
        offset = (page - 1) * PAGE_SIZE
        query = query.offset(offset).limit(PAGE_SIZE)
        res = await self.db_session.execute(query)
        orders = res.fetchall()
        return [order[0] for order in orders]
