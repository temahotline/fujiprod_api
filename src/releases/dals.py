import uuid
from typing import Optional, Union
from uuid import UUID
from datetime import date
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.releases.models import Release, ReleaseType, Track


class ReleaseDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_release(
        self,
        user_id: uuid.UUID,
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
            self, release_id: UUID, **kwargs) -> Union[Release, None]:
        query = (
            update(Release)
            .where(Release.release_id == release_id)
            .values(kwargs)
            .returning(Release)
        )
        res = await self.db_session.execute(query)
        updated_release_row = res.fetchone()

        if updated_release_row is not None:
            return updated_release_row[0]
        return None

    async def get_release_by_id(self, release_id: UUID) -> Union[Release, None]:
        query = select(Release).where(Release.release_id == release_id)
        res = await self.db_session.execute(query)
        release_row = res.fetchone()
        if release_row is not None:
            return release_row[0]
        return None


class TrackDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_track(
        self,
        release_id: UUID,
        title: str,
        artist: str,
        music_writer: str,
        text_writer: str,
        track: str,
        number_on_tracklist: int,
        explicit_content: bool,
        tiktok_timing: Optional[int] = 0,
        text: Optional[str] = None,
        karaoke_text: Optional[str] = None,
        isrc: Optional[str] = None,
    ) -> Track:
        new_track = Track(
            release_id=release_id,
            title=title,
            artist=artist,
            music_writer=music_writer,
            text_writer=text_writer,
            track=track,
            number_on_tracklist=number_on_tracklist,
            tiktok_timing=tiktok_timing,
            explicit_content=explicit_content,
            text=text,
            karaoke_text=karaoke_text,
            isrc=isrc,
        )
        self.db_session.add(new_track)
        await self.db_session.flush()
        return new_track

    async def update_track(self, track_id: UUID, **kwargs) -> Union[Track, None]:
        query = (
            update(Track)
            .where(Track.track_id == track_id)
            .values(kwargs)
            .returning(Track)
        )
        res = await self.db_session.execute(query)
        updated_track_row = res.fetchone()

        if updated_track_row is not None:
            return updated_track_row[0]
        return None

    async def get_track_by_id(self, track_id: UUID) -> Union[Track, None]:
        query = select(Track).where(Track.track_id == track_id)
        res = await self.db_session.execute(query)
        track_row = res.fetchone()
        if track_row is not None:
            return track_row[0]
        return None
