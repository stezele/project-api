from pydantic import BaseModel
from datetime import datetime


class HiredEmployeeSchema(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    class Config:
        orm_mode = True


class DepartmentSchema(BaseModel):
    id: int
    department: str

    class Config:
        orm_mode = True


class JobSchema(BaseModel):
    id: int
    job: str

    class Config:
        orm_mode = True

# Schema for batch insertion


class HiredEmployeeBatch(BaseModel):
    employees: list[HiredEmployeeSchema]  # ✅ List of employees


class GlobalData(BaseModel):
    hired_employees: list[HiredEmployeeSchema]
    departments: list[DepartmentSchema]
    jobs: list[JobSchema]
