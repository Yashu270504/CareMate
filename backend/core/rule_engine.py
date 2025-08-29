from typing import List, Dict
import pandas as pd
from pathlib import Path

# ---------- Setup ----------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "datasets" / "cleaned" / "final_dataset_dynamic_dedup.xlsx"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"❌ Dataset not found at: {DATA_PATH}")

# Load Excel instead of CSV
df = pd.read_excel(DATA_PATH)
print(f"📦 Loaded dataset with {len(df)} rows and {len(df.columns)} columns from {DATA_PATH}")

# Preprocess lowercase for matching
for col in ["food_name", "ingredients", "medicine", "condition",
            "risk_level", "side_effect", "allergens_medicine"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower()


# ---------- Rule Engine ----------
def rule_check(user: Dict, food_name: str, medicines: List[str]) -> Dict:
    """
    Apply dataset-driven rules for allergies, conditions, food-drug interactions, etc.
    """
    food = food_name.lower()
    meds = [m.lower() for m in medicines]

    # Find matching food rows
    rows = df[df["food_name"].str.contains(food, case=False, na=False)]

    # 1. Allergy check in food ingredients
    for allergen in user.get("allergies", []):
        if not rows.empty and rows["ingredients"].str.contains(allergen, case=False, na=False).any():
            return {
                "risk": "danger",
                "reason": f"Contains {allergen}, which you are allergic to.",
                "source": "Allergy dataset rule"
            }

    # 2. Medicine ↔ allergy check (but only for matched medicines)
    for med in meds:
        med_row = df[df["medicine"].str.contains(med, case=False, na=False)]
        if not med_row.empty:
            med_allergens = str(med_row["allergens_medicine"].iloc[0])
            for allergen in user.get("allergies", []):
                if pd.notna(med_allergens) and allergen in med_allergens:
                    return {
                        "risk": "danger",
                        "reason": f"{med.title()} may contain {allergen}, which you are allergic to.",
                        "source": "Medicine allergy rule"
                    }

    # 3. Condition ↔ food risks
    for cond in user.get("conditions", []):
        if not rows.empty and rows["condition"].str.contains(cond, case=False, na=False).any():
            return {
                "risk": "caution",
                "reason": f"{food.title()} is risky for {cond}.",
                "source": "Condition dataset rule"
            }

    # 4. Food ↔ drug interactions
    for med in meds:
        med_row = df[df["medicine"].str.contains(med, case=False, na=False)]
        if not rows.empty and not med_row.empty:
            return {
                "risk": med_row["risk_level"].iloc[0],
                "reason": f"{food.title()} interacts with {med.title()}.",
                "source": "Food-drug dataset rule"
            }

    # 5. Age restrictions
    if "age_limit" in df.columns:
        for med in meds:
            med_row = df[df["medicine"].str.contains(med, case=False, na=False)]
            if not med_row.empty:
                min_age = med_row["age_limit"].iloc[0]
                if pd.notna(min_age) and user.get("age", 0) < min_age:
                    return {
                        "risk": "danger",
                        "reason": f"{med.title()} not safe for age {user['age']}.",
                        "source": "Age dataset rule"
                    }

    # Nothing triggered
    return {
        "risk": "safe",
        "reason": f"No known risks found for {food_name} with given profile.",
        "source": "Default safe rule"
    }


# ---------- Demo Run ----------
if __name__ == "__main__":
    user = {
        "age": 23,
        "allergies": ["peanuts"],
        "conditions": ["thyroid"]
    }
    food = "ice cream"
    medicines = ["aspirin"]

    result = rule_check(user, food, medicines)
    print("Rule Engine Result:", result)
