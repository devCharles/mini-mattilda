from turtle import update
from sqlmodel import Session, select
from app.models import Invoice, InvoiceCreate
from app.models import InvoiceCreate
from app.resources.errors import ObjectNotFoundException


def create_invoice(*, session: Session, create_invoice: InvoiceCreate):
    invoice_db_obj = Invoice.model_validate(create_invoice)
    session.add(invoice_db_obj)
    session.commit()
    session.refresh(invoice_db_obj)
    return invoice_db_obj


def get_invoices(*, session: Session):
    query = select(Invoice).order_by("created_at")
    invoices = session.exec(query).all()
    return invoices


def get_invoice_by_id(*, session: Session, invoice_id: int):
    query = select(Invoice).where(Invoice.id == invoice_id)
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    return invoice


def update_invoice(*, session: Session, invoice_in: InvoiceCreate) -> Invoice | None:
    query = select(Invoice).where(Invoice.id == invoice_in.id)
    invoice = session.exec(query).first()
    if not invoice:
        raise ObjectNotFoundException("Invoice not found")
    invoice_in_validated = Invoice.model_validate(invoice_in)
    invoice(update=invoice_in_validated)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice
