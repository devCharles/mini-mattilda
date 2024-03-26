import pickle
from fastapi import APIRouter

from app.models import InscriptionCreate, InscriptionUpdate, InscriptionCreate
from app.rest.deps import CacheDep, SessionDep
from app.resources.inscriptions import service

router = APIRouter(tags=["Inscriptions"])


@router.get("/", name="GET all inscriptions")
def get_all_inscriptions(
    session: SessionDep, cache: CacheDep, skip: int = 0, limit: int = 100
):
    cache_key = f"get_inscriptions:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return pickle.loads(cached_response)

    inscriptions, count = service.get_inscriptions(
        session=session, skip=skip, limit=limit
    )

    response = {"inscriptions": inscriptions, "count": count}

    cache.set(cache_key, pickle.dumps(response))

    return response


@router.get("/{inscription_id}", name="GET inscription by ID")
def get_inscription(session: SessionDep, cache: CacheDep, inscription_id: int):
    cache_key = f"get_inscription:{inscription_id}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return pickle.loads(cached_response)

    inscription = service.get_inscription_by_id(
        session=session, inscription_id=inscription_id
    )

    response = {"inscription": inscription}

    cache.set(cache_key, pickle.dumps(response))

    return {"inscription": inscription}


@router.get("/student/{student_id}", name="GET inscriptions by student ID")
def get_inscriptions_by_student_id(
    session: SessionDep,
    cache: CacheDep,
    student_id: int,
    skip: int = 0,
    limit: int = 100,
):
    cache_key = f"get_inscriptions_by_student_id:{student_id}:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return pickle.loads(cached_response)

    inscriptions, count = service.get_inscriptions_by_student_id(
        session=session, student_id=student_id, skip=skip, limit=limit
    )

    response = {"inscriptions": inscriptions, "count": count}

    cache.set(cache_key, pickle.dumps(response))

    return response


@router.get("/school/{school_id}", name="GET inscriptions by school ID")
def get_inscriptions_by_school_id(
    session: SessionDep,
    cache: CacheDep,
    school_id: int,
    skip: int = 0,
    limit: int = 100,
):
    cache_key = f"get_inscriptions_by_school_id:{school_id}:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return pickle.loads(cached_response)

    inscriptions, count = service.get_inscriptions_by_school_id(
        session=session, school_id=school_id, skip=skip, limit=limit
    )

    response = {"inscriptions": inscriptions, "count": count}

    cache.set(cache_key, pickle.dumps(response))

    return response


@router.post("/", name="Create a new inscription")
def create_new_inscription(
    session: SessionDep, cache: CacheDep, inscription: InscriptionCreate
):
    new_inscription = service.create_new_inscription(
        session=session, create_inscription=inscription
    )

    cache_pipe = cache.pipeline()
    for key in cache.keys("get_inscriptions*"):
        cache_pipe.delete(key)
    for key in cache.keys("get_student_statement*"):
        cache_pipe.delete(key)
    cache_pipe.execute()

    return {"message": "Inscription created", "inscription": new_inscription}


@router.put("/{inscription_id}", name="Update inscription by ID")
def update_inscription_by_id(
    session: SessionDep,
    cache: CacheDep,
    inscription_id: int,
    inscription: InscriptionUpdate,
):
    cache_key = f"get_inscription:{inscription_id}"
    updated_inscription = service.update_inscription(
        session=session, inscription_in=inscription, inscription_id=inscription_id
    )

    cache.delete(cache_key)

    return {
        "message": "Inscription updated successfully",
        "updated_inscription": updated_inscription,
    }


@router.delete("/{inscription_id}", name="Delete inscription by ID")
def delete_inscription_by_id(session: SessionDep, cache: CacheDep, inscription_id: int):
    service.delete_inscription(session=session, inscription_id=inscription_id)

    cache_pipe = cache.pipeline()
    for key in cache.keys("get_inscriptions*"):
        cache_pipe.delete(key)
    for key in cache.keys("get_student_statement*"):
        cache_pipe.delete(key)
    cache_pipe.delete(f"get_inscription:{inscription_id}")
    cache_pipe.execute()

    return {"message": f"Inscription {inscription_id} deleted"}
