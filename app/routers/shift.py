from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftOut

router = APIRouter(prefix="/shifts", tags=["shifts"])


@router.post("/", response_model=ShiftOut, status_code=201)
def create_shift(payload: ShiftCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == payload.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    shift = Shift(
        company_id=payload.company_id,
        name=payload.name,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/", response_model=list[ShiftOut])
def list_shifts(
    skip: int = 0,
    limit: int = 100,
    company_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Shift)
    if company_id is not None:
        query = query.filter(Shift.company_id == company_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{shift_id}", response_model=ShiftOut)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift
