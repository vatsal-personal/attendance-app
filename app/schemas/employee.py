from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    device_user_id: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    company_id: int


class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    created_at: datetime
