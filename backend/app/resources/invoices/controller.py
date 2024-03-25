from fastapi import APIRouter

router = APIRouter(tags=["Invoices"])


# TODO: Implement
@router.get("/", name="GET all invoices")
def get_invoices():
    return {"invoices": []}


# TODO: Implement
@router.get("/{invoice_id}", name="GET invoice by ID")
def get_invoice(invoice_id: int):
    return {"invoice_id": invoice_id}


# TODO: Implement
@router.post("/", name="Create a new invoice")
def create_invoice():
    return {"message": "Invoice created"}


# TODO: Implement
@router.put("/{invoice_id}")
def update_invoice(invoice_id: int):
    return {"message": "Invoice updated"}


# TODO: Implement
@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int):
    return {"message": "Invoice deleted"}
