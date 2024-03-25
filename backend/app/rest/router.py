from email import message

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from resources.schools.controller import router as schools_router
from resources.invoices.controller import router as invoices_router
from resources.students.controller import router as students_router

router = APIRouter()

router.include_router(schools_router, prefix="/schools")
router.include_router(students_router, prefix="/students")
router.include_router(invoices_router, prefix="/invoices")


@router.get("/", name="Root", tags=["Root"])
def root():
    return JSONResponse(
        content={"message": "Mini Mattilda API"},
        status_code=200,
    )
