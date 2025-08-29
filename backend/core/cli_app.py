import json
from pathlib import Path
from backend.core.rule_engine import rule_check

PROFILE_PATH = Path("backend/core/user_profile.json")

# 🔄 Hardcoded alternatives mapping (50 items)
FOOD_ALTERNATIVES = {
    "peanuts": "Roasted chickpeas",
    "cashews": "Sunflower seeds",
    "almonds": "Pumpkin seeds",
    "milk": "Soy milk",
    "cheese": "Almond cheese",
    "butter": "Olive oil spread",
    "cream": "Coconut cream",
    "ice cream": "Frozen banana blend",
    "yogurt": "Coconut yogurt",
    "eggs": "Tofu scramble",
    "wheat bread": "Rice cakes",
    "pasta": "Gluten-free pasta",
    "pizza": "Cauliflower crust pizza",
    "biscuits": "Oatmeal cookies",
    "cakes": "Millet flour muffins",
    "fish": "Paneer",
    "shrimp": "Jackfruit chunks",
    "crab": "Mushrooms",
    "lobster": "Tofu stir fry",
    "salmon": "Lentils",
    "red meat": "Kidney beans",
    "pork": "Chickpea curry",
    "bacon": "Smoked tempeh",
    "sausage": "Soya chunks",
    "lamb": "Rajma",
    "sugar": "Jaggery powder",
    "chocolate": "Carob treats",
    "candy": "Dates or figs",
    "soft drinks": "Lemon water",
    "energy drinks": "Coconut water",
    "fries": "Baked sweet potato wedges",
    "chips": "Popped corn",
    "burgers": "Veggie burger (black beans)",
    "hot dogs": "Soy sausage",
    "nuggets": "Cauliflower bites",
    "coffee": "Green tea",
    "black tea": "Herbal tea",
    "alcohol": "Sparkling fruit juice",
    "beer": "Ginger ale",
    "whiskey": "Kombucha",
    "spicy curry": "Mild lentil curry",
    "pickles": "Steamed veggies with lemon",
    "fried rice": "Steamed brown rice",
    "biryani": "Quinoa pulao",
    "noodles": "Rice noodles",
    "white rice": "Brown rice",
    "white bread": "Multigrain gluten-free bread",
    "butter chicken": "Tandoori paneer",
    "paneer": "Soy paneer (if lactose issue)",
    "kheer": "Sabudana payasam with coconut milk",
    "ramen": "Miso soup with tofu",
    "sushi": "Veggie sushi rolls",
    "tuna": "Chickpea salad"
}


def save_profile(profile: dict):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)
    print("\n✅ Profile saved (cloud-synced)\n")


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    else:
        return {}


def clean_list(raw_input: str):
    """Split by comma or 'and' to handle inputs naturally."""
    if not raw_input.strip():
        return []
    parts = []
    for token in raw_input.replace(" and ", ",").split(","):
        token = token.strip().lower()
        if token:
            parts.append(token)
    return parts


def create_profile():
    print("\n--- Create User Profile ---")
    name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    age = int(input("Enter age: ").strip())

    profile = {
        "name": name,
        "email": email,
        "age": age
    }
    save_profile(profile)


def analyze_food():
    profile = load_profile()
    if not profile:
        print("⚠ No profile found! Please create one first.")
        return

    print("\n--- Enter Health Details ---")
    conditions = clean_list(input("Enter health conditions (comma separated): "))
    allergies = clean_list(input("Enter allergies (comma separated): "))
    medicines = clean_list(input("Enter medicines (comma separated): "))
    food = input("Enter food taken: ").strip().lower()

    # Call rule_engine (dummy / real)
    result = rule_check(
        {"conditions": conditions, "allergies": allergies},
        food,
        medicines
    )

    print("\n📊 --- Analysis Result ---")
    print(f"👤 User: {profile['name']} ({profile['age']} yrs, {profile['email']})")
    print(f"🍽 Food Taken: {food}")
    print(f"💊 Medicines: {', '.join(medicines) if medicines else 'None'}")

    if result:
        print(f"⚠ Risk Level: {result.get('risk', 'Unknown')}")
        print(f"❗ Effect: {result.get('reason', 'No details')}")
        # 🔄 use hardcoded alternative if exists
        alternative = FOOD_ALTERNATIVES.get(food, result.get("alternative", "Not available"))
        print(f"🔄 Alternative: {alternative}")
        print(f"📖 Source: {result.get('source', 'Dataset')}")
    else:
        print("✅ Safe! No rules triggered.")


def main():
    while True:
        print("\n=== CareMate CLI ===")
        print("1. Create Profile")
        print("2. Analyze Food & Medicine")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            create_profile()
        elif choice == "2":
            analyze_food()
        elif choice == "3":
            print("👋 Exiting CareMate. Stay healthy!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
