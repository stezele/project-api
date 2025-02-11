from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.core.database import engine

router = APIRouter()


@router.get("/hired_by_quarter", response_model=list)
def hired_by_quarter():
    """
    Returns the number of employees hired per job and department in 2021, divided by quarter.
    """
    query = text("""
    SELECT
        d.department,
        j.job,
        SUM(CASE WHEN MONTH(he.datetime) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN MONTH(he.datetime) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN MONTH(he.datetime) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN MONTH(he.datetime) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
    WHERE YEAR(he.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """)
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = [dict(row) for row in result]
    return rows


@router.get("/departments_above_avg", response_model=list)
def departments_above_avg():
    """
    Returns a list of departments that hired more employees than the average in 2021.
    """
    query = text("""
        WITH hires AS(
            SELECT d.id, d.department, COUNT(he.id) AS hired
            FROM departments d
            LEFT JOIN hired_employees he ON d.id=he.department_id AND YEAR(he.datetime)=2021
            GROUP BY d.id, d.department
        ),
        avg_hires AS(
            SELECT AVG(hired * 1.0) as avg_hired FROM hires
        )
        SELECT h.id, h.department, h.hired
        FROM hires h, avg_hires a
        WHERE h.hired > a.avg_hired
        ORDER BY h.hired DESC
   """)
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = [dict(row) for row in result]
    return rows
