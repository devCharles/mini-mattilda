from sqlmodel import Session, select, func
from app.models import Student
from app.resources.errors import ObjectAlreadyExistsException, ObjectNotFoundException


def crete_student(*, session: Session, student: Student) -> Student:
    # Check if student already exists
    query_existing = select(Student).where(
        (Student.name == student.name) & (Student.email == student.email)
    )
    existing_student = session.exec(query_existing).first()
    if existing_student:
        raise ObjectAlreadyExistsException(
            f"Student already exists: {student.name}, {student.email}"
        )

    # Create new student
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def get_students(*, session: Session, skip: int = 0, limit: int = 100):
    query = select(Student).offset(skip).limit(limit)
    students = session.exec(query).all()
    count_query = select(func.count()).select_from(Student)
    count = session.exec(count_query).one()
    return students, count


def get_student_by_id(*, session: Session, student_id: int) -> Student:
    query = select(Student).where(Student.id == student_id)
    student = session.exec(query).first()
    if not student:
        raise ObjectNotFoundException(f"Student not found: {student_id}")
    return student


def update_student(
    *, session: Session, student_in: Student, student_id: int
) -> Student:
    query = select(Student).where(Student.id == student_id)
    student = session.exec(query).first()
    if not student:
        raise ObjectNotFoundException(f"Student not found: {student_id}")

    student_update = student_in.model_dump(exclude_unset=True)
    student.sqlmodel_update(student_update)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def delete_student(*, session: Session, student_id: int) -> bool:
    query = select(Student).where(Student.id == student_id)
    student = session.exec(query).first()
    if not student:
        raise ObjectNotFoundException(f"Student not found: {student_id}")

    session.delete(student)
    session.commit()
    return True


def get_student_statement(*, session: Session, student_id: int):
    query = select(Student).where(Student.id == student_id)
    student = session.exec(query).first()
    if not student:
        raise ObjectNotFoundException(f"Student not found: {student_id}")

    # Student's invoices unpaid
    unpaid_invoices = filter(
        lambda invoice: invoice.status == "unpaid", student.invoices
    )

    # Student's invoices paid
    paid_invoices = filter(lambda invoice: invoice.status == "paid", student.invoices)

    return {
        "student": student,
        "unpaid_invoices": unpaid_invoices,
        "paid_invoices": paid_invoices,
    }
