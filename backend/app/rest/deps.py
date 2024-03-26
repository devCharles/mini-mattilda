from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlmodel import Session
from app.db.db import get_db_session
from app.db.cache import get_redis_client


SessionDep = Annotated[Session, Depends(get_db_session)]

CacheDep = Annotated[Redis, Depends(get_redis_client)]
