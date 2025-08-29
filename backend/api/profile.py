# backend/api/profile.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/profile", tags=["profile"])

class Profile(BaseModel):
    name: str
    age: int | None = None

_FAKE_DB: Profile | None = None

@router.get("")
def get_profile():
    return _FAKE_DB or {"name": "Guest"}

@router.post("")
def save_profile(p: Profile):
    global _FAKE_DB
    _FAKE_DB = p
    return {"saved": True}
