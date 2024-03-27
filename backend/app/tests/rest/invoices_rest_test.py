from fastapi import status
from app.models import InvoiceCreate, SchoolCreate, StudentCreate
from fastapi.testclient import TestClient


def test_full_invoice_life_cycle(client: TestClient):
    # Student
    student = StudentCreate(first_name="Test", last_name="Student", sid="TSTSTU00")
    create_student_response = client.post("/students", json=student.model_dump())
    assert create_student_response.status_code == status.HTTP_200_OK
    student_id = create_student_response.json().get("student").get("id")

    # School
    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_school_response = client.post("/schools", json=school.model_dump())
    assert create_school_response.status_code == status.HTTP_200_OK
    school_id = create_school_response.json().get("school").get("id")

    # Create
    invoice = InvoiceCreate(
        amount=100, student_id=student_id, school_id=school_id, description="Test"
    )
    create_response = client.post(
        "/invoices",
        json={
            "amount": invoice.amount,
            "student_id": invoice.student_id,
            "school_id": invoice.school_id,
            "description": invoice.description,
        },
    )
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()

    # Read
    get_response = client.get(f"/invoices/{response_json.get('invoice').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("invoice") is not None
    assert get_response.json().get("invoice").get("amount") == invoice.amount

    # Update
    new_amount = 200
    update_response = client.put(
        f"/invoices/{response_json.get('invoice').get('id')}",
        json={"amount": new_amount},
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json().get("updated_invoice") is not None
    assert update_response.json().get("updated_invoice").get("amount") == new_amount

    # Validate Update
    get_response = client.get(f"/invoices/{response_json.get('invoice').get('id')}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json().get("invoice") is not None
    assert get_response.json().get("invoice").get("amount") == new_amount

    # Delete
    delete_response = client.delete(
        f"/invoices/{response_json.get('invoice').get('id')}"
    )
    assert delete_response.status_code == status.HTTP_200_OK

    # Validate Delete
    get_response = client.get(f"/invoices/{response_json.get('invoice').get('id')}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_not_create_invoice_with_invalid_student(client: TestClient):
    # School
    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_school_response = client.post("/schools", json=school.model_dump())
    assert create_school_response.status_code == status.HTTP_200_OK
    school_id = create_school_response.json().get("school").get("id")

    # Create
    invoice = InvoiceCreate(
        amount=100, student_id=9999, school_id=school_id, description="Test"
    )
    create_response = client.post(
        "/invoices",
        json={
            "amount": invoice.amount,
            "student_id": invoice.student_id,
            "school_id": invoice.school_id,
            "description": invoice.description,
        },
    )
    assert create_response.status_code == status.HTTP_404_NOT_FOUND


def test_not_create_invoice_with_invalid_school(client: TestClient):
    # Student
    student = StudentCreate(first_name="Test", last_name="Student", sid="TSTSTU00")
    create_student_response = client.post("/students", json=student.model_dump())
    assert create_student_response.status_code == status.HTTP_200_OK
    student_id = create_student_response.json().get("student").get("id")

    # Create
    invoice = InvoiceCreate(
        amount=100, student_id=student_id, school_id=9999, description="Test"
    )
    create_response = client.post(
        "/invoices",
        json={
            "amount": invoice.amount,
            "student_id": invoice.student_id,
            "school_id": invoice.school_id,
            "description": invoice.description,
        },
    )
    assert create_response.status_code == status.HTTP_404_NOT_FOUND


def test_invoice_unpaid_by_default(client: TestClient):
    # Student
    student = StudentCreate(first_name="Test", last_name="Student", sid="TSTSTU00")
    create_student_response = client.post("/students", json=student.model_dump())
    assert create_student_response.status_code == status.HTTP_200_OK
    student_id = create_student_response.json().get("student").get("id")

    # School
    school = SchoolCreate(sid="TSTSCH00", name="Test School")
    create_school_response = client.post("/schools", json=school.model_dump())
    assert create_school_response.status_code == status.HTTP_200_OK
    school_id = create_school_response.json().get("school").get("id")

    # Create
    invoice = InvoiceCreate(
        amount=100, student_id=student_id, school_id=school_id, description="Test"
    )
    create_response = client.post(
        "/invoices",
        json={
            "amount": invoice.amount,
            "student_id": invoice.student_id,
            "school_id": invoice.school_id,
            "description": invoice.description,
        },
    )
    assert create_response.status_code == status.HTTP_200_OK
    response_json = create_response.json()
    assert response_json.get("invoice").get("status") == "unpaid"
