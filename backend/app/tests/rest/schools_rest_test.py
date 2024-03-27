from fastapi import status
from app.models import SchoolCreate
from fastapi.testclient import TestClient


def test_full_school_life_cycle(client: TestClient):
    # Create
    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()

    # Read
    get_response = client.get(f"/schools/{response_json.get('school').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("school") is not None
    assert get_response.json().get("school").get("name") == "Test School"

    # Update
    update_response = client.put(
        f"/schools/{response_json.get('school').get('id')}",
        json={"name": "Updated School", "address": "123 Updated St"},
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json().get("updated_school") is not None
    assert update_response.json().get("updated_school").get("name") == "Updated School"

    # Validate Update
    get_response = client.get(f"/schools/{response_json.get('school').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("school") is not None
    assert get_response.json().get("school").get("name") == "Updated School"

    # Delete
    delete_response = client.delete(f"/schools/{response_json.get('school').get('id')}")
    assert delete_response.status_code == status.HTTP_200_OK

    # Validate Delete
    get_response = client.get(f"/schools/{response_json.get('school').get('id')}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_multiple_creation(client: TestClient):
    school = SchoolCreate(sid="SCH1", name="Multiple 1")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    school = SchoolCreate(sid="SCH2", name="Multiple 2")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    school = SchoolCreate(sid="SCH3", name="Multiple 3")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    school = SchoolCreate(sid="SCH4", name="Multiple 4")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    # Validate creation
    get_all_response = client.get("/schools")
    assert get_all_response.status_code == status.HTTP_200_OK
    assert get_all_response.json().get("schools") is not None
    assert len(get_all_response.json().get("schools")) == 4


def test_no_same_name_allowed(client: TestClient):
    school = SchoolCreate(sid="SCH1", name="Same 1")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    school = SchoolCreate(sid="SCH2", name="Same 1")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_409_CONFLICT


def test_no_same_sid_allowed(client: TestClient):
    school = SchoolCreate(sid="SCH1", name="Same 1")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    school = SchoolCreate(sid="SCH1", name="Same 2")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_409_CONFLICT


def test_all_attributes_saved_correctly(client: TestClient):
    school = SchoolCreate(
        sid="SCH1",
        name="School Name",
        address="123 Test St",
        phone="123-456-7890",
        email="email@example.com",
        website="school.example.com",
        city="Test City",
        state="TS",
        zip_code="12345",
    )
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()

    get_response = client.get(f"/schools/{response_json.get('school').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK

    get_response_school = get_response.json().get("school")
    assert get_response_school is not None
    assert get_response_school.get("sid") == school.sid
    assert get_response_school.get("name") == school.name
    assert get_response_school.get("address") == school.address
    assert get_response_school.get("phone") == school.phone
    assert get_response_school.get("email") == school.email
    assert get_response_school.get("website") == school.website
    assert get_response_school.get("city") == school.city
    assert get_response_school.get("state") == school.state
    assert get_response_school.get("zip_code") == school.zip_code
