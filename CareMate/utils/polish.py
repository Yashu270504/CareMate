import pandas as pd

def polish_dataset():
    # Load merged dataset
    df = pd.read_csv("data/final_dataset.csv")

    # Merge 'reason' into 'explanation' (if explanation is empty)
    df["explanation"] = df["explanation"].fillna(df["reason"])

    # Merge 'interaction' into 'warning' (keep one column)
    df["interaction"] = df["interaction"].fillna(df["warning"])

    # Standardize interaction values
    df["interaction"] = df["interaction"].str.lower().replace({
        "no major risk": "safe",
        "safe": "safe",
        "risky": "risky",
        "risk": "risky"
    })

    # Keep only the polished columns
    polished = df[[
        "type", "medicine", "condition", "food", 
        "interaction", "explanation", "safe_alternative"
    ]]

    # Save polished dataset
    output_file = "data/final_dataset_polished.csv"
    polished.to_csv(output_file, index=False)

    print("✅ Polishing complete!")
    print(f"Rows: {polished.shape[0]}, Columns: {polished.shape[1]}")
    print("\nColumns:", list(polished.columns))
    print("\nSample rows:\n", polished.head(10))

if __name__ == "__main__":
    polish_dataset()
