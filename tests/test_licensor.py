import json

from sqlalchemy import select

from src.licensor.models import Licensor
from tests.conftest import async_session_maker, client


async def test_create_new_licensor(user):
    user_data, user_id = user
    async with async_session_maker() as session:
        licensor_data = {
            "user_id": str(user_id),
            "full_name": "test",
            "birthday": "2000-01-01",
            "passport_number": "test",
            "passport_issue_date": "2000-01-01",
            "registration": "test"
        }
        print(json.dumps(licensor_data))
        response = client.post("/licensor/", json=licensor_data)
        assert response.status_code == 200
        async with session.begin():
            stmt = select(Licensor).where(Licensor.user_id == user_id)
            result = await session.execute(stmt)
            licensor = result.scalar()
            assert licensor is not None
            assert str(licensor.user_id) == user_id
            assert licensor.full_name == licensor_data["full_name"]
            assert licensor.birthday.strftime("%Y-%m-%d") == licensor_data["birthday"]
            assert licensor.passport_number == licensor_data["passport_number"]
            assert licensor.passport_issue_date.strftime("%Y-%m-%d") == licensor_data["passport_issue_date"]
            assert licensor.registration == licensor_data["registration"]


async def test_get_licensor_by_id(user):
    user_data, user_id = user
    async with async_session_maker() as session:
        licensor_data = {
            "user_id": str(user_id),
            "full_name": "test",
            "birthday": "2000-01-01",
            "passport_number": "test",
            "passport_issue_date": "2000-01-01",
            "registration": "test"
        }
        response = client.post("/licensor/", json=licensor_data)
        licensor_id = response.json()["licensor_id"]
        response = client.get(f"/licensor/{licensor_id}")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["user_id"] == licensor_data["user_id"]
        assert response_data["full_name"] == licensor_data["full_name"]
        assert response_data["birthday"] == licensor_data["birthday"]
        assert response_data["passport_number"] == licensor_data["passport_number"]
        assert response_data["passport_issue_date"] == licensor_data["passport_issue_date"]
        assert response_data["registration"] == licensor_data["registration"]
        assert response_data["licensor_id"] == licensor_id


async def test_update_licensor(user):
    user_data, user_id = user
    async with async_session_maker() as session:
        licensor_data = {
            "user_id": str(user_id),
            "full_name": "test",
            "birthday": "2000-01-01",
            "passport_number": "test",
            "passport_issue_date": "2000-01-01",
            "registration": "test"
        }
        response = client.post("/licensor/", json=licensor_data)
        licensor_id = response.json()["licensor_id"]
        new_licensor_data = {
            "full_name": "new_test",
            "passport_number": "new_test",
            "passport_issue_date": "2001-01-01",
            "registration": "new_test"
        }
        response = client.patch(f"/licensor/{licensor_id}", json=new_licensor_data)
        assert response.status_code == 200
        async with session.begin():
            stmt = select(Licensor).where(Licensor.licensor_id == licensor_id)
            result = await session.execute(stmt)
            licensor = result.scalar()
            assert licensor is not None
            assert str(licensor.user_id) == user_id
            assert licensor.full_name == new_licensor_data["full_name"]
            assert licensor.birthday.strftime("%Y-%m-%d") == licensor_data["birthday"]
            assert licensor.passport_number == new_licensor_data["passport_number"]
            assert licensor.passport_issue_date.strftime("%Y-%m-%d") == new_licensor_data["passport_issue_date"]
            assert licensor.registration == new_licensor_data["registration"]
            assert str(licensor.licensor_id) == licensor_id
