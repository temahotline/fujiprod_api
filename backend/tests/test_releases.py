from sqlalchemy import select

from tests.conftest import async_session_maker, client
from src.releases.models import Release


async def test_create_release_with_invavalid_release_date(user, licensor):
    user_id = str(user.user_id)
    licensor_id = str(licensor.licensor_id)
    release_data = {
        "user_id": user_id,
        "licensor_id": licensor_id,
        "release_type": "SINGLE",
        "title": "test",
        "artist": "test",
        "release_date": "2023-01-01",
        "on_sale_date": "2023-01-02",
        "cover": "test",
        "genre": "test",
        "upc": "test"
    }
    response = client.post("/releases/", json=release_data)
    assert response.status_code == 422


async def test_create_release_without_licensor(user):
    user_id = str(user.user_id)
    release_data = {
        "user_id": user_id,
        "release_type": "SINGLE",
        "title": "test",
        "artist": "test",
        "release_date": "2023-08-24",
        "on_sale_date": "2023-08-24",
        "cover": "test",
        "genre": "test",
        "upc": "test"
    }
    response = client.post("/releases/", json=release_data)
    assert response.status_code == 422


async def test_update_release(ac, release):
    release_id = str(release.release_id)
    update_release_data = {
        "release_type": "SINGLE",
        "title": "new_string",
        "artist": "new_string",
        "release_date": "2023-08-24",
        "on_sale_date": "2023-08-24",
        "cover": "new_string",
        "genre": "new_string",
        "upc": "new_string"
    }
    response = client.patch(f"/releases/{release_id}", json=update_release_data)
    assert response.status_code == 200
    async with async_session_maker() as session:
        async with session.begin():
            stmt = select(Release).where(Release.release_id == release_id)
            result = await session.execute(stmt)
            release = result.scalar()
            assert release is not None
            assert release.release_type == update_release_data["release_type"]
            assert release.title == update_release_data["title"]
            assert release.artist == update_release_data["artist"]
            assert release.release_date.strftime("%Y-%m-%d") == update_release_data["release_date"]
            assert release.on_sale_date.strftime("%Y-%m-%d") == update_release_data["on_sale_date"]
            assert release.cover == update_release_data["cover"]
            assert release.genre == update_release_data["genre"]
            assert release.upc == update_release_data["upc"]
            assert str(release.release_id) == release_id
