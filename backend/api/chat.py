# backend/api/chat.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    # TODO: later call Watson Assistant here
    # for now, simple echo so frontend wiring works
    return ChatResponse(reply=f"Echo: {req.text}")
