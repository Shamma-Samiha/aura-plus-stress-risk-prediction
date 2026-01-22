import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

MODEL_PATH = Path("models/baseline_logistic_model.joblib")
DATA_PATH = Path("data/processed/stress_clean.csv")

STRESS_LABELS = {0: "Low", 1: "Moderate", 2: "High"}

# --------- Styling helpers ----------
BADGE_STYLES = {
    0: {"bg_dark": "#0f2f1d", "fg_dark": "#7CFFB2", "border_dark": "#1f7a49", "bg_light": "#e6ffef", "fg_light": "#1b5e20", "border_light": "#81c784", "emoji": "✅"},
    1: {"bg_dark": "#2b2412", "fg_dark": "#FFD37C", "border_dark": "#b27a1f", "bg_light": "#fff9e6", "fg_light": "#795548", "border_light": "#ffd54f", "emoji": "⚠️"},
    2: {"bg_dark": "#2a1414", "fg_dark": "#FF8A8A", "border_dark": "#a83a3a", "bg_light": "#ffebee", "fg_light": "#b71c1c", "border_light": "#ef9a9a", "emoji": "🚨"},
}

# --------- Human-friendly question map ----------
QUESTION_MAP = {
    "anxiety_level": {
        "label": "Anxiety level (0–21)",
        "help": "Higher means more anxiety or worry recently.",
        "section": "Psychological",
        "type": "range",
        "min": 0,
        "max": 21,
        "default": 10,
    },
    "depression": {
        "label": "Depression-related symptoms (0–27)",
        "help": "Higher means more low mood / loss of interest recently.",
        "section": "Psychological",
        "type": "range",
        "min": 0,
        "max": 27,
        "default": 10,
    },
    "self_esteem": {
        "label": "Self-esteem (0–30)",
        "help": "Higher means stronger confidence and self-worth.",
        "section": "Psychological",
        "type": "range",
        "min": 0,
        "max": 30,
        "default": 15,
    },
    "mental_health_history": {
        "label": "Prior mental health difficulties",
        "help": "0 = No, 1 = Yes. This is not a label—just context.",
        "section": "Psychological",
        "type": "binary",
        "default": 0,
    },
    "headache": {
        "label": "Headache frequency (1–5)",
        "help": "1 = rarely, 5 = very often.",
        "section": "Physical",
        "type": "likert",
        "default": 2,
    },
    "blood_pressure": {
        "label": "Blood pressure concerns (1–5)",
        "help": "1 = none, 5 = frequent concerns. Not medical advice.",
        "section": "Physical",
        "type": "likert",
        "default": 2,
    },
    "breathing_problem": {
        "label": "Breathing discomfort (1–5)",
        "help": "1 = none, 5 = frequent discomfort.",
        "section": "Physical",
        "type": "likert",
        "default": 2,
    },
    "sleep_quality": {
        "label": "Sleep quality (1–5)",
        "help": "1 = very poor sleep, 5 = very good sleep.",
        "section": "Sleep",
        "type": "likert",
        "default": 3,
    },
    "noise_level": {
        "label": "Noise in your environment (1–5)",
        "help": "1 = quiet, 5 = very noisy.",
        "section": "Environment",
        "type": "likert",
        "default": 3,
    },
    "living_conditions": {
        "label": "Living conditions (1–5)",
        "help": "1 = very difficult, 5 = very comfortable.",
        "section": "Environment",
        "type": "likert",
        "default": 3,
    },
    "safety": {
        "label": "Feeling safe (1–5)",
        "help": "1 = not safe, 5 = very safe.",
        "section": "Environment",
        "type": "likert",
        "default": 3,
    },
    "basic_needs": {
        "label": "Basic needs met (1–5)",
        "help": "Food/rest/essentials. 1 = not met, 5 = fully met.",
        "section": "Environment",
        "type": "likert",
        "default": 3,
    },
    "academic_performance": {
        "label": "Academic satisfaction (1–5)",
        "help": "How satisfied are you with your academic performance?",
        "section": "Academic",
        "type": "likert",
        "default": 3,
    },
    "study_load": {
        "label": "Study load (1–5)",
        "help": "1 = light, 5 = overwhelming.",
        "section": "Academic",
        "type": "likert",
        "default": 3,
    },
    "teacher_relationship": {
        "label": "Teacher relationship quality (1–5)",
        "help": "1 = poor, 5 = very supportive.",
        "section": "Academic",
        "type": "likert",
        "default": 3,
    },
    "career_concerns": {
        "label": "Future / career concerns (1–5)",
        "help": "1 = not worried, 5 = very worried.",
        "section": "Academic",
        "type": "likert",
        "default": 3,
    },
    "social_support": {
        "label": "Social support (1–5)",
        "help": "1 = not supported, 5 = very supported.",
        "section": "Social",
        "type": "likert",
        "default": 3,
    },
    "peer_pressure": {
        "label": "Peer pressure (1–5)",
        "help": "1 = none, 5 = extreme.",
        "section": "Social",
        "type": "likert",
        "default": 3,
    },
    "bullying": {
        "label": "Bullying experiences (1–5)",
        "help": "1 = none, 5 = frequent/serious.",
        "section": "Social",
        "type": "likert",
        "default": 1,
    },
    "extracurriculars": {
        "label": "Extracurricular load (1–5)",
        "help": "1 = low, 5 = very busy.",
        "section": "Social",
        "type": "likert",
        "default": 3,
    },
}

# Suggestions mapped to key drivers (safe, general)
SUGGESTION_RULES = {
    "study_load": "Split study into smaller blocks (25/5 or 50/10). Plan the next 1–2 days only, not the whole week.",
    "sleep_quality": "Keep a consistent bedtime, reduce screens before sleep, and avoid late caffeine.",
    "peer_pressure": "Practice boundaries: “I can’t do that right now.” Choose priorities that match your goals.",
    "career_concerns": "Write down worries, then choose 1 small action (resume update, talk to a mentor, learn one skill).",
    "bullying": "If bullying is present, consider speaking to a trusted person/counselor. If unsafe, seek immediate help locally.",
    "noise_level": "Try a quieter space, earplugs/headphones, or white noise while studying.",
    "extracurriculars": "Reduce commitments temporarily and protect recovery time. ‘Less but consistent’ beats overload.",
    "headache": "Hydrate, take short screen breaks, and check posture. If persistent, consider professional advice.",
    "blood_pressure": "Slow breathing (4 in, 6 out for 2–3 min) can help. Seek medical advice if concerned.",
    "social_support": "Reach out to one trusted person. Even one supportive conversation can reduce stress load.",
    "safety": "If safety is low, prioritize reaching out to trusted support or local services first.",
    "basic_needs": "Start with basics: meals, hydration, rest. Stress strategies work better when needs are met.",
}

# ---------- Utilities ----------
def load_model():
    if not MODEL_PATH.exists():
        st.error("Model file not found. Train baseline first: python src/models/01_train_baseline.py")
        st.stop()
    return joblib.load(MODEL_PATH)

def get_feature_names():
    if not DATA_PATH.exists():
        st.error("Processed dataset not found. Run cleaning first.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    return [c for c in df.columns if c != "stress_level"]

def explain_with_coefficients(pipeline, user_df, feature_names, top_k=6):
    scaler = pipeline.named_steps["scaler"]
    model = pipeline.named_steps["model"]

    x_scaled = scaler.transform(user_df[feature_names])
    pred_class = int(model.predict(user_df[feature_names])[0])

    coef = model.coef_[pred_class]
    contributions = x_scaled.flatten() * coef
    expl = pd.Series(contributions, index=feature_names).sort_values(key=np.abs, ascending=False)
    return pred_class, expl.head(top_k)

def format_feature_label(feat: str) -> str:
    meta = QUESTION_MAP.get(feat)
    if meta:
        return meta["label"]
    return feat.replace("_", " ").title()

def risk_badge_html(level_int: int, theme: str = "dark") -> str:
    style = BADGE_STYLES[level_int]
    label = STRESS_LABELS[level_int]
    bg = style[f'bg_{theme}']
    fg = style[f'fg_{theme}']
    border = style[f'border_{theme}']
    
    return f"""
    <div style="
        display:inline-flex;
        align-items:center;
        gap:10px;
        padding:12px 18px;
        border-radius:12px;
        background:{bg};
        color:{fg};
        border:1px solid {border};
        font-weight:700;
        font-size:16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        ">
        <span style="font-size:20px;">{style['emoji']}</span>
        <span>Risk level: {label}</span>
    </div>
    """

def make_report_text(pred_label, probs, top_contrib, suggestions):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("AURA+ — Stress Risk Screening Report")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("Disclaimer: Educational screening only; not a diagnosis or medical advice.")
    lines.append("")
    lines.append(f"Predicted risk level: {pred_label}")
    lines.append(f"Model confidence (approx.): Low={probs[0]:.2f}, Moderate={probs[1]:.2f}, High={probs[2]:.2f}")
    lines.append("")
    lines.append("Top contributing factors:")
    for feat, val in top_contrib.items():
        direction = "increases risk" if val > 0 else "reduces risk"
        lines.append(f"- {format_feature_label(feat)}: {direction} (score={val:.3f})")
    lines.append("")
    lines.append("General suggestions:")
    if suggestions:
        for s in suggestions:
            lines.append(f"- {s}")
    else:
        lines.append("- Maintain healthy routines and seek support when needed.")
    lines.append("")
    lines.append("If you feel unsafe or at risk of self-harm, seek immediate local emergency help.")
    return "\n".join(lines)

def set_defaults(feature_names):
    # Store in session_state for reset + persistence
    for feat in feature_names:
        meta = QUESTION_MAP.get(feat, {})
        default = meta.get("default", 3)
        st.session_state[f"inp_{feat}"] = default

# ---------- Page config ----------
st.set_page_config(page_title="AURA+ Stress Risk Screening", page_icon="🧠", layout="wide")

# ---------- Theme & CSS ----------
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

def apply_custom_styles(theme):
    if theme == "dark":
        primary = "#FF4B4B"
        bg_main = "#0a0e1a"
        bg_card = "rgba(30, 35, 50, 0.6)"
        bg_card_hover = "rgba(40, 45, 60, 0.8)"
        text_main = "#ffffff"
        text_secondary = "#b0b8c4"
        glow = "rgba(255, 75, 75, 0.4)"
        border_color = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "auto"
    else:
        primary = "#FF4B4B"
        bg_main = "#f8fafc"
        bg_card = "#ffffff"
        bg_card_hover = "#fef2f2"
        text_main = "#1e293b"
        text_secondary = "#64748b"
        glow = "rgba(255, 75, 75, 0.3)"
        border_color = "rgba(226, 232, 240, 1)"
        sidebar_bg = "#ffffff"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        .stApp {{
            background: {bg_main};
            color: {text_main};
        }}
        
        /* Smooth background gradient */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: {'radial-gradient(circle at 20% 50%, rgba(255, 75, 75, 0.05) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.05) 0%, transparent 50%)' if theme == 'dark' else 'radial-gradient(circle at 30% 20%, rgba(255, 75, 75, 0.06) 0%, transparent 40%), radial-gradient(circle at 70% 80%, rgba(138, 43, 226, 0.05) 0%, transparent 40%)'};
            pointer-events: none;
            z-index: 0;
        }}
        
        .block-container {{ 
            padding-top: 3rem; 
            padding-bottom: 4rem; 
            max-width: 1100px;
            position: relative;
            z-index: 1;
        }}
        
        /* Modern Header with enhanced gradient */
        .main-header {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 50%, #FF8A8A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.3rem;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}
        
        /* Enhanced Buttons */
        div.stButton > button {{
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px {glow}, 0 2px 8px rgba(0, 0, 0, 0.1);
            text-transform: none;
            letter-spacing: 0.3px;
            width: 100%;
            position: relative;
            overflow: hidden;
        }}
        
        div.stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }}
        
        div.stButton > button:hover::before {{
            left: 100%;
        }}
        
        div.stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 30px {glow}, 0 4px 12px rgba(0, 0, 0, 0.15);
            background: linear-gradient(135deg, #FF6B6B 0%, #FF4B4B 100%);
        }}
        
        div.stButton > button:active {{
            transform: translateY(-1px);
            box-shadow: 0 4px 20px {glow};
        }}
        
        /* Primary button special styling */
        div.stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
            font-size: 1.05rem;
            padding: 0.9rem 2.5rem;
            box-shadow: 0 6px 25px {glow}, 0 3px 10px rgba(0, 0, 0, 0.15);
        }}
        
        /* Enhanced Expanders */
        .streamlit-expanderHeader {{
            background: {bg_card} !important;
            border-radius: 12px !important;
            border: 1px solid {border_color} !important;
            margin-bottom: 8px;
            padding: 1rem 1.25rem !important;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            {'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);' if theme == 'light' else ''}
        }}
        
        /* When expander is open/selected */
        .streamlit-expanderHeader[aria-expanded="true"],
        .streamlit-expanderHeader[aria-expanded="true"]:hover {{
            background: {'#f1f5f9' if theme == 'light' else 'rgba(50, 55, 70, 0.8)'} !important;
            border-color: {'rgba(203, 213, 225, 1)' if theme == 'light' else 'rgba(255, 255, 255, 0.15)'} !important;
            {'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), 0 2px 4px rgba(0, 0, 0, 0.04);' if theme == 'light' else ''}
        }}
        
        .streamlit-expanderHeader:hover {{
            background: {bg_card_hover} !important;
            border-color: {'rgba(255, 75, 75, 0.4)' if theme == 'light' else 'rgba(255, 75, 75, 0.3)'} !important;
            transform: translateX(4px);
            {'box-shadow: 0 6px 16px rgba(255, 75, 75, 0.08), 0 2px 6px rgba(0, 0, 0, 0.04);' if theme == 'light' else ''}
        }}
        
        .streamlit-expanderContent {{
            background: {bg_card} !important;
            border-radius: 0 0 12px 12px !important;
            border: 1px solid {border_color} !important;
            border-top: none !important;
            padding: 1.5rem 1.25rem !important;
            backdrop-filter: blur(10px);
            {'box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) inset;' if theme == 'light' else ''}
        }}
        
        /* Custom Card Style for Results */
        .result-card {{
            background: {bg_card};
            padding: 2.5rem;
            border-radius: 20px;
            border: 1px solid {border_color};
            backdrop-filter: blur(20px);
            margin: 1.5rem 0;
            box-shadow: {'0 8px 32px rgba(0, 0, 0, 0.3)' if theme == 'dark' else '0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.1)'};
            transition: all 0.3s ease;
        }}
        
        .result-card:hover {{
            transform: translateY(-2px);
            box-shadow: {'0 12px 40px rgba(0, 0, 0, 0.4)' if theme == 'dark' else '0 8px 30px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08)'};
        }}
        
        /* Enhanced Sliders */
        .stSlider > div > div > div {{
            background: linear-gradient(90deg, #FF4B4B, #FF6B6B);
            {'box-shadow: 0 2px 4px rgba(255, 75, 75, 0.2);' if theme == 'light' else ''}
        }}
        
        .stSlider > div > div > div:hover {{
            {'box-shadow: 0 4px 8px rgba(255, 75, 75, 0.3);' if theme == 'light' else ''}
        }}
        
        /* Better Selectbox styling */
        .stSelectbox > div > div {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 10px;
            transition: all 0.3s ease;
            {'box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);' if theme == 'light' else ''}
        }}
        
        .stSelectbox > div > div:hover {{
            border-color: rgba(255, 75, 75, 0.4);
            box-shadow: {'0 2px 8px ' + glow if theme == 'dark' else '0 4px 12px rgba(255, 75, 75, 0.15), 0 1px 3px rgba(0, 0, 0, 0.1)'};
            {'transform: translateY(-1px);' if theme == 'light' else ''}
        }}
        
        /* Section headers */
        h3 {{
            color: {text_main};
            font-weight: 700;
            font-size: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
        }}
        
        /* Subheaders */
        h2 {{
            color: {text_main};
            font-weight: 700;
            font-size: 1.8rem;
            margin-top: 2rem;
            margin-bottom: 1.25rem;
            letter-spacing: -0.01em;
        }}
        
        /* Captions */
        .stCaption {{
            color: {text_secondary};
            font-size: 0.9rem;
        }}
        
        /* Dividers */
        hr {{
            border: none;
            height: 1px;
            background: {'linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent)' if theme == 'light' else f'linear-gradient(90deg, transparent, {border_color}, transparent)'};
            margin: 2rem 0;
        }}
        
        /* Info boxes */
        .stInfo {{
            background: {bg_card};
            border-left: 4px solid #FF4B4B;
            border-radius: 8px;
            padding: 1rem;
            {'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);' if theme == 'light' else ''}
        }}
        
        /* Sidebar enhancements */
        .css-1d391kg {{
            background: {sidebar_bg if theme == 'light' else bg_card};
            {'box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05), 1px 0 3px rgba(0, 0, 0, 0.03);' if theme == 'light' else ''}
        }}
        
        [data-testid="stSidebar"] {{
            background: {sidebar_bg if theme == 'light' else 'auto'};
            {'box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05), 1px 0 3px rgba(0, 0, 0, 0.03);' if theme == 'light' else ''}
        }}
        
        /* Toggle styling */
        .stToggle {{
            background: {bg_card};
            border-radius: 10px;
            padding: 0.5rem;
            {'box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);' if theme == 'light' else ''}
        }}
        
        /* Toggle switch visibility - fix for light mode */
        .stToggle label {{
            color: {text_main} !important;
        }}
        
        /* Toggle switch track - multiple selectors for compatibility */
        .stToggle [data-baseweb="switch"],
        .stToggle button[data-baseweb="switch"],
        [data-testid="stToggle"] [data-baseweb="switch"],
        [data-testid="stToggle"] button[data-baseweb="switch"] {{
            background-color: {'rgba(0, 0, 0, 0.25)' if theme == 'light' else 'rgba(255, 255, 255, 0.2)'} !important;
            border: {'1px solid rgba(0, 0, 0, 0.1)' if theme == 'light' else '1px solid rgba(255, 255, 255, 0.1)'} !important;
        }}
        
        /* Toggle switch when checked */
        .stToggle [data-baseweb="switch"][aria-checked="true"],
        [data-testid="stToggle"] [data-baseweb="switch"][aria-checked="true"] {{
            background-color: #FF4B4B !important;
            border-color: #FF4B4B !important;
        }}
        
        /* Toggle switch thumb */
        .stToggle [data-baseweb="switch"] [data-baseweb="thumb"],
        [data-testid="stToggle"] [data-baseweb="switch"] [data-baseweb="thumb"] {{
            background-color: #ffffff !important;
            {'box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);' if theme == 'light' else 'box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);'}
        }}
        
        /* Ensure toggle container is visible */
        [data-testid="stToggle"] {{
            background: {bg_card} !important;
        }}
        
        [data-testid="stToggle"] label,
        [data-testid="stToggle"] p,
        [data-testid="stToggle"] span {{
            color: {text_main} !important;
        }}
        
        /* Toggle label text visibility */
        .stToggle > label > div,
        .stToggle > label > span {{
            color: {text_main} !important;
        }}
        
        /* Download button */
        .stDownloadButton > button {{
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            border: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        
        .stDownloadButton > button:hover {{
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        /* Dataframe styling */
        .dataframe {{
            border-radius: 12px;
            overflow: hidden;
            {'box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);' if theme == 'light' else ''}
        }}
        
        /* Input fields styling for light mode */
        input[type="text"], input[type="number"], textarea {{
            {'background-color: #ffffff; border: 1px solid rgba(0, 0, 0, 0.12);' if theme == 'light' else ''}
        }}
        
        input[type="text"]:focus, input[type="number"]:focus, textarea:focus {{
            {'border-color: #FF4B4B; box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);' if theme == 'light' else ''}
        }}
        
        /* Smooth scroll */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Ensure all text is visible - Streamlit default elements */
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {{
            color: {text_main} !important;
        }}
        
        .stText, .stTextInput > div > div > input, .stTextInput label {{
            color: {text_main} !important;
        }}
        
        /* Expander text */
        .streamlit-expanderHeader p, .streamlit-expanderHeader div, .streamlit-expanderHeader span {{
            color: {text_main} !important;
        }}
        
        .streamlit-expanderContent p, .streamlit-expanderContent div, .streamlit-expanderContent span, 
        .streamlit-expanderContent label, .streamlit-expanderContent .stMarkdown {{
            color: {text_main} !important;
        }}
        
        /* Slider labels */
        .stSlider label, .stSlider p {{
            color: {text_main} !important;
        }}
        
        /* Selectbox labels */
        .stSelectbox label, .stSelectbox p {{
            color: {text_main} !important;
        }}
        
        /* All paragraph and text elements */
        p, span, div, label {{
            color: {text_main};
        }}
        
        /* Sidebar text */
        .css-1d391kg p, .css-1d391kg span, .css-1d391kg div, .css-1d391kg label {{
            color: {text_main} !important;
        }}
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{
            color: {text_main} !important;
        }}
        
        /* Info and warning boxes */
        .stInfo, .stInfo p, .stInfo div, .stInfo span {{
            color: {text_main} !important;
        }}
        
        /* Toggle labels */
        .stToggle label {{
            color: {text_main} !important;
        }}
        
        /* Widget labels and help text */
        label, .stWidget label, .stWidget p {{
            color: {text_main} !important;
        }}
        
        /* Help text in tooltips */
        [data-testid="stTooltip"] {{
            color: {text_main} !important;
        }}
        
        /* All text inputs */
        input, textarea, select {{
            color: {text_main} !important;
        }}
        
        /* Streamlit's default text */
        .element-container p, .element-container span, .element-container div {{
            color: {text_main};
        }}
        
        /* Ensure expander labels are visible */
        .streamlit-expanderHeader {{
            color: {text_main} !important;
        }}
        
        .streamlit-expanderHeader * {{
            color: {text_main} !important;
        }}
        
        /* Ensure text in open expanders is visible */
        .streamlit-expanderHeader[aria-expanded="true"] *,
        .streamlit-expanderHeader[aria-expanded="true"] p,
        .streamlit-expanderHeader[aria-expanded="true"] span,
        .streamlit-expanderHeader[aria-expanded="true"] div {{
            color: {text_main} !important;
        }}
        
        /* Streamlit metric and other components */
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
            color: {text_main} !important;
        }}
        
        </style>
    """, unsafe_allow_html=True)

apply_custom_styles(st.session_state["theme"])

# ---------- Sidebar Controls ----------
sidebar_text_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#475569"
sidebar_secondary = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"

with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
            <h1 style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">AURA+</h1>
            <p style="color: {sidebar_secondary}; font-size: 0.85rem; margin-top: 0.5rem;">Stress Risk Screening</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    theme_label = "🌙 Dark Mode" if st.session_state["theme"] == "dark" else "☀️ Light Mode"
    if st.toggle(theme_label, value=(st.session_state["theme"] == "dark")):
        if st.session_state["theme"] != "dark":
            st.session_state["theme"] = "dark"
            st.rerun()
    else:
        if st.session_state["theme"] != "light":
            st.session_state["theme"] = "light"
            st.rerun()
            
    st.divider()
    
    info_bg = "rgba(255, 75, 75, 0.1)" if st.session_state["theme"] == "dark" else "rgba(255, 75, 75, 0.06)"
    info_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    st.markdown(f"""
        <div style="background: {info_bg}; padding: 1rem; border-radius: 10px; border-left: 3px solid #FF4B4B; {info_shadow}">
            <p style="margin: 0; font-size: 0.9rem; line-height: 1.5; color: {sidebar_text_color};">
                <strong style="color: {sidebar_text_color};">💡 About AURA+</strong><br>
                Uses AI to predict stress risks based on multi-dimensional patterns. Educational screening tool only.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------- Modern header ----------
header_subtitle_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="main-header">AURA+ Stress Risk</h1>
        <p style="color: {header_subtitle_color}; font-size: 1.1rem; margin-top: 0.5rem; font-weight: 400;">
            A premium educational screening tool by Shamma Samiha
        </p>
    </div>
""", unsafe_allow_html=True)

disclaimer_bg = "rgba(255, 193, 7, 0.1)" if st.session_state["theme"] == "dark" else "rgba(255, 193, 7, 0.06)"
disclaimer_text = "#b0b8c4" if st.session_state["theme"] == "dark" else "#475569"
disclaimer_title = "#ffffff" if st.session_state["theme"] == "dark" else "#0f172a"
disclaimer_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""

st.markdown(f"""
    <div style="background: {disclaimer_bg}; border-left: 4px solid #ffc107; padding: 1.25rem; border-radius: 12px; margin-bottom: 2rem; {disclaimer_shadow}">
        <div style="display: flex; align-items: start; gap: 0.75rem;">
            <span style="font-size: 1.5rem;">⚠️</span>
            <div>
                <strong style="font-size: 1rem; display: block; margin-bottom: 0.5rem; color: {disclaimer_title};">Important Disclaimer</strong>
                <p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {disclaimer_text};">
                    AURA+ provides an educational estimate of stress risk based on questionnaire inputs. 
                    It is <strong style="color: {disclaimer_text};">not</strong> medical advice and <strong style="color: {disclaimer_text};">not</strong> a clinical diagnosis. 
                    If you feel unsafe or are at risk of self-harm, please seek immediate local emergency help or contact a trusted person.
                </p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

model = load_model()
feature_names = get_feature_names()

# Initialize defaults once
if "initialized" not in st.session_state:
    set_defaults(feature_names)
    st.session_state["initialized"] = True

# ---------- Controls row ----------
c1, c2, c3 = st.columns([1.2, 1, 2])
with c1:
    if st.button("🔄 Reset All Inputs", use_container_width=True):
        set_defaults(feature_names)
        st.toast("✅ Inputs reset to defaults", icon="✅")

with c2:
    show_advanced = st.toggle("🔬 Advanced Details", value=False)

tip_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"
with c3:
    st.markdown(
        f"<div style='text-align:right; color: {tip_color}; font-size: 0.9rem; padding-top: 0.5rem;'>💡 Tip: Use the ⓘ icons to see what each question means</div>",
        unsafe_allow_html=True
    )

st.divider()

# ---------- Group questions ----------
SECTIONS = ["Psychological", "Physical", "Sleep", "Environment", "Academic", "Social"]
section_icons = {
    "Psychological": "🧠",
    "Physical": "🫀",
    "Sleep": "😴",
    "Environment": "🏠",
    "Academic": "📚",
    "Social": "👥",
}

def render_section(section_name, feats):
    st.markdown(f"### {section_icons.get(section_name,'')} {section_name}")
    cols = st.columns(2)
    for i, feat in enumerate(feats):
        meta = QUESTION_MAP.get(feat, {})
        label = meta.get("label", feat.replace("_", " ").title())
        help_text = meta.get("help", "")
        widget_key = f"inp_{feat}"
        col = cols[i % 2]

        if meta.get("type") == "binary":
            col.selectbox(
                label,
                options=[0, 1],
                index=int(st.session_state.get(widget_key, meta.get("default", 0))),
                key=widget_key,
                help=help_text,
            )
        elif meta.get("type") == "range":
            col.slider(
                label,
                min_value=int(meta["min"]),
                max_value=int(meta["max"]),
                value=int(st.session_state.get(widget_key, meta.get("default", (meta["min"] + meta["max"]) // 2))),
                key=widget_key,
                help=help_text,
            )
        else:
            col.slider(
                label,
                min_value=1,
                max_value=5,
                value=int(st.session_state.get(widget_key, meta.get("default", 3))),
                key=widget_key,
                help=help_text,
            )

# Build section -> features in dataset order
section_to_feats = {s: [] for s in SECTIONS}
for feat in feature_names:
    sec = QUESTION_MAP.get(feat, {}).get("section", "Other")
    if sec in section_to_feats:
        section_to_feats[sec].append(feat)

# Render sections with expanders (clean + modern)
section_subtitle_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"
st.markdown(f"""
    <div style="margin: 2rem 0 1.5rem 0;">
        <h2 style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
            1️⃣ Answer a Few Questions
        </h2>
        <p style="color: {section_subtitle_color}; font-size: 0.95rem; margin-top: 0.5rem;">
            Please provide information about your current situation across different life areas.
        </p>
    </div>
""", unsafe_allow_html=True)

for sec in SECTIONS:
    with st.expander(f"{section_icons.get(sec,'')} {sec}", expanded=(sec in ["Psychological", "Academic"])):
        render_section(sec, section_to_feats[sec])

st.divider()

st.markdown(f"""
    <div style="margin: 2rem 0 1.5rem 0; text-align: center;">
        <h2 style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
            2️⃣ See Your Result
        </h2>
        <p style="color: {section_subtitle_color}; font-size: 0.95rem; margin-top: 0.5rem;">
            Click the button below to get your stress risk assessment.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------- Predict button ----------
_, predict_col, _ = st.columns([1, 2, 1])
with predict_col:
    predict_clicked = st.button("Predict Stress Risk", type="primary", use_container_width=True)

# Placeholder card before results
if not predict_clicked and 'last_prediction' not in st.session_state:
    placeholder_text_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"
    placeholder_bg = "rgba(128, 128, 128, 0.03)" if st.session_state["theme"] == "dark" else "rgba(0, 0, 0, 0.02)"
    placeholder_border = "rgba(255, 255, 255, 0.1)" if st.session_state["theme"] == "dark" else "rgba(226, 232, 240, 1)"
    
    st.markdown(f"""
        <div style="background: {placeholder_bg}; border: 1px dashed {placeholder_border}; border-radius: 20px; padding: 3rem 2rem; text-align: center; margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">📋</div>
            <h3 style="color: {placeholder_text_color}; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.75rem;">
                Ready to Get Your Results?
            </h3>
            <p style="color: {placeholder_text_color}; font-size: 0.95rem; opacity: 0.8; max-width: 500px; margin: 0 auto;">
                Click the button above to analyze your responses and receive a personalized stress risk assessment with actionable suggestions.
            </p>
        </div>
    """, unsafe_allow_html=True)

if predict_clicked:
    # Collect inputs from session_state in correct feature order
    user_input = {feat: st.session_state.get(f"inp_{feat}") for feat in feature_names}
    user_df = pd.DataFrame([user_input])

    pred = int(model.predict(user_df[feature_names])[0])
    proba = model.predict_proba(user_df[feature_names])[0]
    pred_label = STRESS_LABELS[pred]

    # Results in a card
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Result header
    result_header_color = "#ffffff" if st.session_state["theme"] == "dark" else "#1e293b"
    result_subtext_color = "#b0b8c4" if st.session_state["theme"] == "dark" else "#64748b"
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="font-size: 1.8rem; font-weight: 700; color: {result_header_color}; margin: 0;">
                Your Assessment Result
            </h3>
            <p style="color: {result_subtext_color}; font-size: 0.9rem; margin-top: 0.5rem;">
                Based on your responses across all categories
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Badge
    st.markdown(risk_badge_html(pred, st.session_state["theme"]), unsafe_allow_html=True)

    # Human explanation line
    explanation_bg_opacity = 0.1 if st.session_state["theme"] == "dark" else 0.08
    explanation_styles = {
        0: {"bg": f"rgba(124, 255, 178, {explanation_bg_opacity})", "border": "#7CFFB2", "icon": "✅"},
        1: {"bg": f"rgba(255, 211, 124, {explanation_bg_opacity})", "border": "#FFD37C", "icon": "⚠️"},
        2: {"bg": f"rgba(255, 138, 138, {explanation_bg_opacity})", "border": "#FF8A8A", "icon": "🚨"}
    }
    style = explanation_styles[pred]
    explanation_text_color = "#ffffff" if st.session_state["theme"] == "dark" else "#0f172a"
    explanation_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    
    explanations = {
        0: f"Your responses suggest a <strong style='color: {explanation_text_color};'>low</strong> stress risk right now. Keep maintaining healthy routines and support systems.",
        1: f"Your responses suggest a <strong style='color: {explanation_text_color};'>moderate</strong> stress risk. A few areas may be contributing—small changes can help.",
        2: f"Your responses suggest a <strong style='color: {explanation_text_color};'>high</strong> stress risk. Consider prioritizing support and recovery. If you feel unsafe, seek immediate help."
    }
    
    st.markdown(f"""
        <div style="background: {style['bg']}; padding: 1.25rem; border-radius: 12px; border-left: 4px solid {style['border']}; margin: 1.5rem 0; {explanation_shadow}">
            <p style="margin: 0; font-size: 1rem; line-height: 1.7; color: {explanation_text_color};">
                {style['icon']} {explanations[pred]}
            </p>
        </div>
    """, unsafe_allow_html=True)

    confidence_bg = "rgba(128, 128, 128, 0.05)" if st.session_state["theme"] == "dark" else "rgba(15, 23, 42, 0.03)"
    confidence_text = "#b0b8c4" if st.session_state["theme"] == "dark" else "#475569"
    confidence_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {confidence_bg}; border-radius: 10px; margin: 1rem 0; {confidence_shadow}">
            <p style="margin: 0; font-size: 0.9rem; color: {confidence_text};">
                <strong style="color: {confidence_text};">Model Confidence:</strong> Low={proba[0]:.1%} | Moderate={proba[1]:.1%} | High={proba[2]:.1%}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Explainability
    pred_class, top_contrib = explain_with_coefficients(model, user_df, feature_names, top_k=6)

    # Suggestions based on top contributors (dedupe)
    suggested = []
    for feat in top_contrib.index:
        if feat in SUGGESTION_RULES:
            suggested.append(SUGGESTION_RULES[feat])
    seen = set()
    suggested = [s for s in suggested if not (s in seen or seen.add(s))]

    suggestion_text_color = "#ffffff" if st.session_state["theme"] == "dark" else "#0f172a"
    suggestion_bg = "rgba(255, 75, 75, 0.05)" if st.session_state["theme"] == "dark" else "rgba(255, 75, 75, 0.04)"
    suggestion_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    
    st.markdown("""
        <div style="margin-top: 2rem;">
            <h3 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem;">
                3️⃣ Personalized Suggestions
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if suggested:
        for i, s in enumerate(suggested[:5], 1):
            st.markdown(f"""
                <div style="background: {suggestion_bg}; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.75rem; border-left: 3px solid #FF4B4B; {suggestion_shadow}">
                    <p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: {suggestion_text_color};">
                        <strong style="color: #FF4B4B;">{i}.</strong> {s}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background: {suggestion_bg}; padding: 1rem 1.25rem; border-radius: 10px; border-left: 3px solid #FF4B4B; {suggestion_shadow}">
                <p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: {suggestion_text_color};">
                    • Maintain healthy routines and seek support when needed.
                </p>
            </div>
        """, unsafe_allow_html=True)

    remember_bg = "rgba(33, 150, 243, 0.1)" if st.session_state["theme"] == "dark" else "rgba(33, 150, 243, 0.06)"
    remember_text = "#b0b8c4" if st.session_state["theme"] == "dark" else "#475569"
    remember_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    st.markdown(f"""
        <div style="background: {remember_bg}; border-left: 4px solid #2196F3; padding: 1.25rem; border-radius: 12px; margin-top: 1.5rem; {remember_shadow}">
            <div style="display: flex; align-items: start; gap: 0.75rem;">
                <span style="font-size: 1.3rem;">💙</span>
                <p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {remember_text};">
                    <strong style="color: {remember_text};">Remember:</strong> If symptoms feel overwhelming or persistent, consider speaking with a qualified professional or trusted support person.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Advanced details toggle
    if show_advanced:
        advanced_border = "rgba(255, 255, 255, 0.1)" if st.session_state["theme"] == "dark" else "rgba(0, 0, 0, 0.1)"
        st.markdown(f"""
            <div style="margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid {advanced_border};">
                <h3 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem;">
                    🔬 Advanced Details: What Influenced the Prediction?
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        advanced_bg = "rgba(138, 43, 226, 0.05)" if st.session_state["theme"] == "dark" else "rgba(138, 43, 226, 0.04)"
        advanced_text = "#b0b8c4" if st.session_state["theme"] == "dark" else "#475569"
        advanced_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
        st.markdown(f"""
            <div style="background: {advanced_bg}; padding: 1rem 1.25rem; border-radius: 10px; border-left: 3px solid #8a2be2; margin-bottom: 1.5rem; {advanced_shadow}">
                <p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {advanced_text};">
                    These are the strongest signals the model noticed. Positive values generally push toward the predicted class; 
                    negative values push away. This is an educational explanation, not a diagnosis.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        expl_table = top_contrib.reset_index()
        expl_table.columns = ["Feature", "Contribution"]
        expl_table["Feature"] = expl_table["Feature"].apply(format_feature_label)
        expl_table["Direction"] = expl_table["Contribution"].apply(lambda x: "📈 Increases risk" if x > 0 else "📉 Reduces risk")
        expl_table["Contribution"] = expl_table["Contribution"].round(3)
        st.dataframe(expl_table[["Feature", "Direction", "Contribution"]], use_container_width=True, height=300)

    st.markdown('</div>', unsafe_allow_html=True)

    # Download report
    report_text = make_report_text(pred_label, proba, top_contrib, suggested[:5])
    st.download_button(
        label="⬇️ Download Detailed Report",
        data=report_text,
        file_name="aura_plus_stress_report.txt",
        mime="text/plain",
    )
