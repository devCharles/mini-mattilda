from fastapi import status
from app.models import (
    InscriptionCreate,
    SchoolCreate,
    Student,
    StudentCreate,
)
from fastapi.testclient import TestClient


def test_full_Inscription_life_cycle(client: TestClient):
    student = StudentCreate(sid="TSTSTU00", first_name="Test", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    created_student = Student(**create_response.json().get("student"))
    student_id = created_student.id

    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    school_id = create_response.json().get("school").get("id")

    other_student = StudentCreate(
        sid="TSTSTU01", first_name="Other", last_name="Student"
    )
    create_other_student_response = client.post(
        "/students", json=other_student.model_dump()
    )
    assert create_other_student_response.status_code == status.HTTP_200_OK
    other_student_id = create_other_student_response.json().get("student").get("id")

    assert student_id
    assert student_id != other_student_id

    # Create
    inscription = InscriptionCreate(school_id=school_id, student_id=student_id)
    create_response = client.post("/inscriptions", json=inscription.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()
    inscription_created = response_json.get("inscription")
    inscription_id = inscription_created.get("id")
    assert inscription_created.get("school_id") == school_id
    assert inscription_created.get("student_id") == student_id

    # Read
    get_response = client.get(f"/inscriptions/{inscription_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("inscription") is not None
    inscription_read = get_response.json().get("inscription")
    assert inscription_read.get("school_id") == school_id
    assert inscription_read.get("student_id") == student_id

    # Update
    update_response = client.put(
        f"/inscriptions/{inscription_id}",
        json={"student_id": other_student_id},
    )
    assert update_response.status_code == status.HTTP_200_OK

    # Validate Update
    validate_get_response = client.get(f"/inscriptions/{inscription_id}")
    assert validate_get_response.status_code == status.HTTP_200_OK
    assert validate_get_response.json().get("inscription") is not None
    inscription_updated = validate_get_response.json().get("inscription")
    assert inscription_updated.get("student_id") == other_student_id

    # Delete
    delete_response = client.delete(f"/inscriptions/{inscription_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    # Validate Delete
    get_response = client.get(f"/inscriptions/{inscription_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_raise_404_when_create_with_invalid_student_id(client: TestClient):
    school = SchoolCreate(sid="TSTSCH00", name="Test School")

    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    school_id = create_response.json().get("school").get("id")

    # Create
    inscription = InscriptionCreate(school_id=school_id, student_id=999)
    create_response = client.post("/inscriptions", json=inscription.model_dump())
    assert create_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_student_inscriptions(client: TestClient):
    student = StudentCreate(sid="TSTSTU00", first_name="Test", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    created_student = create_response.json().get("student")
    student_id = created_student.get("id")

    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    school_id = create_response.json().get("school").get("id")

    school_2 = SchoolCreate(sid="TSTSCH01", name="Test School 2")
    create_response = client.post("/schools", json=school_2.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    school_id_2 = create_response.json().get("school").get("id")

    inscription = InscriptionCreate(school_id=school_id, student_id=student_id)
    create_response = client.post("/inscriptions", json=inscription.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    inscription_2 = InscriptionCreate(school_id=school_id_2, student_id=student_id)
    create_response = client.post("/inscriptions", json=inscription_2.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/inscriptions/student/{student_id}")
    assert get_response.status_code == status.HTTP_200_OK
    response_json = get_response.json()
    assert response_json.get("inscriptions") is not None
    assert len(response_json.get("inscriptions")) == 2
    inscriptions = response_json.get("inscriptions")
    assert inscriptions[0].get("school_id") == school_id
    assert inscriptions[0].get("student_id") == student_id
    assert inscriptions[1].get("school_id") == school_id_2
    assert inscriptions[1].get("student_id") == student_id


def test_get_school_inscriptions(client: TestClient):
    student = StudentCreate(sid="TSTSTU00", first_name="Test", last_name="Student")
    create_response = client.post("/students", json=student.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    created_student = create_response.json().get("student")
    student_id = created_student.get("id")

    student_2 = StudentCreate(sid="TSTSTU01", first_name="Test", last_name="Student 2")
    create_response = client.post("/students", json=student_2.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    created_student_2 = create_response.json().get("student")
    student_id_2 = created_student_2.get("id")

    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_response = client.post("/schools", json=school.model_dump())
    assert create_response.status_code == status.HTTP_200_OK
    school_id = create_response.json().get("school").get("id")

    inscription = InscriptionCreate(school_id=school_id, student_id=student_id)
    create_response = client.post("/inscriptions", json=inscription.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    inscription_2 = InscriptionCreate(school_id=school_id, student_id=student_id_2)
    create_response = client.post("/inscriptions", json=inscription_2.model_dump())
    assert create_response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/inscriptions/school/{school_id}")
    assert get_response.status_code == status.HTTP_200_OK
    response_json = get_response.json()
    assert response_json.get("inscriptions") is not None
    assert len(response_json.get("inscriptions")) == 2
    inscriptions = response_json.get("inscriptions")
    assert inscriptions[0].get("school_id") == school_id
    assert inscriptions[0].get("student_id") == student_id
    assert inscriptions[1].get("school_id") == school_id
    assert inscriptions[1].get("student_id") == student_id_2
