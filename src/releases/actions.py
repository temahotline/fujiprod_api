from uuid import UUID

from src.releases.dals import ReleaseDAL, TrackDAL
from src.releases.schemas import (ReleaseCreate, ShowRelease,
                                  TrackCreate, ShowTrack)


async def _create_new_release(body: ReleaseCreate, session) -> ShowRelease:
    async with session.begin():
        release_dal = ReleaseDAL(session)
        release = await release_dal.create_release(
            user_id=body.user_id,
            licensor_id=body.licensor_id,
            release_type=body.release_type,
            title=body.title,
            artist=body.artist,
            on_sale_date=body.on_sale_date,
            cover=body.cover,
            genre=body.genre,
            release_date=body.release_date,
            upc=body.upc,
        )
        return ShowRelease.from_orm(release)


async def _get_release_by_id(release_id: UUID, session) -> ShowRelease:
    async with session.begin():
        release_dal = ReleaseDAL(session)
        release = await release_dal.get_release_by_id(release_id)
        if release is not None:
            return ShowRelease.from_orm(release)


async def _create_new_track(body: TrackCreate, session) -> ShowTrack:
    async with session.begin():
        track_dal = TrackDAL(session)
        track = await track_dal.create_track(
            release_id=body.release_id,
            title=body.title,
            artist=body.artist,
            music_writer=body.music_writer,
            text_writer=body.text_writer,
            track=body.track,
            number_on_tracklist=body.number_on_tracklist,
            explicit_content=body.explicit_content,
            tiktok_timing=body.tiktok_timing,
            text=body.text,
            karaoke_text=body.karaoke_text,
            isrc=body.isrc,
        )
        return ShowTrack.from_orm(track)


async def _get_track_by_id(track_id: UUID, session) -> ShowTrack:
    async with session.begin():
        track_dal = TrackDAL(session)
        track = await track_dal.get_track_by_id(track_id)
        if track is not None:
            return ShowTrack.from_orm(track)
