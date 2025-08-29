# CareMate/ml/predict.py

from pathlib import Path
import os
import pickle
import pandas as pd
from ml.rules.rule_engine import rule_check  # ✅ rule engine

# ---------------- Paths ----------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # CareMate/
MODEL_PATH = PROJECT_ROOT / "ml" / "models"
DATA_PATH = PROJECT_ROOT / "datasets" / "dataset_with_enriched_alternatives_cleaned12.csv"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"❌ Model directory not found at: {MODEL_PATH}")

# ---------------- Utils ----------------
def load_model(target):
    """Load the trained ML model for a given target column."""
    path = MODEL_PATH / f"{target}_model.pkl"
    if not path.exists():
        raise FileNotFoundError(f"❌ Model not found: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

def get_dataset_columns():
    """Helper: list dataset columns so you know what features exist."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"❌ Dataset not found: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    return df.columns.tolist()

# ---------------- Prediction ----------------
def predict(user_input, target):
    """
    Predict target value using ML model.
    If rule engine has an override, return that.
    """
    # 1. Try rules first
    rule_result = rule_check(user_input, target)
    if rule_result is not None:
        return rule_result

    # 2. ML-based prediction
    # (update features based on actual dataset columns!)
    expected_features = ["drug_medicine", "food_name", "ingredients", "allergens"]

    df = pd.DataFrame([user_input], columns=expected_features)
    model = load_model(target)
    return model.predict(df)[0]

# ---------------- Demo ----------------
if __name__ == "__main__":
    print("📦 Checking dataset columns...")
    try:
        cols = get_dataset_columns()
        print("✅ Dataset columns:", cols)
    except Exception as e:
        print("⚠️ Could not load dataset:", e)

    # Example input (make sure keys match expected_features above)
    user_input = {
        "drug_medicine": "paracetamol",
        "food_name": "ice cream",
        "ingredients": "milk, sugar",
        "allergens": "lactose"
    }

    print("\n🔮 Predictions:")
    try:
        risk = predict(user_input, "risk_level")
        print("Risk Level Prediction:", risk)

        side = predict(user_input, "side_effect")
        print("Side Effect Prediction:", side)

        use = predict(user_input, "use")
        print("Use Prediction:", use)

    except Exception as e:
        print("❌ Prediction error:", e)
