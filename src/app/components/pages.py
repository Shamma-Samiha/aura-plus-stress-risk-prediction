"""
AURA+ Pages Components
Different page views for navigation (About, Results, etc.)
"""

import streamlit as st
from utils.styles import get_theme_colors


def render_about_page(theme: str = "dark"):
    """
    Render the About AURA+ page.
    
    Args:
        theme: Current theme ('dark' or 'light')
    """
    colors = get_theme_colors(theme)
    
    st.markdown(f"""
<div class="animate-fade-in" style="text-align: center; margin-bottom: 2rem;">
<h1 style="color: #FF4B4B; font-size: 3rem; font-weight: 800; margin: 1rem 0;">About AURA+</h1>
<p style="color: {colors['text_secondary']}; font-size: 1.1rem; margin-top: 0.5rem;">Advanced Understanding & Risk Assessment Platform</p>
</div>
""", unsafe_allow_html=True)
    
    # Mission section
    mission_bg = "rgba(255, 75, 75, 0.05)" if theme == "dark" else "rgba(255, 75, 75, 0.04)"
    shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if theme == "light" else ""
    
    st.markdown(f"""
<div class="glass-card animate-fade-in" style="background: {mission_bg}; padding: 2rem; border-radius: 16px; border-left: 4px solid #FF4B4B; margin-bottom: 2rem; {shadow}">
<h2 style="font-size: 1.8rem; font-weight: 700; color: {colors['text_main']}; margin-bottom: 1rem;">🎯 Our Mission</h2>
<p style="color: {colors['text_secondary']}; font-size: 1rem; line-height: 1.8; margin: 0;">
AURA+ is an educational AI-powered screening tool designed to help individuals better understand their stress risk levels. 
By analyzing multi-dimensional patterns across various life domains, AURA+ provides personalized insights and actionable suggestions 
to support mental wellness and early awareness.
</p>
</div>
""", unsafe_allow_html=True)
    
    # Key features
    st.markdown(f"""
<div class="animate-stagger-1" style="margin: 2rem 0 1rem 0;">
<h2 style="font-size: 1.8rem; font-weight: 700; color: {colors['text_main']};">✨ Key Features</h2>
</div>
""", unsafe_allow_html=True)
    
    features = [
        ("🤖 AI-Powered Analysis", "Uses machine learning to identify stress risk patterns across multiple life dimensions"),
        ("📊 Multi-Dimensional Assessment", "Evaluates academic, social, physical, emotional, and lifestyle factors"),
        ("💡 Personalized Suggestions", "Provides tailored recommendations based on your specific risk factors"),
        ("🔒 Privacy First", "Your data stays on your device - we don't store or share any personal information"),
        ("🎓 Educational Tool", "Designed for awareness and learning, not clinical diagnosis"),
        ("🌙 Modern Interface", "Beautiful dark/light themes with smooth animations and responsive design")
    ]
    
    feature_bg = "rgba(138, 43, 226, 0.05)" if theme == "dark" else "rgba(138, 43, 226, 0.04)"
    
    cols = st.columns(2)
    for idx, (title, description) in enumerate(features):
        with cols[idx % 2]:
            st.markdown(f"""
<div class="glass-card hover-lift animate-stagger-{idx + 2}" style="background: {feature_bg}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 3px solid #8a2be2; {shadow}; min-height: 140px;">
<h3 style="font-size: 1.1rem; font-weight: 700; color: {colors['text_main']}; margin-bottom: 0.75rem;">{title}</h3>
<p style="color: {colors['text_secondary']}; font-size: 0.9rem; line-height: 1.6; margin: 0;">{description}</p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Important disclaimer
    warning_bg = "rgba(255, 193, 7, 0.1)" if theme == "dark" else "rgba(255, 193, 7, 0.06)"
    st.markdown(f"""
<div class="glass-card animate-fade-in" style="background: {warning_bg}; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ffc107; margin: 2rem 0; {shadow}">
<h2 style="font-size: 1.5rem; font-weight: 700; color: {colors['text_main']}; margin-bottom: 1rem;">⚠️ Important to Know</h2>
<ul style="color: {colors['text_secondary']}; font-size: 0.95rem; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
<li><strong>Not a Medical Tool:</strong> AURA+ is an educational screening tool, not a diagnostic instrument or medical device.</li>
<li><strong>Not a Substitute:</strong> This tool does not replace professional mental health assessment or care.</li>
<li><strong>Seek Professional Help:</strong> If you're experiencing distress, please consult a qualified mental health professional.</li>
<li><strong>Emergency Support:</strong> If you feel unsafe or are in crisis, contact local emergency services or a crisis helpline immediately.</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    # How it works
    st.markdown(f"""
<div class="animate-stagger-1" style="margin: 2rem 0 1rem 0;">
<h2 style="font-size: 1.8rem; font-weight: 700; color: {colors['text_main']};">🔬 How It Works</h2>
</div>
""", unsafe_allow_html=True)
    
    info_bg = "rgba(33, 150, 243, 0.05)" if theme == "dark" else "rgba(33, 150, 243, 0.04)"
    
    steps = [
        ("1️⃣ Answer Questions", "Complete a brief questionnaire about various aspects of your life"),
        ("2️⃣ AI Analysis", "Our machine learning model analyzes patterns across multiple dimensions"),
        ("3️⃣ Risk Assessment", "Receive a stress risk level (Low, Moderate, or High) with confidence scores"),
        ("4️⃣ Personalized Insights", "Get tailored suggestions based on factors contributing to your assessment")
    ]
    
    for idx, (step, description) in enumerate(steps):
        st.markdown(f"""
<div class="glass-card animate-stagger-{idx + 3}" style="background: {info_bg}; padding: 1.25rem; border-radius: 12px; margin-bottom: 1rem; border-left: 3px solid #2196F3; {shadow}">
<h3 style="font-size: 1.1rem; font-weight: 700; color: {colors['text_main']}; margin-bottom: 0.5rem;">{step}</h3>
<p style="color: {colors['text_secondary']}; font-size: 0.9rem; line-height: 1.6; margin: 0;">{description}</p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Credits section
    credits_bg = "rgba(124, 255, 178, 0.05)" if theme == "dark" else "rgba(124, 255, 178, 0.04)"
    st.markdown(f"""
<div class="glass-card animate-fade-in" style="background: {credits_bg}; padding: 2rem; border-radius: 16px; border-left: 4px solid #7CFFB2; margin: 2rem 0; {shadow}; text-align: center;">
<h2 style="font-size: 1.5rem; font-weight: 700; color: {colors['text_main']}; margin-bottom: 1rem;">💜 Created by Shamma Samiha</h2>
<p style="color: {colors['text_secondary']}; font-size: 1rem; line-height: 1.8; margin: 0;">
AURA+ is built with care to promote mental health awareness and early intervention.<br>
If you have questions or feedback, please reach out to the development team.
</p>
</div>
""", unsafe_allow_html=True)


def render_results_page(theme: str = "dark"):
    """
    Render the Results page showing the last prediction.
    
    Args:
        theme: Current theme ('dark' or 'light')
    """
    colors = get_theme_colors(theme)
    
    st.markdown(f"""
<div class="animate-fade-in" style="text-align: center; margin-bottom: 2rem;">
<h1 style="color: #FF4B4B; font-size: 3rem; font-weight: 800; margin: 1rem 0;">Your Results</h1>
<p style="color: {colors['text_secondary']}; font-size: 1.1rem; margin-top: 0.5rem;">View your latest assessment results</p>
</div>
""", unsafe_allow_html=True)
    
    # Check if there are any saved results
    if "last_prediction" in st.session_state and st.session_state["last_prediction"] is not None:
        result_data = st.session_state["last_prediction"]
        
        # Display saved result
        st.markdown(f"""
<div class="glass-card animate-fade-in" style="padding: 2rem; border-radius: 16px; margin-bottom: 2rem;">
{result_data}
</div>
""", unsafe_allow_html=True)
        
    else:
        # No results yet - show placeholder
        placeholder_bg = "rgba(128, 128, 128, 0.03)" if theme == "dark" else "rgba(0, 0, 0, 0.02)"
        
        st.markdown(f"""
<div style="background: {placeholder_bg}; border: 1px dashed {colors['border_color']}; border-radius: 20px; padding: 4rem 2rem; text-align: center; margin-top: 2rem;">
<div style="font-size: 4rem; margin-bottom: 1.5rem; opacity: 0.5;">📊</div>
<h3 style="color: {colors['text_secondary']}; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem;">No Results Yet</h3>
<p style="color: {colors['text_secondary']}; font-size: 1rem; opacity: 0.8; max-width: 500px; margin: 0 auto 2rem auto;">
You haven't completed an assessment yet. Click "New Assessment" in the sidebar to get started!
</p>
</div>
""", unsafe_allow_html=True)
        
        # Real Streamlit button to start assessment
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            if st.button("🚀 Start Your First Assessment", type="primary", use_container_width=True):
                st.session_state["current_page"] = "assessment"
                st.rerun()
