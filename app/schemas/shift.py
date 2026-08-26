from datetime import time

from pydantic import BaseModel, ConfigDict


class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time


class ShiftCreate(ShiftBase):
    company_id: int


class ShiftOut(ShiftBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
