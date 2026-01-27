"""
AURA+ Constants
All application constants including question maps, suggestions, and styling configurations.
"""

from pathlib import Path

# Path Configuration
ROOT_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = ROOT_DIR / "models" / "baseline_logistic_model.joblib"
DATA_PATH = ROOT_DIR / "data" / "processed" / "stress_clean.csv"

# Stress Level Labels
STRESS_LABELS = {0: "Low", 1: "Moderate", 2: "High"}

# Badge Styling Configuration
BADGE_STYLES = {
    0: {
        "bg_dark": "#0f2f1d",
        "fg_dark": "#7CFFB2",
        "border_dark": "#1f7a49",
        "bg_light": "#e6ffef",
        "fg_light": "#1b5e20",
        "border_light": "#81c784",
        "emoji": "✅"
    },
    1: {
        "bg_dark": "#2b2412",
        "fg_dark": "#FFD37C",
        "border_dark": "#b27a1f",
        "bg_light": "#fff9e6",
        "fg_light": "#795548",
        "border_light": "#ffd54f",
        "emoji": "⚠️"
    },
    2: {
        "bg_dark": "#2a1414",
        "fg_dark": "#FF8A8A",
        "border_dark": "#a83a3a",
        "bg_light": "#ffebee",
        "fg_light": "#b71c1c",
        "border_light": "#ef9a9a",
        "emoji": "🚨"
    },
}

# Question Configuration Map
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

# Suggestion Rules
SUGGESTION_RULES = {
    "study_load": "Split study into smaller blocks (25/5 or 50/10). Plan the next 1–2 days only, not the whole week.",
    "sleep_quality": "Keep a consistent bedtime, reduce screens before sleep, and avoid late caffeine.",
    "peer_pressure": "Practice boundaries: \"I can't do that right now.\" Choose priorities that match your goals.",
    "career_concerns": "Write down worries, then choose 1 small action (resume update, talk to a mentor, learn one skill).",
    "bullying": "If bullying is present, consider speaking to a trusted person/counselor. If unsafe, seek immediate help locally.",
    "noise_level": "Try a quieter space, earplugs/headphones, or white noise while studying.",
    "extracurriculars": "Reduce commitments temporarily and protect recovery time. 'Less but consistent' beats overload.",
    "headache": "Hydrate, take short screen breaks, and check posture. If persistent, consider professional advice.",
    "blood_pressure": "Slow breathing (4 in, 6 out for 2–3 min) can help. Seek medical advice if concerned.",
    "social_support": "Reach out to one trusted person. Even one supportive conversation can reduce stress load.",
    "safety": "If safety is low, prioritize reaching out to trusted support or local services first.",
    "basic_needs": "Start with basics: meals, hydration, rest. Stress strategies work better when needs are met.",
}
