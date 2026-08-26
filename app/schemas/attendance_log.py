from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.attendance_log import DirectionEnum


class AttendanceLogBase(BaseModel):
    employee_id: int
    direction: DirectionEnum
    device_id: Optional[str] = None
    source: Optional[str] = None


class AttendanceLogCreate(AttendanceLogBase):
    # Optional so a device/manual entry can supply its own timestamp,
    # or omit it to default to "now" at creation time.
    timestamp: Optional[datetime] = None


class AttendanceLogOut(AttendanceLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
