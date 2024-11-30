from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.device_model import Device
from app.schemas.device_schema import Device
from app.timeseries.influxdb_client import write_telemetry_data

router = APIRouter()

@router.post("/telemetry")
def receive_telemetry_data(device_id: int, data: dict, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    # Process and validate data
    write_telemetry_data(device_id, data)
    return {"status": "Data received"}