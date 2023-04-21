from uuid import UUID

from src.releases.dals import ReleaseDAL
from src.releases.schemas import ReleaseCreate, ShowRelease


async def _create_new_release(body: ReleaseCreate, db) -> ShowRelease:
    async with db as session:
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


async def _get_release_by_id(release_id: UUID, db) -> ShowRelease:
    async with db as session:
        async with session.begin():
            release_dal = ReleaseDAL(session)
            release = await release_dal.get_release_by_id(release_id)
            if release is not None:
                return ShowRelease.from_orm(release)


async def _update_release(
        updated_release_params: dict,
        release_id: UUID,
        db) -> UUID:
    async with db as session:
        async with session.begin():
            release_dal = ReleaseDAL(session)
            updated_release_id = await release_dal.update_release(
                release_id, **updated_release_params
            )
            if updated_release_id is not None:
                return updated_release_id
