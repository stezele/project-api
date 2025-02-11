from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
from sqlalchemy import text
from app.core.database import engine
from fastavro import writer, parse_schema, reader

router = APIRouter()


@router.get("/{table_name}", response_model=dict)
def backup_table(table_name: str):
    """
    Create a backup of the specified table in Avro format.
    """
    if table_name not in ["hired_employees", "departments", "jobs"]:
        raise HTTPException(status_code=400, detail="Invalid table")

    # Read table data using pandas
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)

    # Define a basic Avro schema (adjust types as needed)
    schema = {
        "doc": f"Backup of {table_name}",
        "name": table_name,
        "namespace": "globant.backup",
        "type": "record",
        "fields": [{"name": col, "type": "string"} for col in df.columns]
    }
    parsed_schema = parse_schema(schema)

    # Convert all data to strings to match the defined schema
    records = df.astype(str).to_dict(orient="records")

    backup_file = f"backup_{table_name}.avro"
    with open(backup_file, "wb") as out:
        writer(out, parsed_schema, records)

    return {"message": f"Backup of {table_name} generated successfully", "file": backup_file}


@router.post("/restore/{table_name}", response_model=dict)
async def restore_table(table_name: str, file: UploadFile = File(...)):
    """
    Restore the specified table from an Avro backup file.
    """
    if table_name not in ["hired_employees", "departments", "jobs"]:
        raise HTTPException(status_code=400, detail="Invalid table")
    try:
        contents = await file.read()
        temp_file = f"temp_{table_name}.avro"
        with open(temp_file, "wb") as f:
            f.write(contents)

        with open(temp_file, "rb") as fo:
            avro_reader = reader(fo)
            records = [record for record in avro_reader]

        # Insert records into the table (assuming the record format matches the database schema)
        with engine.connect() as connection:
            trans = connection.begin()
            for record in records:
                fields = ', '.join(record.keys())
                placeholders = ', '.join([f":{k}" for k in record.keys()])
                query = text(
                    f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})")
                connection.execute(query, record)
            trans.commit()

        return {"message": f"Table {table_name} restored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restoration error: {e}")
