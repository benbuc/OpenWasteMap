from fastapi.testclient import TestClient
from random import randint, random
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.waste_sample import create_random_waste_sample
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_datetime


def test_create_waste_sample(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"waste_level": 3, "latitude": 12.345, "longitude": 23.456}
    response = client.post(
        f"{settings.API_V1_STR}/waste-samples/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["waste_level"] == data["waste_level"]
    assert content["latitude"] == data["latitude"]
    assert content["longitude"] == data["longitude"]
    assert "id" in content
    assert "owner_id" in content


def test_create_waste_samples_bulk(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    users = [create_random_user(db) for _ in range(2)]
    data = [
        {
            "waste_level": randint(0, 10),
            "latitude": random() * 90,
            "longitude": random() * 90,
            "owner_nickname": users[randint(0, len(users) - 1)].nickname,
            "sampling_date": random_datetime().isoformat(),
        }
        for _ in range(10)
    ]
    r = client.post(
        f"{settings.API_V1_STR}/waste-samples/bulk",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    content = r.json()
    for sample, stored_id in zip(data, content):
        stored_sample = crud.waste_sample.get(db=db, id=stored_id)
        assert stored_sample
        assert sample["waste_level"] == stored_sample.waste_level
        assert sample["latitude"] == stored_sample.latitude
        assert sample["longitude"] == stored_sample.longitude
        assert sample["owner_nickname"] == stored_sample.owner.nickname
        assert sample["sampling_date"] == stored_sample.sampling_date.isoformat()


def test_read_waste_sample(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    waste_sample = create_random_waste_sample(db)
    response = client.get(
        f"{settings.API_V1_STR}/waste-samples/{waste_sample.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["waste_level"] == waste_sample.waste_level
    assert content["latitude"] == waste_sample.latitude
    assert content["longitude"] == waste_sample.longitude
    assert content["id"] == waste_sample.id
    assert content["owner_id"] == waste_sample.owner_id


def test_read_waste_sample_without_owner(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    waste_sample = create_random_waste_sample(db, create_owner=False)
    assert waste_sample.owner_id is None
    response = client.get(
        f"{settings.API_V1_STR}/waste-samples/{waste_sample.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["owner_id"] is None
    assert content["waste_level"] == waste_sample.waste_level


def test_get_all_waste_samples(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    waste_samples = [
        create_random_waste_sample(db, create_owner=False) for _ in range(5)
    ]
    response = client.get(
        f"{settings.API_V1_STR}/waste-samples/all", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= len(waste_samples)
