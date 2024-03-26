from sqlmodel import Session, func, select

from app.models import Inscription, InscriptionCreate
from app.resources.errors import ObjectAlreadyExistsException, ObjectNotFoundException


def create_new_inscription(
    *, session: Session, create_inscription: InscriptionCreate
) -> Inscription:
    inscription = Inscription.model_validate(create_inscription)

    existing_inscription_query = select(Inscription).where(
        (Inscription.student_id == inscription.student_id)
        & (Inscription.school_id == inscription.school_id)
    )

    existing_inscription = session.exec(existing_inscription_query).first()

    if existing_inscription:
        raise ObjectAlreadyExistsException(
            f"Inscription already exists: {inscription.student_id}, {inscription.school_id}"
        )

    session.add(inscription)
    session.commit()
    session.refresh(inscription)
    return inscription


def get_inscriptions(*, session: Session, skip: int = 0, limit: int = 100):
    query = select(Inscription).order_by("created_at").offset(skip).limit(limit)
    inscriptions = session.exec(query).all()

    count_query = select(func.count()).select_from(Inscription)
    count = session.exec(count_query).one()

    return inscriptions, count


def get_inscription_by_id(*, session: Session, inscription_id: int) -> Inscription:
    query = select(Inscription).where(Inscription.id == inscription_id)
    inscription = session.exec(query).first()

    if not inscription:
        raise ObjectNotFoundException(f"Inscription not found: {inscription_id}")

    return inscription


def get_inscriptions_by_student_id(
    *, session: Session, student_id: int, skip: int = 0, limit: int = 100
):
    query = (
        select(Inscription)
        .where(Inscription.student_id == student_id)
        .order_by("created_at")
        .offset(skip)
        .limit(limit)
    )
    inscriptions = session.exec(query).all()

    count_query = (
        select(func.count())
        .where(Inscription.student_id == student_id)
        .select_from(Inscription)
    )
    count = session.exec(count_query).one()

    return inscriptions, count


def get_inscriptions_by_school_id(
    *, session: Session, school_id: int, skip: int = 0, limit: int = 100
):
    query = (
        select(Inscription)
        .where(Inscription.school_id == school_id)
        .order_by("created_at")
        .offset(skip)
        .limit(limit)
    )
    inscriptions = session.exec(query).all()

    count_query = (
        select(func.count())
        .where(Inscription.school_id == school_id)
        .select_from(Inscription)
    )
    count = session.exec(count_query).one()

    return inscriptions, count


def update_inscription(
    *, session: Session, inscription_in: InscriptionCreate, inscription_id: int
) -> Inscription:
    query = select(Inscription).where(Inscription.id == inscription_id)
    inscription = session.exec(query).first()

    if not inscription:
        raise ObjectNotFoundException(f"Inscription not found: {inscription_id}")

    inscription_update = inscription_in.model_dump(exclude_unset=True)
    inscription.sqlmodel_update(inscription_update)

    session.add(inscription)
    session.commit()
    session.refresh(inscription)

    return inscription


def delete_inscription(*, session: Session, inscription_id: int) -> bool:
    query = select(Inscription).where(Inscription.id == inscription_id)
    inscription = session.exec(query).first()

    if not inscription:
        raise ObjectNotFoundException(f"Inscription not found: {inscription_id}")

    session.delete(inscription)
    session.commit()

    return True
