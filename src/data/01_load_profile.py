import pandas as pd

PATH = "data/raw/stress_raw.csv"

def main():
    df = pd.read_csv(PATH)

    print("\n✅ Loaded:", PATH)
    print("Shape (rows, cols):", df.shape)

    print("\n--- Columns ---")
    print(df.columns.tolist())

    print("\n--- First 5 rows ---")
    print(df.head())

    print("\n--- Data types ---")
    print(df.dtypes)

    print("\n--- Missing values (top 15) ---")
    missing = df.isna().sum().sort_values(ascending=False)
    print(missing.head(15))

    # Target distribution
    if "stress_level" in df.columns:
        print("\n--- Target distribution: stress_level ---")
        print(df["stress_level"].value_counts(dropna=False).sort_index())
    else:
        print("\n⚠️ Target column 'stress_level' not found. Check column names.")

    # Quick stats (for numeric columns)
    print("\n--- Numeric summary (quick) ---")
    print(df.describe().T.head(15))

if __name__ == "__main__":
    main()
