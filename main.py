from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel as PydanticBaseModel
import os
import database as db
from models import (
    SubjectCreate, SubjectUpdate, SubjectResponse,
    ConnectionCreate, ConnectionUpdate, ConnectionResponse,
)
from seed_data import seed

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")

app = FastAPI(title="KHU CSE Curriculum Map API", version="1.0.0")

# ── Startup ──
@app.on_event("startup")
def startup():
    db.init_db()
    if db.is_db_empty():
        seed()


# ── Auth ──
class AuthRequest(PydanticBaseModel):
    password: str

@app.post("/api/auth")
def auth(data: AuthRequest):
    if data.password == ADMIN_PASSWORD:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Wrong password")


# ── Subject API ──

@app.get("/api/subjects", response_model=list[SubjectResponse])
def list_subjects():
    return db.get_all_subjects()


@app.post("/api/subjects", response_model=SubjectResponse, status_code=201)
def create_subject(data: SubjectCreate):
    success = db.create_subject(data.model_dump())
    if not success:
        raise HTTPException(status_code=409, detail=f"Subject '{data.id}' already exists")
    return db.get_subject(data.id)


@app.put("/api/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: str, data: SubjectUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = db.update_subject(subject_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")
    return db.get_subject(subject_id)


@app.delete("/api/subjects/{subject_id}")
def delete_subject(subject_id: str):
    success = db.delete_subject(subject_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")
    return {"message": f"Subject '{subject_id}' deleted"}


# ── Connection API ──

@app.get("/api/connections")
def list_connections():
    return db.get_all_connections()


@app.post("/api/connections", status_code=201)
def create_connection(data: ConnectionCreate):
    new_id = db.create_connection(data.model_dump())
    if new_id is None:
        raise HTTPException(status_code=400, detail="from_id or to_id does not exist")
    conns = db.get_all_connections()
    return next((c for c in conns if c["id"] == new_id), None)


@app.put("/api/connections/{conn_id}")
def update_connection(conn_id: int, data: ConnectionUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    success = db.update_connection(conn_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail=f"Connection {conn_id} not found")
    conns = db.get_all_connections()
    return next((c for c in conns if c["id"] == conn_id), None)


@app.delete("/api/connections/{conn_id}")
def delete_connection(conn_id: int):
    success = db.delete_connection(conn_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Connection {conn_id} not found")
    return {"message": f"Connection {conn_id} deleted"}


@app.get("/api/subjects/{subject_id}/connection-count")
def get_connection_count(subject_id: str):
    conns = db.get_all_connections()
    count = sum(1 for c in conns if c["from"] == subject_id or c["to"] == subject_id)
    return {"count": count}


# ── Static files ──
app.mount("/", StaticFiles(directory="static", html=True), name="static")
