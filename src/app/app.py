"""
AURA+ Stress Risk Screening Application
Modern, modular Streamlit application for stress risk assessment.
"""

import streamlit as st
import pandas as pd

# Import utilities
from utils.constants import STRESS_LABELS, QUESTION_MAP, SUGGESTION_RULES
from utils.model import (
    load_model,
    get_feature_names,
    explain_with_coefficients,
    predict_proba_safe,
    format_feature_label,
    make_report_text,
    set_defaults
)
from utils.styles import load_css, risk_badge_html, get_theme_colors

# Import components
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.cards import render_info_card, render_header
from components.forms import render_all_questions
from components.pages import render_about_page, render_results_page

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="AURA+ Stress Risk Screening",
    page_icon="🧠",
    layout="wide"
)

# ========== THEME INITIALIZATION ==========
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

# ========== LOAD CSS STYLES ==========
load_css(st.session_state["theme"])

# ========== RENDER NAVBAR ==========
render_navbar(st.session_state["theme"])

# ========== RENDER SIDEBAR & HANDLE THEME TOGGLE ==========
new_theme = render_sidebar(st.session_state["theme"])
if new_theme != st.session_state["theme"]:
    st.session_state["theme"] = new_theme
    st.rerun()

# ========== LOAD MODEL & FEATURES ==========
model = load_model()
feature_names = get_feature_names()

# Initialize defaults once
if "initialized" not in st.session_state:
    set_defaults(feature_names)
    st.session_state["initialized"] = True

# Initialize page navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "assessment"

# ========== MAIN CONTENT ==========
colors = get_theme_colors(st.session_state["theme"])

# ========== PAGE ROUTING ==========
if st.session_state["current_page"] == "about":
    render_about_page(st.session_state["theme"])
    st.stop()  # Don't render the rest of the page
    
elif st.session_state["current_page"] == "results":
    render_results_page(st.session_state["theme"])
    st.stop()  # Don't render the rest of the page

# Otherwise, render the assessment page (default)

# Header
render_header(
    "AURA+ Stress Risk",
    "A premium educational screening tool by Shamma Samiha",
    st.session_state["theme"]
)

# Disclaimer
render_info_card(
    "Important Disclaimer",
    "AURA+ provides an educational estimate of stress risk based on questionnaire inputs. "
    "It is <strong>not</strong> medical advice and <strong>not</strong> a clinical diagnosis. "
    "If you feel unsafe or are at risk of self-harm, please seek immediate local emergency help or contact a trusted person.",
    "⚠️",
    st.session_state["theme"],
    card_type="warning"
)

# ========== CONTROL BUTTONS ==========
c1, c2, c3 = st.columns([1.2, 1, 2])
with c1:
    if st.button("🔄 Reset All Inputs", use_container_width=True):
        set_defaults(feature_names)
        st.toast("✅ Inputs reset to defaults", icon="✅")

with c2:
    show_advanced = st.toggle("🔬 Advanced Details", value=False)

with c3:
    st.markdown(
        f"<div style='text-align:right; color: {colors['text_secondary']}; font-size: 0.9rem; padding-top: 0.5rem;'>💡 Tip: Use the ⓘ icons to see what each question means</div>",
        unsafe_allow_html=True
    )

st.divider()

# ========== QUESTIONNAIRE SECTION ==========
st.markdown(f"""
<div class="animate-fade-in" style="margin: 2rem 0 1.5rem 0;">
<h2 class="animate-stagger-1" style="font-size: 2rem; font-weight: 800; margin: 0; color: #FF4B4B;">1️⃣ Answer a Few Questions</h2>
<p class="animate-stagger-2" style="color: {colors['text_secondary']}; font-size: 0.95rem; margin-top: 0.5rem;">Please provide information about your current situation across different life areas.</p>
</div>
""", unsafe_allow_html=True)

# Render all questions using the forms component
render_all_questions(feature_names, st.session_state["theme"])

st.divider()

# ========== PREDICTION SECTION ==========
st.markdown(f"""
<div class="animate-fade-in" style="margin: 2rem 0 1.5rem 0; text-align: center;">
<h2 class="animate-stagger-1" style="font-size: 2rem; font-weight: 800; margin: 0; color: #FF4B4B;">2️⃣ See Your Result</h2>
<p class="animate-stagger-2" style="color: {colors['text_secondary']}; font-size: 0.95rem; margin-top: 0.5rem;">Click the button below to get your stress risk assessment.</p>
</div>
""", unsafe_allow_html=True)

# Predict button
_, predict_col, _ = st.columns([1, 2, 1])
with predict_col:
    predict_clicked = st.button("🚀 Predict Stress Risk", type="primary", use_container_width=True)

# Placeholder before results
if not predict_clicked and 'last_prediction' not in st.session_state:
    placeholder_bg = "rgba(128, 128, 128, 0.03)" if st.session_state["theme"] == "dark" else "rgba(0, 0, 0, 0.02)"
    
    st.markdown(f"""
<div style="background: {placeholder_bg}; border: 1px dashed {colors['border_color']}; border-radius: 20px; padding: 3rem 2rem; text-align: center; margin-top: 2rem;">
<div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">📋</div>
<h3 style="color: {colors['text_secondary']}; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.75rem;">Ready to Get Your Results?</h3>
<p style="color: {colors['text_secondary']}; font-size: 0.95rem; opacity: 0.8; max-width: 500px; margin: 0 auto;">Click the button above to analyze your responses and receive a personalized stress risk assessment with actionable suggestions.</p>
</div>
""", unsafe_allow_html=True)

# ========== RESULTS DISPLAY ==========
if predict_clicked:
    # Collect inputs
    user_input = {feat: st.session_state.get(f"inp_{feat}") for feat in feature_names}
    user_df = pd.DataFrame([user_input])

    # Make prediction
    pred = int(model.predict(user_df[feature_names])[0])
    proba = predict_proba_safe(model, user_df[feature_names])[0]
    pred_label = STRESS_LABELS[pred]

    # Results card with glassmorphism
    from components.cards import render_result_card
    
    result_content = ""
    
    # Result header
    result_content += f"""
<div class="animate-fade-in" style="text-align: center; margin-bottom: 2rem;">
<div class="animate-float" style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
<h3 class="animate-stagger-1" style="font-size: 1.8rem; font-weight: 700; color: {colors['text_main']}; margin: 0;">Your Assessment Result</h3>
<p class="animate-stagger-2" style="color: {colors['text_secondary']}; font-size: 0.9rem; margin-top: 0.5rem;">Based on your responses across all categories</p>
</div>
"""
    
    # Risk badge
    result_content += risk_badge_html(pred, st.session_state["theme"])

    # Explanation
    explanation_bg_opacity = 0.1 if st.session_state["theme"] == "dark" else 0.08
    explanation_styles = {
        0: {"bg": f"rgba(124, 255, 178, {explanation_bg_opacity})", "border": "#7CFFB2", "icon": "✅"},
        1: {"bg": f"rgba(255, 211, 124, {explanation_bg_opacity})", "border": "#FFD37C", "icon": "⚠️"},
        2: {"bg": f"rgba(255, 138, 138, {explanation_bg_opacity})", "border": "#FF8A8A", "icon": "🚨"}
    }
    style = explanation_styles[pred]
    
    explanations = {
        0: f"Your responses suggest a <strong style='color: {colors['text_main']};'>low</strong> stress risk right now. Keep maintaining healthy routines and support systems.",
        1: f"Your responses suggest a <strong style='color: {colors['text_main']};'>moderate</strong> stress risk. A few areas may be contributing—small changes can help.",
        2: f"Your responses suggest a <strong style='color: {colors['text_main']};'>high</strong> stress risk. Consider prioritizing support and recovery. If you feel unsafe, seek immediate help."
    }
    
    shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    result_content += f"""
<div class="animate-stagger-3 glass-card" style="background: {style['bg']}; padding: 1.25rem; border-radius: 12px; border-left: 4px solid {style['border']}; margin: 1.5rem 0; {shadow}; backdrop-filter: blur(10px);">
<p style="margin: 0; font-size: 1rem; line-height: 1.7; color: {colors['text_main']};">{style['icon']} {explanations[pred]}</p>
</div>
"""

    confidence_bg = "rgba(128, 128, 128, 0.05)" if st.session_state["theme"] == "dark" else "rgba(15, 23, 42, 0.03)"
    confidence_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    result_content += f"""
<div class="animate-stagger-4 glass-card" style="text-align: center; padding: 1rem; background: {confidence_bg}; border-radius: 10px; margin: 1rem 0; {confidence_shadow}; backdrop-filter: blur(10px);">
<p style="margin: 0; font-size: 0.9rem; color: {colors['text_secondary']};"><strong>Model Confidence:</strong> Low={proba[0]:.1%} | Moderate={proba[1]:.1%} | High={proba[2]:.1%}</p>
</div>
"""

    # Get explanations and suggestions
    pred_class, top_contrib = explain_with_coefficients(model, user_df, feature_names, top_k=6)
    
    suggested = []
    for feat in top_contrib.index:
        if feat in SUGGESTION_RULES:
            suggested.append(SUGGESTION_RULES[feat])
    seen = set()
    suggested = [s for s in suggested if not (s in seen or seen.add(s))]

    # Suggestions
    result_content += """
<div class="animate-stagger-5" style="margin-top: 2rem;">
<h3 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem;"> Personalized Suggestions</h3>
</div>
"""
    
    suggestion_bg = "rgba(255, 75, 75, 0.05)" if st.session_state["theme"] == "dark" else "rgba(255, 75, 75, 0.04)"
    suggestion_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    
    if suggested:
        for i, s in enumerate(suggested[:5], 1):
            result_content += f"""
<div class="glass-card hover-lift animate-stagger-{min(i+4, 9)}" style="background: {suggestion_bg}; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.75rem; border-left: 3px solid #FF4B4B; {suggestion_shadow}; backdrop-filter: blur(10px);">
<p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: {colors['text_main']};"><strong style="color: #FF4B4B;">{i}.</strong> {s}</p>
</div>
"""
    else:
        result_content += f"""
<div class="glass-card animate-stagger-5" style="background: {suggestion_bg}; padding: 1rem 1.25rem; border-radius: 10px; border-left: 3px solid #FF4B4B; {suggestion_shadow}; backdrop-filter: blur(10px);">
<p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: {colors['text_main']};">• Maintain healthy routines and seek support when needed.</p>
</div>
"""

    # Remember message
    remember_bg = "rgba(33, 150, 243, 0.1)" if st.session_state["theme"] == "dark" else "rgba(33, 150, 243, 0.06)"
    remember_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
    result_content += f"""
<div class="glass-card animate-stagger-5" style="background: {remember_bg}; border-left: 4px solid #2196F3; padding: 1.25rem; border-radius: 12px; margin-top: 1.5rem; {remember_shadow}; backdrop-filter: blur(10px);">
<div style="display: flex; align-items: start; gap: 0.75rem;">
<span class="animate-float" style="font-size: 1.3rem;">💙</span>
<p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {colors['text_secondary']};"><strong>Remember:</strong> If symptoms feel overwhelming or persistent, consider speaking with a qualified professional or trusted support person.</p>
</div>
</div>
"""
    
    # Render the complete result card
    render_result_card(result_content, st.session_state["theme"])
    
    # Save result to session state for viewing later
    st.session_state["last_prediction"] = result_content

    # Advanced details
    if show_advanced:
        advanced_border = colors['border_color']
        st.markdown(f"""
<div style="margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid {advanced_border};">
<h3 style="font-size: 1.6rem; font-weight: 700; margin-bottom: 1rem;">🔬 Advanced Details: What Influenced the Prediction?</h3>
</div>
""", unsafe_allow_html=True)
        
        advanced_bg = "rgba(138, 43, 226, 0.05)" if st.session_state["theme"] == "dark" else "rgba(138, 43, 226, 0.04)"
        advanced_shadow = "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);" if st.session_state["theme"] == "light" else ""
        st.markdown(f"""
<div style="background: {advanced_bg}; padding: 1rem 1.25rem; border-radius: 10px; border-left: 3px solid #8a2be2; margin-bottom: 1.5rem; {advanced_shadow}">
<p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {colors['text_secondary']};">These are the strongest signals the model noticed. Positive values generally push toward the predicted class; negative values push away. This is an educational explanation, not a diagnosis.</p>
</div>
""", unsafe_allow_html=True)
        
        expl_table = top_contrib.reset_index()
        expl_table.columns = ["Feature", "Contribution"]
        expl_table["Feature"] = expl_table["Feature"].apply(format_feature_label)
        expl_table["Direction"] = expl_table["Contribution"].apply(lambda x: "📈 Increases risk" if x > 0 else "📉 Reduces risk")
        expl_table["Contribution"] = expl_table["Contribution"].round(3)
        st.dataframe(expl_table[["Feature", "Direction", "Contribution"]], use_container_width=True, height=300)

    # Download report
    report_text = make_report_text(pred_label, proba, top_contrib, suggested[:5])
    st.download_button(
        label="⬇️ Download Detailed Report",
        data=report_text,
        file_name="aura_plus_stress_report.txt",
        mime="text/plain",
    )
