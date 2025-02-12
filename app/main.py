from fastapi import FastAPI
from app.routes import employees, backup, metrics, global_data

app = FastAPI(
    title="API Project",
    description="API for data management, backup, and metrics",
    version="1.0.0"
)


# Include all routers
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(backup.router, prefix="/backup", tags=["Backup"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(global_data.router, prefix="/data", tags=["Data"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
