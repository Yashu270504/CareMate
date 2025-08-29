# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .chat import router as chat_router
from .profile import router as profile_router

app = FastAPI(title="CareMate API")

# allow your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # add your deployed URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount routers under a single prefix
app.include_router(chat_router, prefix="/api")
app.include_router(profile_router, prefix="/api")

@app.get("/api/health")
def health():
    return {"ok": True}
