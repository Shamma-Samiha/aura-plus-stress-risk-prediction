"""
AURA+ Navbar Component
Modern top navigation bar with branding and theme toggle.
"""

import streamlit as st


def render_navbar(theme: str):
    """
    Render the top navigation bar.
    
    Args:
        theme: Current theme ('dark' or 'light')
    """
    theme_emoji = "🌙" if theme == "dark" else "☀️"
    theme_text_color = "#b0b8c4" if theme == "dark" else "#64748b"
    navbar_bg = "rgba(15, 20, 35, 0.95)" if theme == "dark" else "rgba(255, 255, 255, 0.95)"
    navbar_border = "rgba(255, 255, 255, 0.1)" if theme == "dark" else "rgba(226, 232, 240, 1)"
    navbar_shadow = "0 4px 16px rgba(0, 0, 0, 0.25)" if theme == "dark" else "0 4px 16px rgba(0, 0, 0, 0.08)"
    
    # Build navbar HTML with proper escaping
    navbar_html = (
        '<div class="glass-navbar animate-slide-in-left" style="'
        f'position: fixed; top: 0; left: 0; right: 0; height: 65px; '
        f'background: {navbar_bg}; backdrop-filter: blur(20px); '
        f'-webkit-backdrop-filter: blur(20px); border-bottom: 1px solid {navbar_border}; '
        f'z-index: 30; display: flex; align-items: center; justify-content: space-between; '
        f'padding: 0 2rem; box-shadow: {navbar_shadow};'
        '">'
        '<div class="hover-scale" style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">'
        '<span style="font-size: 2rem; animation: float 3s ease-in-out infinite;">🧠</span>'
        '<span style="font-size: 1.5rem; font-weight: 800; '
        'background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%); '
        '-webkit-background-clip: text; -webkit-text-fill-color: transparent; '
        'background-clip: text;">AURA+</span>'
        '</div>'
        f'<div style="display: flex; align-items: center; gap: 1rem; color: {theme_text_color}; font-size: 0.9rem;">'
        f'<span class="animate-pulse">{theme_emoji} {theme.title()} Mode</span>'
        '</div>'
        '</div>'
        '<div style="height: 80px;"></div>'
    )
    
    st.markdown(navbar_html, unsafe_allow_html=True)
