import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel
from bson import ObjectId

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "health_app")

_client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URL)
db: AsyncIOMotorDatabase = _client[DB_NAME]


def _ensure_str_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id")) if doc.get("_id") else None
    doc.pop("_id", None)
    return doc

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    data = {**data, "created_at": now, "updated_at": now}
    res = await db[collection_name].insert_one(data)
    created = await db[collection_name].find_one({"_id": res.inserted_id})
    return _ensure_str_id(created)

async def get_documents(
    collection_name: str,
    filter_dict: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = 100,
    sort: Optional[List] = None,
) -> List[Dict[str, Any]]:
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict)
    if sort:
        cursor = cursor.sort(sort)
    if limit:
        cursor = cursor.limit(limit)
    docs = await cursor.to_list(length=limit or 1000)
    return [_ensure_str_id(d) for d in docs]

async def get_document_by_id(collection_name: str, id_str: str) -> Optional[Dict[str, Any]]:
    try:
        oid = ObjectId(id_str)
    except Exception:
        return None
    doc = await db[collection_name].find_one({"_id": oid})
    return _ensure_str_id(doc) if doc else None

async def update_document(collection_name: str, id_str: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        oid = ObjectId(id_str)
    except Exception:
        return None
    data["updated_at"] = datetime.utcnow().isoformat()
    await db[collection_name].update_one({"_id": oid}, {"$set": data})
    doc = await db[collection_name].find_one({"_id": oid})
    return _ensure_str_id(doc) if doc else None

async def delete_document(collection_name: str, id_str: str) -> bool:
    try:
        oid = ObjectId(id_str)
    except Exception:
        return False
    res = await db[collection_name].delete_one({"_id": oid})
    return res.deleted_count == 1
