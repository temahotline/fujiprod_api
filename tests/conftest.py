import asyncio
from datetime import date
from typing import AsyncGenerator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
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
    user_data = {
        "sign_up_source": SignUpSource.VK,
        "id_on_source": "test"
    }
    resp_user = client.post("/users/", json=user_data)
    assert resp_user.status_code == 200
    user_id = resp_user.json()["user_id"]
    return user_data, user_id


@pytest.fixture
async def licensor(user):
    user_data, user_id = user
    licensor_data = {
        "user_id": user_id,
        "full_name": "test",
        "birthday": "2000-01-01",
        "passport_number": "test",
        "passport_issue_date": "2000-01-01",
        "registration": "test"
    }
    resp_licensor = client.post("/licensors/", json=licensor_data)
    assert resp_licensor.status_code == 200
    licensor_id = resp_licensor.json()["licensor_id"]
    return licensor_data, licensor_id


@pytest.fixture
async def release(licensor, user):
    user_data, user_id = user
    licensor_data, licensor_id = licensor
    release_data = {
        "user_id": user_id,
        "licensor_id": licensor_id,
        "release_type": "SINGLE",
        "title": "test",
        "artist": "test",
        "release_date": "2023-08-24",
        "on_sale_date": "2023-08-24",
        "cover": "test",
        "genre": "test"
    }
    resp_release = client.post("/releases/", json=release_data)
    assert resp_release.status_code == 200
    release_id = resp_release.json()["release_id"]
    return release_data, release_id


@pytest.fixture
async def track(release):
    release_data, release_id = release
    track_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 1,
        "tiktok_timing": 1,
        "explicit_content": True,
        "text": "string",
        "karaoke_text": "string",
        }
    resp_track = client.post("/tracks/", json=track_data)
    assert resp_track.status_code == 200
    track_id = resp_track.json()["track_id"]
    return track_data, track_id


@pytest.fixture
async def order(user):
    user_data, user_id = user
    order_data = {
        "user_id": user_id
    }
    resp_order = client.post("/orders/", json=order_data)
    assert resp_order.status_code == 200
    order_id = resp_order.json()["order_id"]
    return order_data, order_id
