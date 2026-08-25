"""
Import all models here so that Base.metadata is aware of every table
when app.core.database.Base.metadata.create_all(engine) is called.
"""
from app.models.company import Company
from app.models.employee import Employee
from app.models.attendance_log import AttendanceLog, DirectionEnum
from app.models.shift import Shift
from app.models.leave import Leave, LeaveStatusEnum

__all__ = [
    "Company",
    "Employee",
    "AttendanceLog",
    "DirectionEnum",
    "Shift",
    "Leave",
    "LeaveStatusEnum",
]
