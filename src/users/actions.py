from uuid import UUID
from src.users.dals import UserDAL
from src.users.schemas import UserCreate, ShowUser


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                sign_up_source=body.sign_up_source,
                id_on_source=body.id_on_source,
            )
            return ShowUser(
                user_id=user.user_id,
                sign_up_source=user.sign_up_source,
                id_on_source=user.id_on_source,
            )


async def _get_user_by_id(user_id: UUID, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if user is not None:
                return user
