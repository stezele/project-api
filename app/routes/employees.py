from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import HiredEmployeeSchema, HiredEmployeeBatch
from app.models import HiredEmployee
from app.core.database import get_db

router = APIRouter()


@router.post("/", response_model=dict)
def create_employee(employee: HiredEmployeeSchema, db: Session = Depends(get_db)):
    """
    Endpoint to create a single employee.
    """
    new_employee = HiredEmployee(**employee.model_dump())
    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return {"message": "Employee created successfully", "employee_id": new_employee.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error creating employee: {e}")


@router.post("/batch", response_model=dict)
def create_employees_batch(batch: HiredEmployeeBatch, db: Session = Depends(get_db)):
    """
    Endpoint to create multiple employees in a batch.
    Maximum allowed rows: 1000.
    """
    if len(batch.employees) > 1000:
        raise HTTPException(
            status_code=400, detail="Maximum of 1000 rows allowed")
    inserted = 0
    errors = []
    for emp in batch.employees:
        new_emp = HiredEmployee(**emp.model_dump())
        try:
            db.add(new_emp)
            db.commit()
            inserted += 1
        except Exception as e:
            db.rollback()
            errors.append({"id": emp.id, "error": str(e)})
    return {"inserted": inserted, "errors": errors}
