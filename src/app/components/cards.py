"""
AURA+ Card Components
Reusable card components for displaying information and results.
"""

import streamlit as st


def render_info_card(title: str, content: str, emoji: str = "ℹ️", theme: str = "dark", card_type: str = "info"):
    """
    Render an information card with glassmorphism.
    
    Args:
        title: Card title
        content: Card content
        emoji: Icon emoji
        theme: Current theme
        card_type: Card type ('info', 'warning', 'success', 'error')
    """
    # Color scheme based on card type
    color_schemes = {
        "info": {
            "bg": "rgba(75, 172, 255, 0.1)" if theme == "dark" else "rgba(75, 172, 255, 0.06)",
            "border": "#4BACFF",
            "glow": "rgba(75, 172, 255, 0.3)"
        },
        "warning": {
            "bg": "rgba(255, 193, 7, 0.1)" if theme == "dark" else "rgba(255, 193, 7, 0.06)",
            "border": "#ffc107",
            "glow": "rgba(255, 193, 7, 0.3)"
        },
        "success": {
            "bg": "rgba(124, 255, 178, 0.1)" if theme == "dark" else "rgba(124, 255, 178, 0.06)",
            "border": "#7CFFB2",
            "glow": "rgba(124, 255, 178, 0.3)"
        },
        "error": {
            "bg": "rgba(255, 75, 75, 0.1)" if theme == "dark" else "rgba(255, 75, 75, 0.06)",
            "border": "#FF4B4B",
            "glow": "rgba(255, 75, 75, 0.3)"
        }
    }
    
    scheme = color_schemes.get(card_type, color_schemes["info"])
    text_color = "#b0b8c4" if theme == "dark" else "#475569"
    title_color = "#ffffff" if theme == "dark" else "#0f172a"
    shadow = "0 4px 20px rgba(0, 0, 0, 0.3)" if theme == "dark" else "0 2px 8px rgba(0, 0, 0, 0.06)"
    
    card_html = f"""
<div class="glass-card animate-fade-in hover-lift" style="background: {scheme['bg']};border-left: 4px solid {scheme['border']};padding: 1.25rem;border-radius: 12px;margin-bottom: 1.5rem;box-shadow: {shadow}, 0 0 20px {scheme['glow']};backdrop-filter: blur(20px);-webkit-backdrop-filter: blur(20px);">
<div style="display: flex; align-items: start; gap: 0.75rem;">
<span style="font-size: 1.5rem; animation: float 3s ease-in-out infinite;">{emoji}</span>
<div style="flex: 1;">
<strong style="font-size: 1rem; display: block; margin-bottom: 0.5rem; color: {title_color}; font-weight: 700;">{title}</strong>
<p style="margin: 0; font-size: 0.9rem; line-height: 1.6; color: {text_color};">{content}</p>
</div>
</div>
</div>
"""
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "", theme: str = "dark"):
    """
    Streamlit Cloud–safe header renderer.
    Title is ALWAYS visible, gradient applied only when supported.
    """

    subtitle_color = "#b0b8c4" if theme == "dark" else "#64748b"

    st.markdown(
        f"""
        <div style="text-align:center; margin: 2rem 0 2.5rem 0;">
            <h1
                style="
                    font-size:3.2rem;
                    font-weight:800;
                    margin:0;
                    line-height:1.1;
                    letter-spacing:-0.02em;
                    color:#FF4B4B;
                    background: linear-gradient(135deg,#FF4B4B,#FF6B6B,#FF8A8A);
                    background-clip:text;
                    -webkit-background-clip:text;
                    display:inline-block;
                "
            >
                {title}
            </h1>

            <p style="
                margin-top:0.6rem;
                font-size:1.05rem;
                color:{subtitle_color};
                font-weight:400;
            ">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )




def render_result_card(content: str, theme: str = "dark"):
    """
    Render a result card with glassmorphism effect.
    
    Args:
        content: HTML content for the card
        theme: Current theme
    """
    card_html = f"""
<div class="result-card glass-card animate-scale-in">
{content}
</div>
"""
    
    st.markdown(card_html, unsafe_allow_html=True)
