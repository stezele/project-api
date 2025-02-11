# app/routes/global_data.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
# Global model that groups employees, departments, and jobs
from app.schemas import GlobalData
# SQLAlchemy models for the respective tables
from app.models import HiredEmployee, Department, Job
from app.core.database import get_db

router = APIRouter()


@router.post("/global", response_model=dict)
def receive_global_data(data: GlobalData, db: Session = Depends(get_db)):
    """
    Endpoint to receive all data (employees, departments, and jobs) in one request.
    Processes and stores the received information into the database.
    """
    try:
        # Process departments first (since employees reference departments)
        for dept in data.departments:
            # Check if the department already exists to avoid duplicates
            existing_dept = db.query(Department).filter(
                Department.id == dept.id).first()
            if not existing_dept:
                new_dept = Department(**dept.model_dump())
                db.add(new_dept)
            else:
                # Optionally, update the existing department if necessary
                pass

        # Process jobs next (since employees reference jobs)
        for job in data.jobs:
            # Check if the job already exists to avoid duplicates
            existing_job = db.query(Job).filter(Job.id == job.id).first()
            if not existing_job:
                new_job = Job(**job.model_dump())
                db.add(new_job)
            else:
                # Optionally, update the existing job if necessary
                pass

        # Process hired employees
        for emp in data.hired_employees:
            # Optionally check if the referenced department exists
            if not db.query(Department).filter(Department.id == emp.department_id).first():
                raise HTTPException(
                    status_code=400, detail=f"Department {emp.department_id} does not exist")
            # Optionally check if the referenced job exists
            if not db.query(Job).filter(Job.id == emp.job_id).first():
                raise HTTPException(
                    status_code=400, detail=f"Job {emp.job_id} does not exist")
            new_emp = HiredEmployee(**emp.model_dump())
            db.add(new_emp)

        # Commit all changes to the database
        db.commit()

        return {
            "message": "Data received and saved successfully",
            "employees": len(data.hired_employees),
            "departments": len(data.departments),
            "jobs": len(data.jobs)
        }
    except Exception as e:
        # Rollback in case of any error to avoid partial updates
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error processing data: {e}")
