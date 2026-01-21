# src/data/03_eda_basics.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = "data/processed/stress_clean.csv"

def ensure_dirs():
    """
    Windows-safe directory creation.
    Avoids FileExistsError edge cases by checking existence explicitly.
    """
    reports_dir = Path("reports")
    figures_dir = reports_dir / "figures"

    reports_dir.mkdir(exist_ok=True)
    
    # Remove file if it exists (edge case handling)
    if figures_dir.exists() and figures_dir.is_file():
        figures_dir.unlink()
    
    figures_dir.mkdir(parents=True, exist_ok=True)

    return reports_dir, figures_dir

def main():
    reports_dir, figures_dir = ensure_dirs()

    df = pd.read_csv(DATA_PATH)

    # 1) Target distribution plot
    ax = df["stress_level"].value_counts().sort_index().plot(kind="bar")
    ax.set_title("Stress Level Distribution (0=Low, 1=Moderate, 2=High)")
    ax.set_xlabel("stress_level")
    ax.set_ylabel("count")
    plt.tight_layout()
    plt.savefig(figures_dir / "target_distribution.png")
    plt.close()

    # 2) Correlation with target (quick ranking)
    corr = df.corr(numeric_only=True)["stress_level"].sort_values(ascending=False)
    corr.to_csv(reports_dir / "stress_level_correlations.csv")

    top_pos = corr.head(10)
    top_neg = corr.tail(10)

    print("\n✅ Saved:", figures_dir / "target_distribution.png")
    print("✅ Saved:", reports_dir / "stress_level_correlations.csv")

    print("\n--- Top positively correlated with stress_level ---")
    print(top_pos)

    print("\n--- Top negatively correlated with stress_level ---")
    print(top_neg)

    # 3) Compare means by stress_level for a few key features
    key_features = [
        "anxiety_level",
        "depression",
        "self_esteem",
        "sleep_quality",
        "social_support",
        "peer_pressure",
    ]
    existing = [c for c in key_features if c in df.columns]

    group_means = df.groupby("stress_level")[existing].mean()
    group_means.to_csv(reports_dir / "group_means_by_stress_level.csv")

    print("\n✅ Saved:", reports_dir / "group_means_by_stress_level.csv")
    print("\n--- Group means (by stress_level) ---")
    print(group_means)

if __name__ == "__main__":
    main()
