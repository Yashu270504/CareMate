import pandas as pd

def clean_condition_food():
    # Load dataset
    df = pd.read_csv("data/condition_food.csv")

    # Clean all string columns
    for col in df.columns:
        if df[col].dtype == "object":   # only text columns
            df[col] = df[col].fillna("unknown")
            df[col] = df[col].str.lower().str.strip()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Save cleaned file
    df.to_csv("data/condition_food_clean.csv", index=False)
    print("✅ Cleaned condition_food.csv → condition_food_clean.csv")
    print("Shape after cleaning:", df.shape)
    return df

if __name__ == "__main__":
    clean_condition_food()
