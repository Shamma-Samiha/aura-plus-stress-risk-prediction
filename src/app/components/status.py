"""
AURA+ Status Components
Progress indicators, status badges, and loading states.
"""

import streamlit as st


def render_progress_bar(progress: float, label: str = "", theme: str = "dark"):
    """
    Render a modern progress bar.
    
    Args:
        progress: Progress value (0.0 to 1.0)
        label: Optional label text
        theme: Current theme
    """
    progress_pct = min(max(progress * 100, 0), 100)
    text_color = "#b0b8c4" if theme == "dark" else "#64748b"
    
    progress_html = f"""
    <div style="margin: 1rem 0;">
        {f'<p style="color: {text_color}; font-size: 0.9rem; margin-bottom: 0.5rem; font-weight: 600;">{label}</p>' if label else ''}
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress_pct}%;"></div>
        </div>
        <p style="color: {text_color}; font-size: 0.85rem; margin-top: 0.5rem; text-align: right;">{progress_pct:.1f}%</p>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)


def render_status_indicator(status_type: str, message: str, theme: str = "dark"):
    """
    Render a status indicator badge.
    
    Args:
        status_type: 'success', 'warning', 'error', or 'info'
        message: Status message text
        theme: Current theme
    """
    status_html = f"""
    <div class="status-indicator status-{status_type} animate-fade-in">
        {message}
    </div>
    """
    
    st.markdown(status_html, unsafe_allow_html=True)


def render_loading_spinner(message: str = "Loading...", theme: str = "dark"):
    """
    Render a loading spinner with message.
    
    Args:
        message: Loading message text
        theme: Current theme
    """
    text_color = "#b0b8c4" if theme == "dark" else "#64748b"
    
    spinner_html = f"""
    <div style="display: flex; align-items: center; gap: 1rem; padding: 2rem; justify-content: center;">
        <div class="loading-spinner"></div>
        <p style="color: {text_color}; font-size: 1rem; margin: 0;">{message}</p>
    </div>
    """
    
    st.markdown(spinner_html, unsafe_allow_html=True)


def render_step_indicator(current_step: int, total_steps: int, labels: list = None, theme: str = "dark"):
    """
    Render a step indicator for multi-step processes.
    
    Args:
        current_step: Current step (1-indexed)
        total_steps: Total number of steps
        labels: Optional list of step labels
        theme: Current theme
    """
    text_color = "#b0b8c4" if theme == "dark" else "#64748b"
    active_color = "#FF4B4B"
    inactive_color = "#64748b" if theme == "dark" else "#cbd5e1"
    
    steps_html = '<div style="display: flex; align-items: center; justify-content: space-between; margin: 2rem 0; gap: 0.5rem;">'
    
    for i in range(1, total_steps + 1):
        is_active = i == current_step
        is_completed = i < current_step
        
        step_color = active_color if (is_active or is_completed) else inactive_color
        step_bg = f"rgba(255, 75, 75, 0.2)" if (is_active or is_completed) else "transparent"
        
        step_label = labels[i - 1] if labels and i <= len(labels) else f"Step {i}"
        
        steps_html += f"""
        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 0.5rem;">
            <div style="
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: {step_bg};
                border: 2px solid {step_color};
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                color: {step_color};
                transition: all var(--transition-base);
                {'box-shadow: 0 0 20px rgba(255, 75, 75, 0.4);' if is_active else ''}
            ">
                {'✓' if is_completed else i}
            </div>
            <span style="font-size: 0.85rem; color: {text_color}; text-align: center;">{step_label}</span>
        </div>
        """
        
        if i < total_steps:
            steps_html += f"""
            <div style="
                flex: 1;
                height: 2px;
                background: {'linear-gradient(90deg, ' + active_color + ', ' + (active_color if i < current_step else inactive_color) + ')'};
                margin: 0 0.5rem;
            "></div>
            """
    
    steps_html += '</div>'
    
    st.markdown(steps_html, unsafe_allow_html=True)
