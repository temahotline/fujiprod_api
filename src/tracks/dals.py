from typing import Optional, Union
from uuid import UUID
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tracks.models import Track


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
        track_row = res.unique().fetchone()
        if track_row is not None:
            return track_row[0]
        return None
