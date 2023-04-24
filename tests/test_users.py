import uuid
import json
from sqlalchemy import select

from conftest import async_session_maker, client
from src.users.models import User, SignUpSource


async def test_create_user():
    user_data = {
        "sign_up_source": "VK",
        "id_on_source": "test"
    }
    response = client.post("/users/", content=json.dumps(user_data))
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["sign_up_source"] == user_data["sign_up_source"]
    assert response_data["id_on_source"] == user_data["id_on_source"]
    assert uuid.UUID(response_data["user_id"])
    async with async_session_maker() as session:
        async with session.begin():
            stmt = select(User).where(User.user_id == response_data["user_id"])
            result = await session.execute(stmt)
            user = result.scalar()
            assert user is not None
            assert user.sign_up_source == SignUpSource.VK
            assert user.id_on_source == user_data["id_on_source"]
            assert user.user_id == uuid.UUID(response_data["user_id"])


async def test_create_user_with_invalid_sign_up_source():
    user_data = {
        "sign_up_source": "invalid",
        "id_on_source": "test"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid data"


async def test_create_user_with_invalid_id_on_source():
    user_data = {
        "sign_up_source": "VK",
        "id_on_source": {1: "test"}
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "str type expected"


async def test_get_user_by_id():
    user_data = {
        "sign_up_source": "VK",
        "id_on_source": "test"
    }
    response = client.post("/users/", json=user_data)
    response_data = response.json()
    user_id = response_data["user_id"]
    response = client.get(f"/users/{user_id}")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["sign_up_source"] == user_data["sign_up_source"]
    assert response_data["id_on_source"] == user_data["id_on_source"]
    assert response_data["user_id"] == user_id


async def test_get_user_by_invalid_id():
    user_id = uuid.uuid4()
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_get_user_by_invalid_id_format():
    user_id = "invalid"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid uuid"


async def test_create_two_users_with_same_data():
    user_data = {
        "sign_up_source": "VK",
        "id_on_source": "test"
    }
    response1 = client.post("/users/", json=user_data)
    response1_data = response1.json()
    assert response1.status_code == 200
    assert response1_data["sign_up_source"] == user_data["sign_up_source"]
    assert response1_data["id_on_source"] == user_data["id_on_source"]
    assert uuid.UUID(response1_data["user_id"])
    response2 = client.post("/users/", json=user_data)
    response2_data = response2.json()
    assert response2.status_code == 200
    assert response1_data["user_id"] == response2_data["user_id"]
