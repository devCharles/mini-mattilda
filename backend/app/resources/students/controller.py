import pickle

from fastapi import APIRouter
from sqlalchemy import delete

from app.models import StudentCreate, StudentUpdate
from app.resources.students import service
from app.rest.deps import CacheDep, SessionDep

router = APIRouter(tags=["Students"])


@router.get("/", name="GET all students")
def get_students(session: SessionDep, cache: CacheDep, skip: int = 0, limit: int = 100):
    cache_key = f"get_students:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    students, count = service.get_students(session=session, skip=skip, limit=limit)
    response = {"students": students, "count": count}
    cache.set(cache_key, pickle.dumps(response))
    return response


@router.get("/{student_id}", name="GET student by ID")
def get_student(student_id: int, session: SessionDep, cache: CacheDep):
    cache_key = f"get_student:{student_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    student = service.get_student_by_id(session=session, student_id=student_id)
    response = {"student": student}

    cache.set(cache_key, pickle.dumps(response))
    return {"student": student}


@router.post("/", name="Create a new student")
def create_student(session: SessionDep, cache: CacheDep, student: StudentCreate):
    new_student = service.create_student(session=session, student=student)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_students*"):
        cache_pipe.delete(key)
    cache_pipe.execute()
    return {"message": "Student created", "student": new_student}


@router.put("/{student_id}")
def update_student_by_id(
    session: SessionDep, cache: CacheDep, student_id: int, student: StudentUpdate
):
    cache_key = f"get_student:{student_id}"
    updated_student = service.update_student(
        session=session, student_in=student, student_id=student_id
    )
    cache.delete(cache_key)
    return {
        "message": "Student updated successfully",
        "updated_student": updated_student,
    }


@router.delete("/{student_id}")
def delete_student(session: SessionDep, cache: CacheDep, student_id: int):
    service.delete_student(session=session, student_id=student_id)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_students*"):
        cache_pipe.delete(key)
    cache_pipe.delete(f"get_student:{student_id}")
    cache_pipe.execute()
    return {"message": f"Student {student_id} deleted"}


@router.get("/{student_id}/statement")
def get_student_statement(session: SessionDep, cache: CacheDep, student_id: int):
    cache_key = f"get_student_statement:{student_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    statement = service.get_student_statement(session=session, student_id=student_id)
    response = {"statement": statement}
    cache.set(cache_key, pickle.dumps(response))
    return response
