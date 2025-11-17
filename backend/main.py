from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents, get_document_by_id, update_document, delete_document
from schemas import SymptomEntry, LabResult, SupplementLog, Reminder, Profile, Insight

app = FastAPI(title="Health Monitoring API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

# Generic CRUD helpers

class IdResponse(BaseModel):
    id: str

# Symptom Entries
@app.post("/entries", response_model=dict)
async def create_entry(payload: SymptomEntry):
    doc = await create_document("symptomentry", payload.model_dump())
    return doc

@app.get("/entries", response_model=List[dict])
async def list_entries(user_id: Optional[str] = None, limit: int = 100):
    filt = {"user_id": user_id} if user_id else {}
    docs = await get_documents("symptomentry", filt, limit=limit, sort=[("date", -1)])
    return docs

@app.get("/entries/{entry_id}")
async def get_entry(entry_id: str):
    doc = await get_document_by_id("symptomentry", entry_id)
    if not doc:
        raise HTTPException(404, "Not found")
    return doc

@app.put("/entries/{entry_id}")
async def update_entry(entry_id: str, payload: SymptomEntry):
    doc = await update_document("symptomentry", entry_id, payload.model_dump())
    if not doc:
        raise HTTPException(404, "Not found")
    return doc

@app.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str):
    ok = await delete_document("symptomentry", entry_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"ok": True}

# Lab Results
@app.post("/labs", response_model=dict)
async def create_lab(payload: LabResult):
    doc = await create_document("labresult", payload.model_dump())
    return doc

@app.get("/labs", response_model=List[dict])
async def list_labs(user_id: Optional[str] = None, limit: int = 100):
    filt = {"user_id": user_id} if user_id else {}
    docs = await get_documents("labresult", filt, limit=limit, sort=[("test_date", -1)])
    return docs

# Supplements
@app.post("/supplements", response_model=dict)
async def create_supplement(payload: SupplementLog):
    doc = await create_document("supplementlog", payload.model_dump())
    return doc

@app.get("/supplements", response_model=List[dict])
async def list_supplements(user_id: Optional[str] = None, limit: int = 200):
    filt = {"user_id": user_id} if user_id else {}
    docs = await get_documents("supplementlog", filt, limit=limit, sort=[("name", 1)])
    return docs

# Reminders
@app.post("/reminders", response_model=dict)
async def create_reminder(payload: Reminder):
    doc = await create_document("reminder", payload.model_dump())
    return doc

@app.get("/reminders", response_model=List[dict])
async def list_reminders(user_id: Optional[str] = None, limit: int = 200):
    filt = {"user_id": user_id} if user_id else {}
    docs = await get_documents("reminder", filt, limit=limit, sort=[("title", 1)])
    return docs

# Profiles
@app.post("/profiles", response_model=dict)
async def create_profile(payload: Profile):
    doc = await create_document("profile", payload.model_dump())
    return doc

@app.get("/profiles", response_model=List[dict])
async def list_profiles(owner_id: Optional[str] = None, limit: int = 50):
    filt = {"owner_id": owner_id} if owner_id else {}
    docs = await get_documents("profile", filt, limit=limit, sort=[("name", 1)])
    return docs

# Insights (precomputed or manual)
@app.post("/insights", response_model=dict)
async def create_insight(payload: Insight):
    doc = await create_document("insight", payload.model_dump())
    return doc

@app.get("/insights", response_model=List[dict])
async def list_insights(user_id: Optional[str] = None, limit: int = 100):
    filt = {"user_id": user_id} if user_id else {}
    docs = await get_documents("insight", filt, limit=limit, sort=[("created_at", -1)])
    return docs

