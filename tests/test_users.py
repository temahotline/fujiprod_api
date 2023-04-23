import uuid
import json
import pytest
from sqlalchemy import insert, select

from conftest import async_session_maker
from src.users.models import User, SignUpSource


async def test_create_user():
    async with async_session_maker() as session:
        stmt = insert(User).values(sign_up_source="VK", id_on_source="test")
        await session.execute(stmt)
        await session.commit()

        query = select(User)
        result = await session.execute(query)
        print(result.all())
