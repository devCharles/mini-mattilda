from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlmodel import Session

from app.db.cache import get_redis_client
from app.db.db import get_db_session

SessionDep = Annotated[Session, Depends(get_db_session)]

CacheDep = Annotated[Redis, Depends(get_redis_client)]
