from sqlmodel import Session, func, select

from app.models import Invoice, InvoiceCreate, InvoiceUpdate, School, Student
from app.resources.errors import ObjectNotFoundException


def create_invoice(*, session: Session, create_invoice: InvoiceCreate) -> Invoice:
    invoice_validated = Invoice.model_validate(create_invoice)

    student_query = select(Student).where(Student.id == invoice_validated.student_id)
    student = session.exec(student_query).first()
    if not student:
        raise ObjectNotFoundException("Student not found")

    school_query = select(School).where(School.id == invoice_validated.school_id)
    school = session.exec(school_query).first()
    if not school:
        raise ObjectNotFoundException("School not found")

    session.add(invoice_validated)
    session.commit()
    session.refresh(invoice_validated)
    return invoice_validated


def get_invoices(*, session: Session, skip: int = 0, limit: int = 100):
    query = select(Invoice).order_by("created_at").offset(skip).limit(limit)
    invoices = session.exec(query).all()
    count_query = select(func.count()).select_from(Invoice)
    count = session.exec(count_query).one()
    return invoices, count


def get_invoice_by_id(*, session: Session, invoice_id: int) -> Invoice | None:
    query = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    return invoice


def get_invoice_by_school_id(
    *, session: Session, school_id: int, skip: int = 0, limit: int = 100
) -> Invoice | None:
    query = (
        select(Invoice).where(Invoice.school_id == school_id).offset(skip).limit(limit)
    )
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    return invoice


def get_invoice_by_student_id(
    *, session: Session, student_id: int, skip: int = 0, limit: int = 100
) -> Invoice | None:
    query = (
        select(Invoice)
        .where(Invoice.student_id == student_id)
        .offset(skip)
        .limit(limit)
    )
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    return invoice


def update_invoice(
    *, session: Session, invoice_in: InvoiceUpdate, invoice_id: int
) -> Invoice | None:
    query = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")

    invoice_update = invoice_in.model_dump(exclude_unset=True)
    invoice.sqlmodel_update(invoice_update)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


def delete_invoice(*, session: Session, invoice_id: int) -> bool:
    query = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    session.delete(invoice)
    session.commit()
    return True
