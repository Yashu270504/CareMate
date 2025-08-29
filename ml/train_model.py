import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import os

# =========================
# Load dataset
# =========================
print("📦 Loading dataset…")
df = pd.read_csv("../datasets/dataset_with_enriched_alternatives_cleaned12.csv")
# Combine textual features into one string
df["features"] = (
    df["medicine"].astype(str) + " " +
    df["food_name"].astype(str) + " " +
    df["allergens"].astype(str) + " " +
    df["condition"].astype(str)
)

# Targets
targets = {
    "risk_level": "risk_level",
    "side_effect": "side_effect",
    "allergens_medicine": "allergens_medicine"
}

# Save models here
os.makedirs("ml/models", exist_ok=True)

# =========================
# Train function
# =========================
def train_and_save_model(target_name):
    print(f"\n🚀 Training model for: {target_name}")
    X = df["features"]
    y = df[target_name]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # Pipeline: TF-IDF + RandomForest
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", RandomForestClassifier(n_estimators=300, random_state=42))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # Report
    print(f"\n=== {target_name.upper()} ===")
    print(classification_report(y_test, y_pred))

    # Save model
    model_path = f"ml/models/{target_name}_model.pkl"
    joblib.dump(pipeline, model_path)
    print(f"✅ Saved {target_name} model to: {model_path}")


# =========================
# Train all targets
# =========================
for target in targets.values():
    train_and_save_model(target)

print("\n✨ All models trained and saved.")
