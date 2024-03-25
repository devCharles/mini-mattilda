from fastapi import APIRouter

router = APIRouter(tags=["Schools"])


# TODO: Implement
@router.get("/", name="GET all schools")
def get_schools():
    return {"schools": []}


# TODO: Implement
@router.get("/{school_id}", name="GET school by ID")
def get_school(school_id: int):
    return {"school_id": school_id}


# TODO: Implement
@router.post("/", name="Create a new school")
def create_school():
    return {"message": "School created"}


# TODO: Implement
@router.put("/{school_id}")
def update_school(school_id: int):
    return {"message": "School updated"}


# TODO: Implement
@router.delete("/{school_id}")
def delete_school(school_id: int):
    return {"message": "School deleted"}


# TODO Implement
@router.get("/status-report")
def get_schools_status_report():
    return {"message": "Schools status report"}
