# CareMate/ml/train.py

from pathlib import Path
import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ---------------- Paths ----------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # CareMate/
MODEL_PATH = PROJECT_ROOT / "ml" / "models"
DATA_PATH = PROJECT_ROOT / "datasets" / "dataset_with_enriched_alternatives_cleaned12.csv"

MODEL_PATH.mkdir(parents=True, exist_ok=True)

# ---------------- Load Data ----------------
print("📂 Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"📦 Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")
print("📝 Available columns:", df.columns.tolist())

# ---------------- Features / Targets ----------------
features = ["medicine", "food_name", "ingredients", "allergens"]
targets = ["risk_level", "side_effect", "use"]

# ---------------- Train Models ----------------
for target in targets:
    if target not in df.columns:
        print(f"⚠️ Skipping {target} (not in dataset)")
        continue

    X = df[features].fillna("unknown")
    y = df[target].fillna("unknown")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Preprocessor: OneHotEncode categorical string features
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), features)
        ]
    )

    # Pipeline: preprocessing + model
    clf = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )

    print(f"🔄 Training model for {target}...")
    clf.fit(X_train, y_train)

    # Save pipeline (includes encoder + model)
    model_path = MODEL_PATH / f"{target}_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)
    print(f"✅ Saved {target} model at {model_path}")

print("🎉 Training complete!")
