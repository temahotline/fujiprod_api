from uuid import UUID

from src.tracks.dals import TrackDAL
from src.tracks.schemas import TrackCreate, ShowTrack


async def _create_new_track(body: TrackCreate, db) -> ShowTrack:
    async with db as session:
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


async def _get_track_by_id(track_id: UUID, db) -> ShowTrack:
    async with db as session:
        async with session.begin():
            track_dal = TrackDAL(session)
            track = await track_dal.get_track_by_id(track_id)
            if track is not None:
                return ShowTrack.from_orm(track)


async def _update_track(
        updated_track_params: dict,
        track_id: UUID,
        db) -> UUID:
    async with db as session:
        async with session.begin():
            track_dal = TrackDAL(session)
            updated_track_id = await track_dal.update_track(
                track_id, **updated_track_params
            )
            if updated_track_id is not None:
                return updated_track_id
