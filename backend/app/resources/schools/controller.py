import pickle

from fastapi import APIRouter

from app.models import SchoolCreate, SchoolUpdate
from app.resources.schools import service
from app.rest.deps import CacheDep, SessionDep

router = APIRouter(tags=["Schools"])


@router.get("/", name="GET all schools")
def get_all_schools(
    session: SessionDep, cache: CacheDep, skip: int = 0, limit: int = 100
):
    cache_key = f"get_schools:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    schools, count = service.get_schools(session=session, skip=skip, limit=limit)
    response = {"schools": schools, "count": count}
    cache.set(cache_key, pickle.dumps(response))
    return response


@router.get("/{school_id}", name="GET school by ID")
def get_school(session: SessionDep, cache: CacheDep, school_id: int):
    cache_key = f"get_school:{school_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    school = service.get_school_by_id(session=session, school_id=school_id)
    response = {"school": school}

    cache.set(cache_key, pickle.dumps(response))
    return {"school": school}


@router.post("/", name="Create a new school")
def create_new_school(session: SessionDep, cache: CacheDep, school: SchoolCreate):
    new_school = service.create_school(session=session, create_school=school)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_schools*"):
        cache_pipe.delete(key)
    cache_pipe.execute()
    return {"message": "School created", "school": new_school}


@router.put("/{school_id}")
def update_school_by_id(
    session: SessionDep, cache: CacheDep, school_id: int, school: SchoolUpdate
):
    cache_key = f"get_school:{school_id}"
    updated_school = service.update_school(
        session=session, school_in=school, school_id=school_id
    )
    cache.delete(cache_key)
    return {
        "message": "School updated successfully",
        "updated_school": updated_school,
    }


@router.delete("/{school_id}")
def delete_school(session: SessionDep, cache: CacheDep, school_id: int):
    service.delete_school(session=session, school_id=school_id)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_schools*"):
        cache_pipe.delete(key)
    cache_pipe.delete(f"get_school:{school_id}")
    cache_pipe.execute()
    return {"message": f"School deleted {school_id}"}


@router.get("/{school_id}/account-statement")
def get_schools_statement_report(session: SessionDep, cache: CacheDep, school_id: int):
    cache_key = f"get_school_statement:{school_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    statement = service.get_school_statement(session=session, school_id=school_id)
    response = {"statement": statement}
    cache.set(cache_key, pickle.dumps(response))
    return response
