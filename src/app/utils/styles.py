"""
AURA+ Style Utilities
Functions for loading CSS and generating styled components.
"""

import streamlit as st
from pathlib import Path
from .constants import BADGE_STYLES, STRESS_LABELS


def load_css(theme: str = "dark"):
    """
    Load all CSS files from the static directory.
    
    Args:
        theme: Current theme ('dark' or 'light')
    """
    css_dir = Path(__file__).parent.parent / "static" / "css"
    
    # Load CSS files in order: base, theme, components, animations
    css_files = ["base.css", f"{theme}.css", "components.css", "animations.css"]
    
    css_content = ""
    for css_file in css_files:
        css_path = css_dir / css_file
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                css_content += f.read() + "\n"
    
    # Add theme data attribute to body
    if css_content:
        st.markdown(f"""
            <style>
            :root {{
                data-theme: {theme};
            }}
            .stApp {{
                data-theme: {theme};
            }}
            {css_content}
            </style>
        """, unsafe_allow_html=True)


def risk_badge_html(level_int: int, theme: str = "dark") -> str:
    """
    Generate HTML for risk level badge.
    
    Args:
        level_int: Risk level (0=Low, 1=Moderate, 2=High)
        theme: Current theme ('dark' or 'light')
        
    Returns:
        str: HTML string for badge
    """
    style = BADGE_STYLES[level_int]
    label = STRESS_LABELS[level_int]
    bg = style[f'bg_{theme}']
    fg = style[f'fg_{theme}']
    border = style[f'border_{theme}']
    
    return f"""
<div style="display:inline-flex;align-items:center;gap:10px;padding:12px 18px;border-radius:12px;background:{bg};color:{fg};border:1px solid {border};font-weight:700;font-size:16px;box-shadow: 0 4px 15px rgba(0,0,0,0.1);margin-bottom: 20px;">
<span style="font-size:20px;">{style['emoji']}</span>
<span>Risk level: {label}</span>
</div>
"""


def get_theme_colors(theme: str) -> dict:
    """
    Get color palette for the current theme.
    
    Args:
        theme: 'dark' or 'light'
        
    Returns:
        dict: Color configuration
    """
    if theme == "dark":
        return {
            "primary": "#FF4B4B",
            "bg_main": "#0a0e1a",
            "bg_card": "rgba(30, 35, 50, 0.6)",
            "text_main": "#ffffff",
            "text_secondary": "#b0b8c4",
            "border_color": "rgba(255, 255, 255, 0.1)",
        }
    else:
        return {
            "primary": "#FF4B4B",
            "bg_main": "#f8fafc",
            "bg_card": "#ffffff",
            "text_main": "#1e293b",
            "text_secondary": "#64748b",
            "border_color": "rgba(226, 232, 240, 1)",
        }
