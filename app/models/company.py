from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    shifts = relationship("Shift", back_populates="company", cascade="all, delete-orphan")
