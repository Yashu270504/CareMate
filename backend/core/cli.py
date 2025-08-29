# cli_app.py  (Bluff Demo Mode)

def check_case(name, age, allergies, conditions, medicines, food):
    """
    Fake hardcoded engine with alternatives + fake trigger ingredients.
    """
    demo_rules = {
        # --- ❌ RISK cases ---
        ("peanuts", "peanut butter"): ("❌ RISK", "Peanut allergy detected.", "Oats porridge", ["peanuts"]),
        ("milk", "ice cream"): ("❌ RISK", "Milk allergy + dairy product.", "Fruit Salad", ["milk", "cream"]),
        ("soy", "soy sauce"): ("❌ RISK", "Soy allergy triggered.", "Lemon dressing", ["soybeans"]),
        ("warfarin", "spinach"): ("❌ RISK", "Warfarin interacts with Vitamin K (spinach).", "Cabbage", ["vitamin K foods"]),

        # --- ⚠ CAUTION cases ---
        ("diabetes", "brown bread"): ("⚠ CAUTION", "Bread may raise blood sugar.", "Multigrain oats", ["wheat"]),
        ("pregnancy", "green tea"): ("⚠ CAUTION", "Green tea not recommended in pregnancy.", "Chamomile tea", ["caffeine"]),
        ("kidney disease", "red meat"): ("⚠ CAUTION", "Red meat may strain kidneys.", "Boiled lentils", ["animal protein"]),

        # --- ✅ SAFE cases ---
        ("none", "oats"): ("✅ SAFE", "Oats are safe for most people.", "Continue with oats", []),
        ("none", "apple"): ("✅ SAFE", "Apple is a safe fruit choice.", "Any fruit salad", []),
        ("none", "rice"): ("✅ SAFE", "Rice is generally safe.", "Plain rice", []),
    }

    # Normalize inputs
    allergies = [a.strip().lower() for a in allergies if a.strip()]
    conditions = [c.strip().lower() for c in conditions if c.strip()]
    medicines = [m.strip().lower() for m in medicines if m.strip()]
    food = food.lower().strip()

    # Check against demo rules
    for key, (risk, reason, alternative, triggers) in demo_rules.items():
        if key[0] in allergies + conditions + medicines or key[0] == "none":
            if key[1] == food:
                return risk, reason, alternative, triggers

    # Default fallback
    return "✅ SAFE", "No conflicts found.", "Rice / Oats", []


def main():
    print("=== CareMate Bluff CLI (Demo Mode) ===\n")

    name = input("👤 Name: ")
    age = input("🎂 Age: ")
    allergies = input("🤧 Allergies (comma separated): ").lower().split(",")
    conditions = input("🩺 Conditions (comma separated): ").lower().split(",")
    medicines = input("💊 Medicines (comma separated): ").lower().split(",")
    food = input("🍽 Food eaten: ")

    # Run fake checker
    risk, reason, alternative, triggers = check_case(name, age, allergies, conditions, medicines, food)

    # Print Result
    print("\n--- RESULT ---")
    print(f"👤 {name}, Age {age}")
    print(f"🤧 Allergies: {', '.join(allergies) if any(allergies) else 'None'}")
    print(f"🩺 Conditions: {', '.join(conditions) if any(conditions) else 'None'}")
    print(f"💊 Medicines: {', '.join(medicines) if any(medicines) else 'None'}")
    print(f"🍽 Food: {food}")
    print(f"\nResult: {risk}")
    print(f"Reason: {reason}")

    if triggers:
        print(f"⚠ Trigger Ingredients: {', '.join(triggers)}")

    print(f"💡 Suggested Alternative: {alternative}")


if __name__ == "__main__":
    main()
