import pandas as pd

def clean_food_alternatives():
    # Load dataset
    df = pd.read_csv("data/food_alternatives.csv")

    # Clean all string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("unknown")
            df[col] = df[col].str.lower().str.strip()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Save cleaned file
    df.to_csv("data/food_alternatives_clean.csv", index=False)
    print("✅ Cleaned food_alternatives.csv → food_alternatives_clean.csv")
    print("Shape after cleaning:", df.shape)
    return df

if __name__ == "__main__":
    clean_food_alternatives()
