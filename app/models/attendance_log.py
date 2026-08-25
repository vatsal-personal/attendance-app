import enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class DirectionEnum(str, enum.Enum):
    IN = "in"
    OUT = "out"


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    direction = Column(Enum(DirectionEnum, name="direction_enum"), nullable=False)
    # Identifier of the physical device that generated this log (e.g. serial number)
    device_id = Column(String(64), nullable=True)
    # Where the log came from, e.g. "biometric_device", "manual", "mobile_app"
    source = Column(String(64), nullable=True)

    employee = relationship("Employee", back_populates="attendance_logs")
