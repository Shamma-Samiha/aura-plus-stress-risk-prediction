# AURA+ — Mental Health Stress Risk Prediction

AURA+ is a machine learning–based system designed to analyze psychological,
academic, and social factors to assess **stress risk levels** and provide
actionable insights.

⚠️ **Disclaimer:**  
This project is for educational and screening purposes only and does not provide
medical or clinical diagnoses.

---

## Dataset
- Source: Kaggle (Student Stress Level Dataset)
- Records: 1,100
- Features: 20
- Target: `stress_level` (0 = Low, 1 = Moderate, 2 = High)

---

## Project Structure

AURA-plus/
├── data/
│ ├── raw/ # ignored (Kaggle data)
│ └── processed/ # cleaned dataset
├── notebooks/ # EDA & experiments
├── src/
│ ├── data/ # data loading & cleaning
│ ├── features/ # feature engineering
│ ├── models/ # model training
│ └── app/ # Streamlit app
├── reports/ # analysis outputs
├── requirements.txt
└── README.md


---

## Key Insights (EDA)
- Anxiety and depression show strong positive associations with stress level
- Self-esteem and sleep quality decline as stress increases
- Peer pressure, study load, and career concerns are major contributors
- Social support acts as a protective factor

---

## Tech Stack
- Python
- pandas, NumPy
- scikit-learn
- matplotlib, seaborn
- Streamlit (deployment planned)

---

## Model Selection

A logistic regression baseline achieved an accuracy of 88% with balanced
performance across all stress levels. Although a Random Forest model was also
evaluated, it did not outperform the baseline and introduced additional
misclassification of low-stress cases.

Given its superior performance, interpretability, and stability, logistic
regression was selected as the final model for deployment.

