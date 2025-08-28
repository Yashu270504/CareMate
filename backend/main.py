from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CareMate API",
    description="Backend API for CareMate health assistant",
    version="1.0.0"
)

# Allow all origins for testing (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def read_root():
    return {"message": "CareMate API is running!"}
