from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.leave import LeaveStatusEnum


class LeaveBase(BaseModel):
    employee_id: int
    date: date_type
    reason: Optional[str] = None


class LeaveCreate(LeaveBase):
    # Status defaults to "pending" on creation; not accepted from the client here.
    pass


class LeaveOut(LeaveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: LeaveStatusEnum
