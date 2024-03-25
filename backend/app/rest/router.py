from email import message

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from resources.invoices import controller as invoices_router
from resources.schools import controller as schools_router
from resources.students import controller as students_router

router = APIRouter()

router.include_router(schools_router.router, prefix="/schools")
router.include_router(students_router.router, prefix="/students")
router.include_router(invoices_router.router, prefix="/invoices")


@router.get("/", name="Root", tags=["Root"])
def root():
    return JSONResponse(
        content={message: "Mini Mattilda API"},
        status_code=200,
    )
