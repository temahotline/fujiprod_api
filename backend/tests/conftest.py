import asyncio
from datetime import date
from typing import AsyncGenerator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_db
from src.main import app
from src.database import Base
from src.licensor.models import Licensor
from src.users.models import User, SignUpSource
from src.releases.models import Release, ReleaseType
from src.tracks.models import Track
from src.orders.models import Order, OrderStatus


metadata = Base.metadata


# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def user():
    async def create_user():
        async with async_session_maker() as session:
            user = User(
                sign_up_source=SignUpSource.VK,
                id_on_source="test"
            )
            session.add(user)
            await session.commit()

            async with async_session_maker() as new_session:
                stmt = select(User).where(
                    and_(User.sign_up_source == SignUpSource.VK,
                         User.id_on_source == "test")
                )
                res = await new_session.execute(stmt)
                user = res.scalar()
                return user

    created_user = await create_user()
    yield created_user


@pytest.fixture
async def licensor(user):
    async def create_licensor():
        async with async_session_maker() as session:
            licensor = Licensor(
                user_id=user.user_id,
                full_name="test",
                birthday=date(2000, 1, 1),
                passport_number="test",
                passport_issue_date=date(2000, 1, 1),
                registration="test"
            )
            session.add(licensor)
            await session.commit()

            async with async_session_maker() as new_session:
                stmt = select(Licensor).where(
                    Licensor.user_id == user.user_id)
                res = await new_session.execute(stmt)
                licensor = res.scalar()
                return licensor

    created_licensor = await create_licensor()
    yield created_licensor


@pytest.fixture
async def release(user, licensor):
    async def create_release():
        async with async_session_maker() as session:
            release = Release(
                user_id=user.user_id,
                licensor_id=licensor.licensor_id,
                release_type=ReleaseType.SINGLE,
                title="test",
                artist="test",
                release_date=date(2023, 1, 1),
                on_sale_date=date(2023, 1, 1),
                cover="test",
                genre="test"
            )
            session.add(release)
            await session.commit()

            async with async_session_maker() as new_session:
                stmt = select(Release).where(
                    Release.user_id == user.user_id)
                res = await new_session.execute(stmt)
                release = res.scalar()
                return release

    created_release = await create_release()
    yield created_release


@pytest.fixture
async def track(release):
    async def create_track():
        async with async_session_maker() as session:
            track = Track(
                release_id=release.release_id,
                title="test",
                artist="test",
                music_writer="test",
                text_writer="test",
                track="test",
                number_on_tracklist=1,
                tiktok_timing=1,
                explicit_content=True,
                text="test",
                karaoke_text="test"
            )
            session.add(track)
            await session.commit()

            async with async_session_maker() as new_session:
                stmt = select(Track).where(
                    Track.release_id == release.release_id)
                res = await new_session.execute(stmt)
                track = res.scalar()
                return track

    created_track = await create_track()
    yield created_track


@pytest.fixture
async def order(user):
    async def create_order():
        async with async_session_maker() as session:
            order = Order(
                user_id=user.user_id,
            )
            session.add(order)
            await session.commit()

            async with async_session_maker() as new_session:
                stmt = select(Order).where(
                    Order.user_id == user.user_id)
                res = await new_session.execute(stmt)
                order = res.scalar()
                return order

    created_order = await create_order()
    yield created_order
