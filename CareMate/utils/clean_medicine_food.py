import pandas as pd

def normalize_text(text):
    if pd.isna(text):  # handle missing values
        return "unknown"
    return str(text).lower().strip()

# Load dataset
df = pd.read_csv("data/medicine_food.csv")

# Clean key columns
df["medicine"] = df["medicine"].apply(normalize_text)
df["food"] = df["food"].apply(normalize_text)
if "warning" in df.columns:
    df["warning"] = df["warning"].apply(normalize_text)

# Drop duplicate rows
df = df.drop_duplicates()

# Save cleaned version
df.to_csv("data/medicine_food_clean.csv", index=False)

print("✅ Cleaning complete. New shape:", df.shape)


print("Rows, Columns:", df.shape)   # check size
print("Missing values:\n", df.isna().sum())  # see NaN counts
print("Duplicates:", df.duplicated().sum())  # check duplicates
print(df.sample(10))   # preview 10 random rows
