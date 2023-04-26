from tests.conftest import client


async def test_get_track_by_id(track):
    track_id = str(track.track_id)
    response = client.get(f"/tracks/{track_id}")
    assert response.status_code == 200
    response = response.json()
    assert response["title"] == "test"
    assert response["artist"] == "test"
    assert response["music_writer"] == "test"
    assert response["text_writer"] == "test"
    assert response["track"] == "test"
    assert response["number_on_tracklist"] == 1
    assert response["tiktok_timing"] == 1
    assert response["explicit_content"] is True
    assert response["text"] == "test"
    assert response["karaoke_text"] == "test"


async def test_create_track_with_invalid_number_of_tracklist(release):
    release_id = str(release.release_id)
    treck_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 0,
        "tiktok_timing": 0,
        "explicit_content": True
    }
    response = client.post("/tracks/", json=treck_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 1"


async def test_create_track_with_invalid_tiktok_timing(release):
    release_id = str(release.release_id)
    treck_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 1,
        "tiktok_timing": -1,
        "explicit_content": True
    }
    response = client.post("/tracks/", json=treck_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 0"


async def test_create_track_with_invalid_explicit_content(release):
    release_id = str(release.release_id)
    treck_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 1,
        "tiktok_timing": 0,
        "explicit_content": "string"
    }
    response = client.post("/tracks/", json=treck_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value could not be parsed to a boolean"


async def test_create_track_with_invalid_release_id(release):
    release_id = str(release.release_id) + "1"
    treck_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 1,
        "tiktok_timing": 0,
        "explicit_content": True
    }
    response = client.post("/tracks/", json=treck_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid uuid"


async def test_create_and_update_track(release):
    release_id = str(release.release_id)
    treck_data = {
        "release_id": release_id,
        "title": "string",
        "artist": "string",
        "music_writer": "string",
        "text_writer": "string",
        "track": "string",
        "number_on_tracklist": 1,
        "tiktok_timing": 0,
        "explicit_content": True
    }
    response_first = client.post("/tracks/", json=treck_data)
    assert response_first.status_code == 200
    track_id = response_first.json()["track_id"]
    update_track_data = {
        "title": "new_string",
        "artist": "new_string",
        "music_writer": "new_string",
        "text_writer": "new_string",
        "track": "new_string",
        "number_on_tracklist": 2,
        "tiktok_timing": 1,
        "explicit_content": False,
        "text": "string",
        "karaoke_text": "string",
        "isrc": "string"
    }
    response_second = client.patch(f"/tracks/{track_id}", json=update_track_data)
    response_third = client.get(f"/tracks/{track_id}")

    assert response_second.status_code == 200
    assert response_third.status_code == 200
    response_third = response_third.json()
    assert response_third["title"] == "new_string"
    assert response_third["artist"] == "new_string"
    assert response_third["music_writer"] == "new_string"
    assert response_third["text_writer"] == "new_string"
    assert response_third["track"] == "new_string"
    assert response_third["number_on_tracklist"] == 2
    assert response_third["tiktok_timing"] == 1
    assert response_third["explicit_content"] is False
    assert response_third["text"] == "string"
    assert response_third["karaoke_text"] == "string"
    assert response_third["isrc"] == "string"
