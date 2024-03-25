from pydantic import BaseModel


class Student(BaseModel):
    id: int
    firstName: str
    lastName: str
    birthDate: str
