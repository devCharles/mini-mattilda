from sqlmodel import SQLModel, create_engine

engine = create_engine(url="postgresql://postgres:password@localhost:5432/minimattilda")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
