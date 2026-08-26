from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.employee import Employee
from app.models.attendance_log import AttendanceLog
from app.schemas.attendance_log import AttendanceLogCreate, AttendanceLogOut

router = APIRouter(prefix="/attendance-logs", tags=["attendance_logs"])


@router.post("/", response_model=AttendanceLogOut, status_code=201)
def create_attendance_log(payload: AttendanceLogCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    log = AttendanceLog(
        employee_id=payload.employee_id,
        direction=payload.direction,
        device_id=payload.device_id,
        source=payload.source,
        timestamp=payload.timestamp or datetime.now(timezone.utc),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/", response_model=list[AttendanceLogOut])
def list_attendance_logs(
    skip: int = 0,
    limit: int = 100,
    employee_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(AttendanceLog)
    if employee_id is not None:
        query = query.filter(AttendanceLog.employee_id == employee_id)
    return query.order_by(AttendanceLog.timestamp.desc()).offset(skip).limit(limit).all()


@router.get("/{log_id}", response_model=AttendanceLogOut)
def get_attendance_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AttendanceLog).filter(AttendanceLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Attendance log not found")
    return log
