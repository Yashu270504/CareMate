import pandas as pd

def merge_datasets():
    # Load datasets
    medicine_food = pd.read_csv("data/medicine_food_clean.csv")
    condition_food = pd.read_csv("data/condition_food_clean.csv")
    food_alternatives = pd.read_csv("data/food_alternatives_clean.csv")

    # Add source type column
    medicine_food["type"] = "medicine"
    condition_food["type"] = "condition"
    food_alternatives["type"] = "alternative"

    # Collect all unique columns
    all_columns = set(medicine_food.columns) | set(condition_food.columns) | set(food_alternatives.columns)

    # Reindex to align all datasets (missing values filled as NaN)
    medicine_food = medicine_food.reindex(columns=all_columns)
    condition_food = condition_food.reindex(columns=all_columns)
    food_alternatives = food_alternatives.reindex(columns=all_columns)

    # Merge into one unified dataset
    final_dataset = pd.concat([medicine_food, condition_food, food_alternatives], ignore_index=True)

    # Save to CSV
    output_file = "data/final_dataset.csv"
    final_dataset.to_csv(output_file, index=False)

    # Print stats + preview
    print("✅ Merge complete!")
    print(f"Rows: {final_dataset.shape[0]}, Columns: {final_dataset.shape[1]}")
    print("\nColumns:", list(final_dataset.columns))
    print("\nSample rows:\n", final_dataset.head(10))

if __name__ == "__main__":
    merge_datasets()
