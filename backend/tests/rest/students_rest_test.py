from fastapi import status
from app.models import StudentCreate
from fastapi.testclient import TestClient


def test_full_student_life_cycle(client: TestClient):

    # Create
    student = StudentCreate(sid="TSTSTU00", first_name="Testinio", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()

    # Read
    get_response = client.get(f"/students/{response_json.get('student').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("student") is not None
    assert get_response.json().get("student").get("first_name") == student.first_name

    # Update
    new_first_name = "Actualberto"
    update_response = client.put(
        f"/students/{response_json.get('student').get('id')}",
        json={"first_name": new_first_name},
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json().get("updated_student") is not None
    assert (
        update_response.json().get("updated_student").get("first_name")
        == new_first_name
    )

    # Validate Update
    get_response = client.get(f"/students/{response_json.get('student').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("student") is not None
    assert get_response.json().get("student").get("first_name") == new_first_name

    # Delete
    delete_response = client.delete(
        f"/students/{response_json.get('student').get('id')}"
    )
    assert delete_response.status_code == status.HTTP_200_OK

    # Validate Delete
    get_response = client.get(f"/students/{response_json.get('student').get('id')}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_multiple_creation(client: TestClient):
    student = StudentCreate(sid="STU1", first_name="Multiple 1", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    student = StudentCreate(sid="STU2", first_name="Multiple 2", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    student = StudentCreate(sid="STU3", first_name="Multiple 3", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    student = StudentCreate(sid="STU4", first_name="Multiple 4", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    # Validate creation
    get_all_response = client.get("/students")
    assert get_all_response.status_code == status.HTTP_200_OK
    assert get_all_response.json().get("students") is not None
    assert len(get_all_response.json().get("students")) == 4
    assert get_all_response.json().get("students")[0].get("first_name") == "Multiple 1"
    assert get_all_response.json().get("students")[1].get("first_name") == "Multiple 2"
    assert get_all_response.json().get("students")[2].get("first_name") == "Multiple 3"
    assert get_all_response.json().get("students")[3].get("first_name") == "Multiple 4"


def test_no_same_sid_allowed(client: TestClient):
    student = StudentCreate(sid="STU1", first_name="Same 1", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    student = StudentCreate(sid="STU1", first_name="Same 2", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_409_CONFLICT


def test_all_attributes_saved_correctly(client: TestClient):
    student = StudentCreate(
        sid="STU1",
        first_name="Same 1",
        last_name="Student",
        email="email",
        phone="55555",
    )
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    get_response = client.get(
        f"/students/{create_response.json().get('student').get('id')}"
    )
    assert get_response.status_code == status.HTTP_200_OK

    get_student = get_response.json().get("student")
    assert get_student is not None
    assert get_student.get("sid") == student.sid
    assert get_student.get("first_name") == student.first_name
    assert get_student.get("last_name") == student.last_name
    assert get_student.get("email") == student.email
    assert get_student.get("phone") == student.phone
