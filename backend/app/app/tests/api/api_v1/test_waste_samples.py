from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.waste_sample import create_random_waste_sample


def test_create_waste_sample(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"waste_level": 3, "latitude": 12.345, "longitude": 23.456}
    response = client.post(
        f"{settings.API_V1_STR}/waste_samples/",
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


def test_read_waste_sample(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    waste_sample = create_random_waste_sample(db)
    response = client.get(
        f"{settings.API_V1_STR}/waste_samples/{waste_sample.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["waste_level"] == waste_sample.waste_level
    assert content["latitude"] == waste_sample.latitude
    assert content["longitude"] == waste_sample.longitude
    assert content["id"] == waste_sample.id
    assert content["owner_id"] == waste_sample.owner_id
