from fastapi import FastAPI
from app.routes import employees, backup, metrics, global_data

app = FastAPI(
    title="API Project",
    description="API for data management, backup, and metrics",
    version="1.0.0"
)

# Include routers from each module
app.include_router(employees.router, prefix="/hired_employees",
                   tags=["hired_employees"])
app.include_router(employees.router, prefix="/departments",
                   tags=["departments"])
app.include_router(employees.router, prefix="/jobs", tags=["jobs"])
app.include_router(backup.router, prefix="/backup", tags=["backup"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(global_data.router, prefix="/data", tags=["global-data"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
