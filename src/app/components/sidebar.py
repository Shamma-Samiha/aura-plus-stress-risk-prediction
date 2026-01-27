"""
AURA+ Sidebar Component
Enhanced sidebar with navigation, theme toggle, and information cards.
"""

import streamlit as st


def render_sidebar(theme: str):
    """
    Render the enhanced sidebar.
    
    Args:
        theme: Current theme ('dark' or 'light')
        
    Returns:
        str: Selected theme after toggle
    """
    sidebar_text_color = "#b0b8c4" if theme == "dark" else "#475569"
    sidebar_secondary = "#b0b8c4" if theme == "dark" else "#64748b"
    
    with st.sidebar:
        # Logo and branding
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
                <h1 style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">AURA+</h1>
                <p style="color: {sidebar_secondary}; font-size: 0.85rem; margin-top: 0.5rem;">Stress Risk Screening</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Theme toggle
        theme_label = "🌙 Dark Mode" if theme == "dark" else "☀️ Light Mode"
        if st.toggle(theme_label, value=(theme == "dark")):
            new_theme = "dark"
        else:
            new_theme = "light"
            
        st.divider()
        
        # Information card
        info_bg = "rgba(255, 75, 75, 0.1)" if theme == "dark" else "rgba(255, 75, 75, 0.06)"
        info_shadow = "box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);" if theme == "light" else ""
        
        st.markdown(f"""
            <div style="background: {info_bg}; padding: 1rem; border-radius: 10px; border-left: 3px solid #FF4B4B; {info_shadow}">
                <p style="margin: 0; font-size: 0.9rem; line-height: 1.5; color: {sidebar_text_color};">
                    <strong style="color: {sidebar_text_color};">💡 About AURA+</strong><br>
                    Uses AI to predict stress risks based on multi-dimensional patterns. Educational screening tool only.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="animate-fade-in" style="color: {sidebar_text_color};">
                <p style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Navigation</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons with modern styling
        nav_buttons = [
            ("📝 New Assessment", "Reset and start a new assessment"),
            ("📊 View Results", "See your latest assessment results"),
            ("ℹ️ About", "Learn more about AURA+")
        ]
        
        for label, tooltip in nav_buttons:
            if st.button(label, use_container_width=True, help=tooltip):
                if "New Assessment" in label:
                    # Reset session state for new assessment
                    for key in list(st.session_state.keys()):
                        if key.startswith("inp_"):
                            del st.session_state[key]
                    st.session_state["initialized"] = False
                    st.rerun()
        
        st.divider()
        
        # Quick stats or info (optional)
        st.markdown(f"""
            <div class="animate-fade-in" style="color: {sidebar_text_color}; font-size: 0.85rem;">
                <p style="margin-bottom: 0.5rem; font-weight: 600;">Quick Info</p>
                <ul style="margin: 0; padding-left: 1.2rem; line-height: 1.8;">
                    <li>Educational tool only</li>
                    <li>Not a diagnosis</li>
                    <li>Seek help if needed</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    return new_theme
