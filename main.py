"""
FastAPI entry point for the Attendance SaaS backend.

Run locally with:
    uvicorn main:app --reload
"""
from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import companies, employees, attendance_log, shift, leave

# Import models so they're registered on Base.metadata before create_all runs.
import app.models  # noqa: F401

app = FastAPI(
    title="Attendance SaaS API",
    description="Backend API for biometric attendance tracking, employees, shifts, and leaves.",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    # Creates any tables that don't exist yet. Fine for local development;
    # for production use a migration tool like Alembic instead.
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "attendance-saas-api"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}


app.include_router(companies.router)
app.include_router(employees.router)
app.include_router(attendance_log.router)
app.include_router(shift.router)
app.include_router(leave.router)
