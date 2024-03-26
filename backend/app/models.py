"""
This file contains all the data Models
This is a single file to keep everything simple and to not have to worry about circular imports
With more time and a bigger project, I would have split this into multiple files
"""

import enum
import datetime
import pendulum
from typing import Optional
from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel


# Enums
class InvoiceStatus(str, enum.Enum):
    unpaid = "unpaid"
    paid = "paid"
    cancelled = "cancelled"


class InscriptionStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


# School Models
class SchoolBase(SQLModel):
    name: str | None = Field(index=True)
    sid: str | None = Field(
        unique=True, index=True
    )  # School ID for internal recognition purposes
    address: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    zip_code: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)


class SchoolCreate(SchoolBase):
    name: str | None = Field(nullable=True)
    pass


class School(SchoolBase, table=True):
    """
    I usually prefer to use UUID for id
    because its helps to avoid some security and scalability issues
    but let's keep it simple for this project and use int
    """

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    # Relationships
    inscriptions: list["Inscription"] = Relationship(back_populates="school")
    invoices: list["Invoice"] = Relationship(back_populates="school")


class SchoolUpdate(SchoolBase):
    name: str | None = None
    sid: str | None = None


# Student Models


class StudentBase(SQLModel):
    first_name: str = Field()
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    sid: str = Field(
        default=None, unique=True, index=True
    )  # Student ID for internal recognition purposes


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    sid: str | None = None


class Student(StudentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    # Relationships
    inscriptions: list["Inscription"] = Relationship(back_populates="student")
    invoices: list["Invoice"] = Relationship(back_populates="student")


# Invoice Models


class InvoiceBase(SQLModel):
    amount: float
    date: datetime.datetime = Field(default_factory=pendulum.now)
    due_date: datetime.datetime = Field(
        default_factory=lambda: pendulum.now().add(days=30)
    )
    description: Optional[str] = Field(default=None)
    school_id: int = Field(foreign_key="school.id")
    student_id: int = Field(foreign_key="student.id")


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: InvoiceStatus = Field(
        sa_column=Column(Enum(InvoiceStatus)), default=InvoiceStatus.unpaid
    )
    created_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    # Relationships
    student: "Student" = Relationship(back_populates="invoices")
    school: "School" = Relationship(back_populates="invoices")


# Inscription Schools <-> Student relationship model
class InscriptionBase(SQLModel):
    student_id: int = Field(foreign_key="student.id")
    school_id: int = Field(foreign_key="school.id")


class InscriptionCreate(InscriptionBase):
    pass


class Inscription(InscriptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: InscriptionStatus = Field(
        sa_column=Column(Enum(InscriptionStatus)), default=InscriptionStatus.active
    )
    created_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    updated_at: datetime.datetime = Field(default_factory=pendulum.now, nullable=False)
    # Relationships
    student: "Student" = Relationship(back_populates="inscriptions")
    school: "School" = Relationship(back_populates="inscriptions")
