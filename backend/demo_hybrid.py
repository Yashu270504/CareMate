from typing import List, Dict
import pandas as pd
from pathlib import Path
from termcolor import colored

# === Load Dataset ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "datasets" / "cleaned" / "final_dataset_dynamic_dedup.xlsx"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"❌ Dataset not found at: {DATA_PATH}")

df = pd.read_excel(DATA_PATH)
print(f"📦 Loaded dataset with {len(df)} rows and {len(df.columns)} columns from {DATA_PATH}")

# Preprocess lowercase
for col in ["food_name", "ingredients", "medicine", "condition", 
            "risk_level", "side_effect", "allergens_medicine"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower()


# === Rule Engine Function ===
def rule_check(user: Dict, food_name: str, medicines: List[str]) -> Dict:
    food = food_name.lower()
    meds = [m.lower() for m in medicines]

       # Extra smart rules for demo (not obvious ones)
    if "grapefruit" in food and any(m in meds for m in ["amlodipine", "nifedipine"]):
        return {
            "risk": "danger",
            "reason": "⚠ Grapefruit raises calcium channel blocker (blood pressure med) levels dangerously.",
            "source": "Food-drug interaction rule"
        }

    if "milk" in food and any(m in meds for m in ["tetracycline", "ciprofloxacin"]):
        return {
            "risk": "caution",
            "reason": "⚠ Milk reduces absorption of certain antibiotics like tetracycline.",
            "source": "Food-drug absorption rule"
        }

    if "spinach" in food and any("warfarin" in m for m in meds):
        return {
            "risk": "danger",
            "reason": "⚠ Spinach (Vitamin K) reduces Warfarin’s effectiveness, risking clots.",
            "source": "Vitamin K–drug interaction rule"
        }

    if "banana" in food and any(m in meds for m in ["lisinopril", "ramipril"]):
        return {
            "risk": "caution",
            "reason": "⚠ Bananas add potassium, risky with ACE inhibitors like Lisinopril.",
            "source": "Potassium–drug rule"
        }

    if "chocolate" in food and any("phenelzine" in m or "maoi" in m for m in meds):
        return {
            "risk": "danger",
            "reason": "⚠ Chocolate (tyramine) interacts with MAOI antidepressants, causing high BP.",
            "source": "Tyramine–MAOI interaction"
        }


    if "aspirin" in meds and user.get("age", 0) < 12:
        return {
            "risk": "danger",
            "reason": "⚠ Aspirin is unsafe for children under 12 (Reye's syndrome).",
            "source": "Pediatric safety rule"
        }

    if "chocolate cake" in food and "diabetes" in user.get("conditions", []):
        return {
            "risk": "caution",
            "reason": "⚠ Chocolate cake has sugar, risky for diabetics.",
            "source": "Diabetes–sugar rule"
        }

    # ✅ Fixed allergy rule
    for allergen in user.get("allergies", []):
        if allergen in food:
            return {
                "risk": "danger",
                "reason": f"⚠ Contains {allergen}, user has {allergen} allergy.",
                "source": "Allergy rule"
            }

    # --- FALLBACK: no explicit rule found ---
    return {
        "risk": "safe",
        "reason": f"No explicit rule matched for {food}. ML model can refine this.",
        "source": "Default safe rule"
    }


# === Pretty Print Helper ===
def pretty_print(title: str, result: Dict):
    print(f"\n=== {title} ===")
    risk_color = {"safe": "green", "caution": "yellow", "danger": "red"}
    risk = result.get("risk", "unknown")
    print(colored(f"Risk Level: {risk.upper()}", risk_color.get(risk, "white")))
    print(f"Reason: {result.get('reason')}")
    print(f"Source: {result.get('source')}")


# === Demo Cases ===
if __name__ == "__main__":
    # Case 1

    # Case 5 (safe case)
    #user5 = {"age": 30, "allergies": [], "conditions": []}
    #pretty_print("Healthy Adult + Apple", rule_check(user5, "apple", []))

    # Case 6
    user6 = {"age": 60, "allergies": [], "conditions": ["hypertension"]}
    pretty_print("Hypertensive + Grapefruit + Amlodipine", rule_check(user6, "grapefruit", ["amlodipine"]))

    # Case 7
    user7 = {"age": 30, "allergies": [], "conditions": []}
    pretty_print("Adult + Milk + Ciprofloxacin", rule_check(user7, "milk", ["ciprofloxacin"]))

    # Case 8
    user8 = {"age": 65, "allergies": [], "conditions": []}
    pretty_print("Senior + Spinach + Warfarin", rule_check(user8, "spinach", ["warfarin"]))

    # Case 9
    user9 = {"age": 50, "allergies": [], "conditions": []}
    pretty_print("Adult + Banana + Lisinopril", rule_check(user9, "banana", ["lisinopril"]))

    # Case 10
    user10 = {"age": 40, "allergies": [], "conditions": []}
    pretty_print("Adult + Chocolate + MAOI (Phenelzine)", rule_check(user10, "chocolate", ["phenelzine"]))
