import pandas as pd
#from utils.utils import normalize_text, map_synonyms

# -------------------
# 1. Load datasets
# -------------------
def load_datasets():
    med_food_df = pd.read_csv("data/medicine_food.csv")
    cond_food_df = pd.read_csv("data/condition_food.csv")
    alt_df = pd.read_csv("data/food_alternatives.csv")
    return med_food_df, cond_food_df, alt_df

# -------------------
# TEMP UTILS (until Y finishes utils.py)
# -------------------
def normalize_text(t):
    """Simple text cleaner: lowercase + strip spaces"""
    return str(t).strip().lower()

def map_synonyms(t):
    """Dummy synonym mapper: just return input (expand later)"""
    return t
# -------------------
# 2. Core Functions
# -------------------
def check_medicine_food(medicines, ingredients, med_food_df):
    results = []
    for med in medicines:
        med_norm = normalize_text(med)
        for ing in ingredients:
            ing_norm = map_synonyms(normalize_text(ing))
            matches = med_food_df[
                (med_food_df["medicine"].str.lower() == med_norm) &
                (med_food_df["food"].str.lower() == ing_norm)
            ]
            for _, row in matches.iterrows():
                results.append({
                    "type": "medicine-food",
                    "medicine": med_norm,
                    "food": ing_norm,
                    "interaction": row["interaction"],
                    "warning": row["warning"],
                    "explanation": row["explanation"]
                })
    return results


def check_condition_food(conditions, ingredients, cond_food_df):
    results = []
    for cond in conditions:
        cond_norm = normalize_text(cond)
        for ing in ingredients:
            ing_norm = map_synonyms(normalize_text(ing))
            matches = cond_food_df[
                (cond_food_df["condition"].str.lower() == cond_norm) &
                (cond_food_df["food"].str.lower() == ing_norm)
            ]
            for _, row in matches.iterrows():
                results.append({
                    "type": "condition-food",
                    "condition": cond_norm,
                    "food": ing_norm,
                    "warning": row["warning"],
                    "explanation": row["explanation"]
                })
    return results


def suggest_alternatives(ingredients, alt_df):
    results = []
    for ing in ingredients:
        ing_norm = map_synonyms(normalize_text(ing))
        matches = alt_df[alt_df["food"].str.lower() == ing_norm]
        for _, row in matches.iterrows():
            results.append({
                "food": ing_norm,
                "alternative": row["safe_alternative"],
                "reason": row["reason"]
            })
    return results


# -------------------
# 3. Master Function
# -------------------
def analyze_input(medicines, ingredients, conditions):
    med_food_df, cond_food_df, alt_df = load_datasets()

    warnings = []
    warnings.extend(check_medicine_food(medicines, ingredients, med_food_df))
    warnings.extend(check_condition_food(conditions, ingredients, cond_food_df))
    alternatives = suggest_alternatives(ingredients, alt_df)

    return {
        "warnings": warnings,
        "alternatives": alternatives
    }


# -------------------
# 4. Quick Test Run
# -------------------
if __name__ == "__main__":
    # Example inputs
    medicines = ["Paracetamol"]
    ingredients = ["rice", "ghee", "laddu"]
    conditions = ["diabetes"]

    result = analyze_input(medicines, ingredients, conditions)

    print("⚠️ Warnings:")
    for w in result["warnings"]:
        print(f"- [{w['type']}] {w['food']} → {w['warning']} ({w['explanation']})")

    print("\n✅ Alternatives:")
    for alt in result["alternatives"]:
        print(f"- {alt['food']} → {alt['alternative']} ({alt['reason']})")
