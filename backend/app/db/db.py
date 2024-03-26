from sqlmodel import SQLModel, create_engine, Session
import app.models  # imported to load the models

engine = create_engine(url="postgresql://postgres:abcde@postgres:5432/postgres")


def create_db_and_tables():
    from app.db.db import engine

    SQLModel.metadata.create_all(engine, checkfirst=True)


def get_db_session():
    with Session(engine) as session:
        yield session
