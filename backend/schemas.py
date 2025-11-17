from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

# Each model maps to a Mongo collection using the class name lowercased

class SymptomEntry(BaseModel):
    user_id: str
    date: date
    duration_days: int = 0
    symptoms: List[dict] = Field(default_factory=list)  # [{name: str, severity: int(1-10)}]
    medications: List[dict] = Field(default_factory=list)  # [{name, dosage, frequency, effectiveness}]
    recovery_notes: Optional[str] = None
    photos: List[str] = Field(default_factory=list)

class LabResult(BaseModel):
    user_id: str
    test_date: date
    biomarkers: List[dict] = Field(default_factory=list)  # [{name, value, unit, optimal_min, optimal_max}]
    source: Optional[str] = None  # uploaded, ocr, provider
    notes: Optional[str] = None

class SupplementLog(BaseModel):
    user_id: str
    name: str
    dosage: Optional[str] = None
    schedule: str = "daily"  # daily, weekly, as-needed
    taken_on: List[date] = Field(default_factory=list)

class Reminder(BaseModel):
    user_id: str
    title: str
    schedule_cron: str  # simplified cron-like string
    profile_id: Optional[str] = None
    snooze_minutes: int = 10

class Profile(BaseModel):
    owner_id: str
    name: str
    relation: str = "self"  # self, child, parent
    dob: Optional[date] = None
    chronic_conditions: List[str] = Field(default_factory=list)
    medications: List[dict] = Field(default_factory=list)  # ongoing meds with refill
    critical_info: Optional[str] = None
    privacy_level: str = "standard"

class Insight(BaseModel):
    user_id: str
    type: str
    message: str
    score: Optional[float] = None
    created_at: Optional[datetime] = None
