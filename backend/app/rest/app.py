from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .router import router as rest_router

app = FastAPI(title="Mini Mattilda", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router, prefix="/v1")
