from typing import Sequence
from sqlalchemy import Boolean
from sqlmodel import Session, select, func

from app.models import Inscription, Invoice, School, SchoolCreate, SchoolUpdate, Student
from app.resources.errors import ObjectAlreadyExistsException, ObjectNotFoundException


def create_school(*, session: Session, create_school: SchoolCreate) -> School:
    school_validated = School.model_validate(create_school)

    # Check if school already exists
    query_existing = select(School).where(
        (School.sid == school_validated.sid) | (School.name == school_validated.name)
    )
    existing_school = session.exec(query_existing).first()
    if existing_school:
        raise ObjectAlreadyExistsException(
            f"School already exists: {school_validated.name}, {school_validated.sid}"
        )

    # Create new school
    session.add(school_validated)
    session.commit()
    session.refresh(school_validated)
    return school_validated


def get_schools(*, session: Session, skip: int = 0, limit: int = 100):
    query = select(School).order_by("created_at").offset(skip).limit(limit)
    schools = session.exec(query).all()
    count_query = select(func.count()).select_from(School)
    count = session.exec(count_query).one()
    return schools, count


def get_school_by_id(*, session: Session, school_id: int) -> School:
    query = select(School).where(School.id == school_id)
    school = session.exec(query).first()
    if not school:
        raise ObjectNotFoundException(f"School not found: {school_id}")
    return school


def update_school(
    *, session: Session, school_in: SchoolUpdate, school_id: int
) -> School:
    query = select(School).where(School.id == school_id)
    school = session.exec(query).first()
    if not school:
        raise ObjectNotFoundException(f"School not found: {school_id}")

    school_update = school_in.model_dump(exclude_unset=True)
    school.sqlmodel_update(school_update)
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


def delete_school(*, session: Session, school_id: int) -> bool:
    query = select(School).where(School.id == school_id)
    school = session.exec(query).first()
    if not school:
        raise ObjectNotFoundException(f"School not found: {school_id}")
    session.delete(school)
    session.commit()
    return True


# TODO: update to allow date range
def get_school_statement(*, session: Session, school_id: int) -> dict:
    # Get school
    school = get_school_by_id(session=session, school_id=school_id)

    # Get inscriptions
    query = select(Inscription).where(Inscription.school_id == school_id)
    inscriptions = session.exec(query).all()

    # Get students
    students = []
    for inscription in inscriptions:
        query = select(Student).where(Student.id == inscription.student_id)
        student = session.exec(query).first()
        students.append(student)

    # Get invoices
    query = select(Invoice).where(Invoice.school_id == school_id)
    invoices = session.exec(query).all()

    # Paid invoices total
    paid_invoices = [invoice for invoice in invoices if invoice.status == "paid"]

    # Unpaid invoices total
    unpaid_invoices = [invoice for invoice in invoices if invoice.status == "unpaid"]

    return {
        "school": school,
        "students": students,
        "invoices": invoices,
        "paid_invoices": paid_invoices,
        "unpaid_invoices": unpaid_invoices,
    }
