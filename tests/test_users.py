import uuid
import json
import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {
        "sign_up_source": "WEBSITE",
        "id_on_source": "12345"
    }
    resp = client.post("/users/", json=user_data)
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["sign_up_source"] == user_data["sign_up_source"]
    assert data_from_resp["id_on_source"] == user_data["id_on_source"]

    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["sign_up_source"] == user_data["sign_up_source"]
    assert user_from_db["id_on_source"] == user_data["id_on_source"]
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
