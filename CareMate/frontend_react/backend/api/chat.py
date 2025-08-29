from fastapi import APIRouter
from core.granite_client import ask_granite

router = APIRouter()

@router.post("/chat")
def chat_with_ai(query: str):
    reply = ask_granite(query)
    return {"query": query, "reply": reply}
