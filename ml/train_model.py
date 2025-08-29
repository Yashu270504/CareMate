"""
Train three light ML classifiers on your cleaned dataset:
1) risk_level (main safety label)
2) side_effect (most likely effect)
3) allergens_medicine (likely allergen from medicine)

We use a unified preprocessing pipeline:
- OneHotEncoder for categorical columns
- TfidfVectorizer for free-text columns
- RandomForest (robust, fast) for classification

Artifacts saved to:
ml/models/risk_level_model.pkl
ml/models/side_effect_model.pkl
ml/models/allergens_model.pkl
Each artifact is a full sklearn Pipeline (preprocess + model).
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Dict

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ----------------------------
# 0) Paths & constants
# ----------------------------
DATA_PATH = Path("datasets/cleaned/final_dataset_dynamic_dedup.xlsx")
SHEET_NAME = "final_dataset_dynamic_dedup"
MODEL_DIR = Path("ml/models")
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Columns we’ll use as features (inputs to the model)
CAT_COLS: List[str] = ["drug_name", "condition", "age_grp", "food_name", "main_ingredient"]
TEXT_COLS: List[str] = ["ingredients", "allergens_combined"]

# Targets we will train (three separate classifiers)
TARGETS: Dict[str, Dict] = {
    "risk_level": {
        "outfile": MODEL_DIR / "risk_level_model.pkl",
        # Exclude target-like columns from features for this head
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
    "side_effect": {
        "outfile": MODEL_DIR / "side_effect_model.pkl",
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
    "allergens_medicine": {
        "outfile": MODEL_DIR / "allergens_model.pkl",
        "exclude_from_features": ["risk_level", "side_effect", "allergens_medicine"],
    },
}


def load_data(path: Path, sheet: str) -> pd.DataFrame:
    """Load Excel and do light sanity cleaning."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path.resolve()}")

    df = pd.read_excel(path, sheet_name=sheet)

    # Drop fully empty unnamed columns if any slipped in
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Basic trims / standardization
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # Lowercase a few key text columns to reduce sparse vocab
    for col in ["drug_name", "condition", "age_grp", "food_name", "main_ingredient",
                "ingredients", "allergens_combined", "side_effect", "risk_level",
                "allergens_medicine"]:
        if col in df.columns:
            df[col] = df[col].str.lower()

    # Optional: normalize common risk labels
    if "risk_level" in df.columns:
        mapping = {
            "safe": "safe",
            "safely": "safe",
            "low": "safe",
            "risky": "risky",
            "moderate": "risky",
            "danger": "dangerous",
            "dangerous": "dangerous",
            "high": "dangerous",
        }
        df["risk_level"] = df["risk_level"].replace(mapping)

    return df


def make_preprocessor(cat_cols: List[str], text_cols: List[str]) -> ColumnTransformer:
    """
    Build a ColumnTransformer that:
      - OneHotEncodes categorical columns
      - TF-IDF vectorizes free-text columns independently
    """
    transformers = []

    if cat_cols:
        transformers.append(
            ("cats", OneHotEncoder(handle_unknown="ignore", sparse=True), cat_cols)
        )

    # Each text column gets its own TF-IDF vectorizer to keep signals separate
    for txt in text_cols:
        transformers.append(
            (f"tfidf_{txt}", TfidfVectorizer(), txt)
        )

    # Note: ColumnTransformer supports passing a single column name directly to a text transformer.
    pre = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        sparse_threshold=0.3,
        verbose_feature_names_out=False,
    )
    return pre


def build_pipeline(cat_cols: List[str], text_cols: List[str]) -> Pipeline:
    """Preprocessing + RandomForest in a single sklearn Pipeline."""
    pre = make_preprocessor(cat_cols, text_cols)
    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        n_jobs=-1,
        class_weight="balanced_subsample",
        random_state=RANDOM_STATE,
    )
    pipe = Pipeline([
        ("preprocess", pre),
        ("clf", clf),
    ])
    return pipe


def eval_and_print(y_true, y_pred, label: str):
    """Print standard metrics for quick feedback."""
    print(f"\n=== {label.upper()} | Classification Report ===")
    print(classification_report(y_true, y_pred, zero_division=0))
    print(f"=== {label.upper()} | Confusion Matrix ===")
    print(confusion_matrix(y_true, y_pred))


def train_one_head(df: pd.DataFrame, target: str, outfile: Path) -> None:
    """
    Train a single classifier for `target`.
    Steps:
      1) Filter rows with non-empty target
      2) Build a features view (exclude targets and obvious leak columns)
      3) Train/test split (stratify by target)
      4) Fit pipeline (preprocess + RF)
      5) Evaluate and save artifact
    """
    # 1) Keep rows with target label present
    dfx = df.copy()
    dfx = dfx[dfx[target].astype(str).str.len() > 0].reset_index(drop=True)

    # 2) Choose features safely (avoid leakage)
    exclude = set(TARGETS[target]["exclude_from_features"] + [target])
    feature_cols = [c for c in (CAT_COLS + TEXT_COLS) if c not in exclude and c in dfx.columns]

    X = dfx[feature_cols]
    y = dfx[target].astype(str)

    # 3) Split
    strat = y if y.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=strat
    )

    # 4) Pipeline
    pipe = build_pipeline(cat_cols=[c for c in feature_cols if c in CAT_COLS],
                          text_cols=[c for c in feature_cols if c in TEXT_COLS])

    pipe.fit(X_train, y_train)

    # 5) Evaluate
    y_pred = pipe.predict(X_test)
    eval_and_print(y_test, y_pred, target)

    # 6) Save
    outfile.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, outfile)
    print(f"✅ Saved {target} model to: {outfile}")


def main():
    print("📦 Loading dataset…")
    df = load_data(DATA_PATH, SHEET_NAME)

    # Quick sanity check that required columns exist
    required = set(CAT_COLS + TEXT_COLS + list(TARGETS.keys()))
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Show basic class balance info
    for tgt in TARGETS:
        if tgt in df.columns:
            print(f"\n▶ Target '{tgt}' distribution:")
            print(df[tgt].value_counts())

    # Train each head independently
    for tgt, meta in TARGETS.items():
        print(f"\n🚀 Training model for: {tgt}")
        train_one_head(df, tgt, meta["outfile"])

    print("\n✨ All models trained and saved. Ready for inference in FastAPI.")

if __name__ == "__main__":
    main()
