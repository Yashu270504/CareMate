import re

# ---------- Text Normalization ----------
def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).strip().lower()

# ---------- Synonym Mapping ----------
SYNONYMS = {
    "tomatoes": "tomato",
    "sugars": "sugar",
    "potatoes": "potato",
    "peanuts": "peanut"
}

def map_synonyms(word: str) -> str:
    word = normalize_text(word)
    return SYNONYMS.get(word, word)

# ---------- Ingredient Extraction ----------
def extract_ingredients(recipe_text: str):
    recipe_text = normalize_text(recipe_text)
    words = recipe_text.split(",")  # split on commas
    return [map_synonyms(w.strip()) for w in words if w.strip()]

# ---------- Watsonx.ai Simplifier ----------
def simplify_text(text: str) -> str:
    """
    Stub for IBM Watsonx.ai integration.
    Replace with actual API call later.
    """
    return f"Simplified: {text}"

if __name__ == "__main__":
    print(extract_ingredients("Tomatoes, sugar, peanuts"))
    print(simplify_text("Alcohol may cause hepatotoxicity with paracetamol."))
