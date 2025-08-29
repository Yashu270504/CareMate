"""
Train three ML classifiers on your cleaned dataset:
1) risk_level (main safety label → Logistic Regression)
2) side_effect (most likely effect → Random Forest)
3) allergens_medicine (likely allergen from medicine → Random Forest)

Unified preprocessing pipeline:
- OneHotEncoder for categorical columns
- TfidfVectorizer for free-text columns

Artifacts saved to:
ml/models/risk_level_model.pkl
ml/models/side_effect_model.pkl
ml/models/allergens_model.pkl
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# ----------------------------
# 0) Paths & constants
# ----------------------------
DATA_PATH = Path("datasets/cleaned/final_dataset_dynamic_dedup.xlsx")
SHEET_NAME = "final_dataset_dynamic_dedup"
MODEL_DIR = Path("ml/models")
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Columns used as features
CAT_COLS: List[str] = ["drug_name", "condition", "age_grp", "food_name", "main_ingredient"]
TEXT_COLS: List[str] = ["ingredients", "allergens_combined"]

# Targets
TARGETS: Dict[str, Dict] = {
    "risk_level": {
        "outfile": MODEL_DIR / "risk_level_model.pkl",
        "algo": "logistic",   # Logistic Regression
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
    "side_effect": {
        "outfile": MODEL_DIR / "side_effect_model.pkl",
        "algo": "rf",         # Random Forest
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
    "allergens_medicine": {
        "outfile": MODEL_DIR / "allergens_model.pkl",
        "algo": "rf",         # Random Forest
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
}

def load_data(path: Path, sheet: str) -> pd.DataFrame:
    """Load Excel and normalize."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path.resolve()}")

    df = pd.read_excel(path, sheet_name=sheet)

    # Drop empty cols
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Normalize text
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

    # Normalize risk_level labels
    if "risk_level" in df.columns:
        mapping = {
            "safe": "safe",
            "safely": "safe",
            "low": "safe",
            "risky": "caution",
            "moderate": "caution",
            "danger": "dangerous",
            "dangerous": "dangerous",
            "high": "dangerous",
        }
        df["risk_level"] = df["risk_level"].replace(mapping)

    return df

def make_preprocessor(cat_cols: List[str], text_cols: List[str]) -> ColumnTransformer:
    """Preprocessing: OneHot for categories, TF-IDF for text."""
    transformers = []
    if cat_cols:
        transformers.append(("cats", OneHotEncoder(handle_unknown="ignore", sparse_output=True), cat_cols))
    for txt in text_cols:
        transformers.append((f"tfidf_{txt}", TfidfVectorizer(), txt))
    pre = ColumnTransformer(transformers=transformers, remainder="drop", sparse_threshold=0.3)
    return pre

def build_pipeline(cat_cols: List[str], text_cols: List[str], algo: str) -> Pipeline:
    """Choose pipeline based on algo flag."""
    pre = make_preprocessor(cat_cols, text_cols)
    if algo == "logistic":
        clf = LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            multi_class="multinomial",
            solver="lbfgs",
            random_state=RANDOM_STATE,
        )
    else:  # default → RandomForest
        clf = RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            n_jobs=-1,
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
        )
    return Pipeline([("preprocess", pre), ("clf", clf)])

def eval_and_print(y_true, y_pred, label: str):
    print(f"\n=== {label.upper()} | Classification Report ===")
    print(classification_report(y_true, y_pred, zero_division=0))
    print(f"=== {label.upper()} | Confusion Matrix ===")
    print(confusion_matrix(y_true, y_pred))

def train_one_head(df: pd.DataFrame, target: str, meta: Dict) -> None:
    """Train and save one model."""
    dfx = df[df[target].astype(str).str.len() > 0].reset_index(drop=True)

    exclude = set(meta["exclude_from_features"] + [target])
    feature_cols = [c for c in (CAT_COLS + TEXT_COLS) if c not in exclude and c in dfx.columns]

    X = dfx[feature_cols]
    y = dfx[target].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y if y.nunique() > 1 else None
    )

    pipe = build_pipeline(
        cat_cols=[c for c in feature_cols if c in CAT_COLS],
        text_cols=[c for c in feature_cols if c in TEXT_COLS],
        algo=meta["algo"],
    )
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    eval_and_print(y_test, y_pred, target)

    meta["outfile"].parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, meta["outfile"])
    print(f"✅ Saved {target} model to: {meta['outfile']}")

def main():
    print("📦 Loading dataset…")
    df = load_data(DATA_PATH, SHEET_NAME)

    for tgt in TARGETS:
        print(f"\n▶ Target '{tgt}' distribution:")
        print(df[tgt].value_counts())

    for tgt, meta in TARGETS.items():
        print(f"\n🚀 Training model for: {tgt}")
        train_one_head(df, tgt, meta)

    print("\n✨ All models trained and saved. Hybrid setup ready for FastAPI.")

if __name__ == "__main__":
    main()
