from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.db.cache import redis_connect, redis_disconnect
from app.db.db import create_db_and_tables
from app.resources.errors import ObjectAlreadyExistsException, ObjectNotFoundException
from app.rest.router import router as rest_router

app = FastAPI(title="Mini Mattilda", version="1.0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    redis_connect()
    yield
    redis_disconnect()


@app.exception_handler(ObjectAlreadyExistsException)
async def AlreadyExistsErrorHandler(
    request: Request, exc: ObjectAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": str(exc)},
    )


@app.exception_handler(ObjectNotFoundException)
async def ObjectNotFoundExceptionHandler(
    request: Request, exc: ObjectNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router)
