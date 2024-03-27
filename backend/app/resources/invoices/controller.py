import pickle

from fastapi import APIRouter

from app.models import InvoiceUpdate
from app.resources.invoices import service
from app.rest.deps import CacheDep, SessionDep

router = APIRouter(tags=["Invoices"])


@router.get("/", name="GET all invoices")
def get_invoices(session: SessionDep, cache: CacheDep, skip: int = 0, limit: int = 100):
    cache_key = f"get_invoices:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    invoices, count = service.get_invoices(session=session, skip=skip, limit=limit)
    response = {"invoices": invoices, "count": count}
    cache.set(cache_key, pickle.dumps(response))
    return response


@router.get("/{invoice_id}", name="GET invoice by ID")
def get_invoice(session: SessionDep, cache: CacheDep, invoice_id: int):
    cache_key = f"get_invoice:{invoice_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    invoice = service.get_invoice_by_id(session=session, invoice_id=invoice_id)
    response = {"invoice": invoice}

    cache.set(cache_key, pickle.dumps(response))
    return {"invoice": invoice}


@router.get("/student/{student_id}", name="GET invoices by student ID")
def get_invoice_by_student_id(
    session: SessionDep,
    cache: CacheDep,
    student_id: int,
    skip: int = 0,
    limit: int = 100,
):
    cache_key = f"get_invoices:student_id:{student_id}:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    invoice = service.get_invoice_by_student_id(
        session=session, student_id=student_id, skip=skip, limit=limit
    )
    response = {"invoice": invoice}

    cache.set(cache_key, pickle.dumps(response))
    return {"invoice": invoice}


@router.get("/school/{school_id}", name="GET invoices by school ID")
def get_invoice_by_school_id(
    session: SessionDep,
    cache: CacheDep,
    school_id: int,
    skip: int = 0,
    limit: int = 100,
):
    cache_key = f"get_invoices:school_id:{school_id}:skip:{skip}:limit:{limit}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return pickle.loads(cached_response)

    invoice = service.get_invoice_by_school_id(
        session=session, school_id=school_id, skip=skip, limit=limit
    )
    response = {"invoice": invoice}

    cache.set(cache_key, pickle.dumps(response))
    return {"invoice": invoice}


@router.post("/", name="Create a new invoice")
def create_invoice(
    session: SessionDep, cache: CacheDep, invoice: service.InvoiceCreate
):
    new_invoice = service.create_invoice(session=session, create_invoice=invoice)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_invoices*"):
        cache_pipe.delete(key)
    cache_pipe.execute()
    return {"message": "Invoice created", "invoice": new_invoice}


@router.put("/{invoice_id}")
def update_invoice(
    session: SessionDep, cache: CacheDep, invoice_id: int, invoice: InvoiceUpdate
):
    cache_key = f"get_invoice:{invoice_id}"
    updated_invoice = service.update_invoice(
        session=session, invoice_in=invoice, invoice_id=invoice_id
    )
    cache.delete(cache_key)

    return {
        "message": "Invoice updated successfully",
        "updated_invoice": updated_invoice,
    }


@router.delete("/{invoice_id}")
def delete_invoice(session: SessionDep, cache: CacheDep, invoice_id: int):
    service.delete_invoice(session=session, invoice_id=invoice_id)
    cache_pipe = cache.pipeline()
    for key in cache.keys("get_invoices*"):
        cache_pipe.delete(key)
    cache_pipe.delete(f"get_invoice:{invoice_id}")
    cache_pipe.execute()
    return {"message": f"Invoice deleted {invoice_id}"}
