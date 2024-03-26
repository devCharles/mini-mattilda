from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.rest.router import router as rest_router
from app.db.db import create_db_and_tables

app = FastAPI(title="Mini Mattilda", version="1.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router)
