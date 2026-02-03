"""
AURA+ Form Components
Form input components for the assessment questionnaire.
"""

import streamlit as st
from utils.constants import QUESTION_MAP


def render_question_section(section_name: str, feature_names: list, theme: str = "dark"):
    """
    Render a section of questions in an expander.
    
    Args:
        section_name: Name of the section (e.g., 'Psychological', 'Physical')
        feature_names: List of all feature names
        theme: Current theme
    """
    # Filter questions for this section
    section_features = [
        feat for feat in feature_names 
        if QUESTION_MAP.get(feat, {}).get("section") == section_name
    ]
    
    if not section_features:
        return
    
    # Section icons
    section_icons = {
        "Psychological": "🧠",
        "Physical": "💪",
        "Sleep": "😴",
        "Environment": "🏠",
        "Academic": "📚",
        "Social": "👥"
    }
    
    icon = section_icons.get(section_name, "📋")
    
    with st.expander(f"{icon} {section_name}", expanded=False):
        # Use 2-column layout to prevent overflow
        cols = st.columns(2)
        for i, feat in enumerate(section_features):
            meta = QUESTION_MAP[feat]
            col = cols[i % 2]
            
            with col:
                # Add some spacing between inputs
                if i > 0 and i % 2 == 0:
                    st.markdown("<br>", unsafe_allow_html=True)
                
                if meta["type"] == "range":
                    # Get min and max for better formatting
                    min_val = meta["min"]
                    max_val = meta["max"]
                    
                    # Format function to show value clearly
                    def format_value(val, min_v=min_val, max_v=max_val):
                        return f"{val} / {max_v}"
                    
                    st.slider(
                        meta["label"],
                        min_value=min_val,
                        max_value=max_val,
                        value=st.session_state.get(f"inp_{feat}", meta["default"]),
                        key=f"inp_{feat}",
                        help=meta["help"],
                        format="%d"
                    )
                    
                elif meta["type"] == "likert":
                    # Likert scale with labels
                    likert_labels = {1: "Strongly Disagree", 2: "Disagree", 3: "Neutral", 4: "Agree", 5: "Strongly Agree"}
                    
                    st.slider(
                        meta["label"],
                        min_value=1,
                        max_value=5,
                        value=st.session_state.get(f"inp_{feat}", meta["default"]),
                        key=f"inp_{feat}",
                        help=meta["help"],
                        format="%d"
                    )
                    # Show current selection label
                    current_val = st.session_state.get(f"inp_{feat}", meta["default"])
                    st.caption(f"*{likert_labels.get(current_val, '')}*")
                    
                elif meta["type"] == "binary":
                    st.selectbox(
                        meta["label"],
                        options=[0, 1],
                        format_func=lambda x: "No" if x == 0 else "Yes",
                        index=st.session_state.get(f"inp_{feat}", meta["default"]),
                        key=f"inp_{feat}",
                        help=meta["help"]
                    )


def render_all_questions(feature_names: list, theme: str = "dark"):
    """
    Render all question sections.
    
    Args:
        feature_names: List of all feature names
        theme: Current theme
    """
    sections = ["Psychological", "Physical", "Sleep", "Environment", "Academic", "Social"]
    
    for section in sections:
        render_question_section(section, feature_names, theme)
