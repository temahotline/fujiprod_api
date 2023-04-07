from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, sign_up_source: str, id_on_source: str
    ) -> User:
        stmt = select(User).where(
            User.sign_up_source == sign_up_source
        ).where(User.id_on_source == id_on_source)
        result = await self.db_session.execute(stmt)
        user = result.scalar()
        if user:
            return user
        new_user = User(
            sign_up_source=sign_up_source,
            id_on_source=id_on_source,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
