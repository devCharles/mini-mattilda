import os
from sqlmodel import SQLModel, create_engine, Session
import app.models  # imported to load the models

db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "abcde")
db_name = os.getenv("POSTGRES_DB", "postgres")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_host = os.getenv("POSTGRES_HOST", "postgres")

# engine = create_engine(url="postgresql://postgres:abcde@postgres:5432/postgres")
engine = create_engine(
    url=f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


def create_db_and_tables():
    from app.db.db import engine

    SQLModel.metadata.create_all(engine, checkfirst=True)


def get_db_session():
    with Session(engine) as session:
        yield session
