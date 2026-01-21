import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

MODEL_PATH = Path("models/baseline_logistic_model.joblib")
DATA_PATH = Path("data/processed/stress_clean.csv")

STRESS_LABELS = {0: "Low", 1: "Moderate", 2: "High"}

# ---------- Human-friendly question map ----------
# label: what user sees
# help: small explanation under the widget
# scale_text: shown near the scale (optional)
QUESTION_MAP = {
    "anxiety_level": {
        "label": "Anxiety level (0–21)",
        "help": "How anxious or worried have you felt recently? Higher = more anxiety.",
    },
    "depression": {
        "label": "Depression-related symptoms (0–27)",
        "help": "How often have you felt low mood / loss of interest recently? Higher = more symptoms.",
    },
    "self_esteem": {
        "label": "Self-esteem (0–30)",
        "help": "How positively do you feel about yourself overall? Higher = stronger self-esteem.",
    },
    "mental_health_history": {
        "label": "Prior mental health difficulties",
        "help": "Have you experienced mental health difficulties in the past? (This does not define you.)",
    },
    "sleep_quality": {
        "label": "Sleep quality (1–5)",
        "help": "1 = very poor sleep, 5 = very good sleep.",
    },
    "study_load": {
        "label": "Study load (1–5)",
        "help": "How heavy does your current study workload feel? 1 = light, 5 = overwhelming.",
    },
    "peer_pressure": {
        "label": "Peer pressure (1–5)",
        "help": "How much pressure do you feel from friends/peers? 1 = none, 5 = extreme.",
    },
    "career_concerns": {
        "label": "Future / career concerns (1–5)",
        "help": "How worried are you about your future or career? 1 = not worried, 5 = very worried.",
    },
    "social_support": {
        "label": "Social support (1–5)",
        "help": "Do you feel supported by people around you? 1 = not supported, 5 = very supported.",
    },
    "bullying": {
        "label": "Bullying experiences (1–5)",
        "help": "1 = none, 5 = frequent/serious. If you feel unsafe, consider reaching out for help.",
    },
    "noise_level": {
        "label": "Noise in your environment (1–5)",
        "help": "How noisy is your daily environment? 1 = quiet, 5 = very noisy.",
    },
    "living_conditions": {
        "label": "Living conditions (1–5)",
        "help": "1 = very difficult, 5 = very comfortable.",
    },
    "safety": {
        "label": "Feeling safe (1–5)",
        "help": "1 = not safe, 5 = very safe.",
    },
    "basic_needs": {
        "label": "Basic needs met (1–5)",
        "help": "Food, rest, essentials. 1 = not met, 5 = fully met.",
    },
    "academic_performance": {
        "label": "Academic performance satisfaction (1–5)",
        "help": "How satisfied are you with your academic performance? 1 = not satisfied, 5 = very satisfied.",
    },
    "teacher_relationship": {
        "label": "Teacher relationship quality (1–5)",
        "help": "1 = poor, 5 = very supportive.",
    },
    "headache": {
        "label": "Headache frequency (1–5)",
        "help": "1 = rarely, 5 = very often.",
    },
    "blood_pressure": {
        "label": "Blood pressure concerns (1–5)",
        "help": "1 = none, 5 = frequent concerns. Not medical advice; consult a professional if worried.",
    },
    "breathing_problem": {
        "label": "Breathing discomfort (1–5)",
        "help": "1 = none, 5 = frequent discomfort.",
    },
    "extracurriculars": {
        "label": "Extracurricular load (1–5)",
        "help": "How busy are you with activities beyond study? 1 = low, 5 = very busy.",
    },
}

# Suggestions mapped to key features (safe, general)
SUGGESTION_RULES = {
    "study_load": "Try splitting study into smaller blocks (e.g., 25 minutes focus + 5 minutes break) and plan the next 1–2 days only.",
    "sleep_quality": "Aim for a consistent sleep schedule. Reduce screens 30–60 minutes before bed and keep caffeine earlier in the day.",
    "peer_pressure": "Practice setting boundaries. A helpful phrase: “I can’t do that right now, but thank you for understanding.”",
    "career_concerns": "Write down worries, then convert them into 1–2 small actions (update resume, talk to a mentor, choose one skill to improve).",
    "bullying": "If bullying is present, consider speaking to a trusted person or counselor. If you feel unsafe, seek immediate help locally.",
    "noise_level": "Try a quieter space, headphones/earplugs, or soft background noise (white noise) to improve focus and calm.",
    "extracurriculars": "If your schedule feels overloaded, reduce commitments temporarily and protect recovery time.",
    "headache": "Hydrate, take short screen breaks, and check posture. If headaches are persistent, consider medical advice.",
    "blood_pressure": "Slow breathing (4 seconds in, 6 seconds out for 2–3 minutes) may help. Seek medical advice if you’re concerned.",
    "social_support": "Consider reaching out to someone you trust. Even one supportive conversation can help reduce stress load.",
    "safety": "If safety feels low, prioritize reaching out to trusted support or local services. Your safety matters first.",
    "basic_needs": "Focus on basics first: regular meals, hydration, and rest. Stress management works better when needs are met.",
}

# ---------- Utilities ----------
def load_model():
    if not MODEL_PATH.exists():
        st.error("Model file not found. Train the baseline model first: python src/models/01_train_baseline.py")
        st.stop()
    return joblib.load(MODEL_PATH)

def get_feature_names():
    if not DATA_PATH.exists():
        st.error("Processed dataset not found. Run cleaning step first.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    return [c for c in df.columns if c != "stress_level"]

def explain_with_coefficients(pipeline, user_df, feature_names, top_k=6):
    """
    Contribution approximation for a scaled logistic regression:
    contribution ~= scaled_value * coefficient_for_predicted_class
    """
    scaler = pipeline.named_steps["scaler"]
    model = pipeline.named_steps["model"]

    x_scaled = scaler.transform(user_df[feature_names])
    pred_class = int(model.predict(user_df[feature_names])[0])

    coef = model.coef_[pred_class]
    contributions = x_scaled.flatten() * coef

    expl = pd.Series(contributions, index=feature_names).sort_values(key=np.abs, ascending=False)
    return pred_class, expl.head(top_k)

def format_feature_name(feat: str) -> str:
    # Prefer question map label, else prettify raw name
    if feat in QUESTION_MAP:
        return QUESTION_MAP[feat]["label"]
    return feat.replace("_", " ").title()

def make_report_text(pred_label, probs, top_contrib, suggestions):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("AURA+ — Stress Risk Screening Report")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("Disclaimer: This report is educational and not a medical diagnosis.")
    lines.append("")
    lines.append(f"Predicted risk level: {pred_label}")
    lines.append(f"Model confidence (approx.): Low={probs[0]:.2f}, Moderate={probs[1]:.2f}, High={probs[2]:.2f}")
    lines.append("")
    lines.append("Top contributing factors (largest impact first):")
    for feat, val in top_contrib.items():
        direction = "increases risk" if val > 0 else "reduces risk"
        lines.append(f"- {format_feature_name(feat)}: {direction} (score={val:.3f})")
    lines.append("")
    lines.append("General suggestions (not medical advice):")
    if suggestions:
        for s in suggestions:
            lines.append(f"- {s}")
    else:
        lines.append("- Maintain healthy routines and seek support when needed.")
    lines.append("")
    lines.append("If you feel unsafe or at risk of self-harm, seek immediate local emergency help.")
    return "\n".join(lines)

# ---------- UI ----------
st.set_page_config(page_title="AURA+ Stress Risk Screener", page_icon="🧠", layout="centered")
st.title("🧠 AURA+ — Stress Risk Screening")
st.caption("Educational screening tool (not a diagnosis).")

with st.expander("⚠️ Disclaimer", expanded=True):
    st.write(
        "AURA+ provides an educational estimate of stress risk based on questionnaire inputs. "
        "It is **not** medical advice and **not** a clinical diagnosis. "
        "If you feel unsafe or are at risk of self-harm, please seek immediate local emergency help or contact a trusted person."
    )

model = load_model()
feature_names = get_feature_names()

st.subheader("1) Answer a few questions")

# Defaults (reasonable midpoints)
defaults = {
    "anxiety_level": 10,
    "self_esteem": 15,
    "mental_health_history": 0,
    "depression": 10,
    "headache": 2,
    "blood_pressure": 2,
    "sleep_quality": 3,
    "breathing_problem": 2,
    "noise_level": 3,
    "living_conditions": 3,
    "safety": 3,
    "basic_needs": 3,
    "academic_performance": 3,
    "study_load": 3,
    "teacher_relationship": 3,
    "career_concerns": 3,
    "social_support": 3,
    "peer_pressure": 3,
    "extracurriculars": 3,
    "bullying": 1,
}

ranges = {
    "anxiety_level": (0, 21),
    "self_esteem": (0, 30),
    "depression": (0, 27),
}

user_input = {}
cols = st.columns(2)

for i, feat in enumerate(feature_names):
    col = cols[i % 2]
    meta = QUESTION_MAP.get(feat, {})
    label = meta.get("label", feat.replace("_", " ").title())
    help_text = meta.get("help", "")

    if feat == "mental_health_history":
        user_input[feat] = col.selectbox(
            label,
            options=[0, 1],
            index=defaults.get(feat, 0),
            help=help_text
        )
    elif feat in ranges:
        lo, hi = ranges[feat]
        user_input[feat] = col.slider(
            label,
            min_value=int(lo),
            max_value=int(hi),
            value=int(defaults.get(feat, (lo + hi) // 2)),
            help=help_text
        )
    else:
        user_input[feat] = col.slider(
            label,
            min_value=1,
            max_value=5,
            value=int(defaults.get(feat, 3)),
            help=help_text
        )

user_df = pd.DataFrame([user_input])

st.subheader("2) See your result")

if st.button("Predict Stress Risk"):
    pred = int(model.predict(user_df[feature_names])[0])
    proba = model.predict_proba(user_df[feature_names])[0]
    pred_label = STRESS_LABELS[pred]

    # More human, safer phrasing
    if pred == 0:
        headline = "✅ Your responses suggest a **Low** stress risk right now."
        tone = "Keep maintaining healthy routines and support systems."
    elif pred == 1:
        headline = "⚠️ Your responses suggest a **Moderate** stress risk."
        tone = "A few areas may be contributing to stress—small adjustments can help."
    else:
        headline = "🚨 Your responses suggest a **High** stress risk."
        tone = "Consider prioritizing support and recovery. If you feel unsafe, seek help immediately."

    st.markdown(f"### {headline}")
    st.write(tone)
    st.caption(f"Model confidence (approx.): Low={proba[0]:.2f}, Moderate={proba[1]:.2f}, High={proba[2]:.2f}")

    st.subheader("3) Why this result? (high-level)")
    pred_class, top_contrib = explain_with_coefficients(model, user_df, feature_names, top_k=6)

    # Turn contributions into friendly text
    expl_table = top_contrib.reset_index()
    expl_table.columns = ["Feature", "Contribution"]
    expl_table["Feature"] = expl_table["Feature"].apply(format_feature_name)
    expl_table["Direction"] = expl_table["Contribution"].apply(lambda x: "Increases risk" if x > 0 else "Reduces risk")
    expl_table["Contribution"] = expl_table["Contribution"].round(3)

    st.write(
        "This section highlights the **strongest signals** that influenced the prediction. "
        "It’s not a diagnosis—just an explanation of what the model noticed."
    )
    st.dataframe(expl_table[["Feature", "Direction", "Contribution"]], use_container_width=True)

    st.subheader("4) Suggestions to reduce risk (general)")
    suggested_texts = []
    for feat in top_contrib.index:
        if feat in SUGGESTION_RULES:
            suggested_texts.append(SUGGESTION_RULES[feat])

    # Deduplicate while preserving order
    seen = set()
    suggested_texts = [s for s in suggested_texts if not (s in seen or seen.add(s))]

    if not suggested_texts:
        st.write("No strong risk drivers detected. Maintain healthy routines and seek support when needed.")
    else:
        for s in suggested_texts[:5]:
            st.write(f"- {s}")

    st.info("If symptoms feel overwhelming or persistent, consider speaking with a qualified professional or trusted support person.")

    # Optional download report
    report_text = make_report_text(pred_label, proba, top_contrib, suggested_texts[:5])
    st.download_button(
        label="⬇️ Download your report (TXT)",
        data=report_text,
        file_name="aura_plus_stress_report.txt",
        mime="text/plain",
    )
