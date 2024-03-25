from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class SchoolBase(SQLModel):
    name: str = Field(index=True)
    sid: str = Field(
        default=None, unique=True, index=True
    )  # School ID for internal recognition purposes
    address: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    zip_code: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)


class SchoolCreate(SchoolBase, table=True):
    pass


class SchoolOut(SchoolBase):
    """
    I usually prefer to use UUID for id
    because its helps to avoid some security and scalability issues
    but let's keep it simple for this project and use int
    """

    id: int | None = Field(default=None, primary_key=True)
