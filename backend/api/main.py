from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn
import pandas as pd
from pathlib import Path

# =====================
# Load Models
# =====================
MODEL_DIR = Path(__file__).resolve().parent.parent / "ml" / "models"
risk_model = joblib.load(MODEL_DIR / "risk_level_model.pkl")
side_effect_model = joblib.load(MODEL_DIR / "side_effect_model.pkl")
allergen_model = joblib.load(MODEL_DIR / "allergens_model.pkl")

# =====================
# FastAPI App
# =====================
app = FastAPI(title="CareMate ML API", version="1.0")

# Define input schema
class MedicineInput(BaseModel):
    name: str
    ingredients: str
    dosage: float = 0
    age: int = 0
    medical_history: str = ""

# =====================
# Routes
# =====================

@app.get("/")
def home():
    return {"message": "Welcome to CareMate ML API 🚑"}

@app.post("/predict")
def predict(data: MedicineInput):
    # Convert input into DataFrame
    df = pd.DataFrame([data.dict()])

    # Predict each target
    risk_pred = risk_model.predict(df)[0]
    side_pred = side_effect_model.predict(df)[0]
    allergen_pred = allergen_model.predict(df)[0]

    return {
        "risk_level": str(risk_pred),
        "side_effect": str(side_pred),
        "allergens": str(allergen_pred)
    }

# =====================
# Run the API
# =====================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)