import pandas as pd
from pathlib import Path
from ibm_watsonx_ai.foundation_models import ModelInference

# === Paths ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "datasets" / "cleaned" / "final_dataset_dynamic_dedup.xlsx"
OUTPUT_PATH = PROJECT_ROOT / "datasets" / "cleaned" / "final_dataset_polished.xlsx"

# === Load Dataset ===
df = pd.read_excel(DATA_PATH)
print(f"📦 Loaded dataset with {len(df)} rows")

# === Init Granite Model ===
model = ModelInference(
    model_id="ibm/granite-13b-chat-v2",
    params={"decoding_method": "greedy", "max_new_tokens": 100},
    credentials={
        "apikey": "cDtWvQgKCzpV2xY3iKBh9zMfaDt-mZVK4p1aw9dwhFQR",  # ✅ your API key
        "url": "https://au-syd.ml.cloud.ibm.com"               # ✅ endpoint
    },
    project_id="87386243-9df6-415e-87f1-4bd60f42bf34"          # ✅ your project ID
)

# === Function to polish text ===
def polish_text(text: str) -> str:
    if not isinstance(text, str) or text.strip() == "":
        return text
    prompt = f"Simplify and rewrite for patients: '{text}'"
    try:
        response = model.generate_text(prompt=prompt)
        return response.strip()
    except Exception as e:
        print(f"⚠ Granite error for text '{text}': {e}")
        return text

# === Apply polishing to target columns ===
for col in ["risk_level", "side_effect", "allergens_medicine"]:
    if col in df.columns:
        print(f"✨ Polishing column: {col}")
        df[col + "_polished"] = df[col].apply(polish_text)

# === Save polished dataset ===
df.to_excel(OUTPUT_PATH, index=False)
print(f"✅ Polished dataset saved to {OUTPUT_PATH}")
