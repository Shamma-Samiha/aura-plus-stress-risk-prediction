import pandas as pd

RAW_PATH = "data/raw/stress_raw.csv"
OUT_PATH = "data/processed/stress_clean.csv"

def main():
    df = pd.read_csv(RAW_PATH)

    # 1. Column rename (minor polish)
    rename_map = {
        "teacher_student_relationship": "teacher_relationship",
        "future_career_concerns": "career_concerns",
        "extracurricular_activities": "extracurriculars"
    }
    df = df.rename(columns=rename_map)

    # 2. Basic validation (clip out-of-range values)
    df["anxiety_level"] = df["anxiety_level"].clip(0, 21)
    df["self_esteem"] = df["self_esteem"].clip(0, 30)
    df["depression"] = df["depression"].clip(0, 27)

    likert_cols = [
        "sleep_quality", "breathing_problem", "noise_level",
        "living_conditions", "safety", "basic_needs",
        "academic_performance", "study_load",
        "teacher_relationship", "career_concerns",
        "social_support", "peer_pressure",
        "extracurriculars", "bullying", "headache", "blood_pressure"
    ]

    for col in likert_cols:
        if col in df.columns:
            df[col] = df[col].clip(1, 5)

    # 3. Save cleaned data
    df.to_csv(OUT_PATH, index=False)

    print("✅ Cleaned dataset saved to:", OUT_PATH)
    print("Final shape:", df.shape)

if __name__ == "__main__":
    main()
