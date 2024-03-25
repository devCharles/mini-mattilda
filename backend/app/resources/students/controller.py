from fastapi import APIRouter

router = APIRouter(tags=["Students"])


# TODO: Implement
@router.get("/", name="GET all students")
def get_students():
    return {"students": []}


# TODO: Implement
@router.get("/{student_id}", name="GET student by ID")
def get_student(student_id: int):
    return {"student_id": student_id}


# TODO: Implement
@router.post("/", name="Create a new student")
def create_student():
    return {"message": "Student created"}


# TODO: Implement
@router.put("/{student_id}")
def update_student(student_id: int):
    return {"message": "Student updated"}


# TODO: Implement
@router.delete("/{student_id}")
def delete_student(student_id: int):
    return {"message": "Student deleted"}


# TODO Implement
@router.get("/status-report")
def get_account_status_report():
    return {"message": "Account status report"}
