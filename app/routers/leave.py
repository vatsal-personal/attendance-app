from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.employee import Employee
from app.models.leave import Leave, LeaveStatusEnum
from app.schemas.leave import LeaveCreate, LeaveOut

router = APIRouter(prefix="/leaves", tags=["leaves"])


@router.post("/", response_model=LeaveOut, status_code=201)
def create_leave(payload: LeaveCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    leave = Leave(
        employee_id=payload.employee_id,
        date=payload.date,
        reason=payload.reason,
        status=LeaveStatusEnum.PENDING,
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.get("/", response_model=list[LeaveOut])
def list_leaves(
    skip: int = 0,
    limit: int = 100,
    employee_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Leave)
    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{leave_id}", response_model=LeaveOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave
