"""
AURA+ Model Utilities
Functions for loading models, making predictions, and explaining results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from .constants import MODEL_PATH, DATA_PATH, STRESS_LABELS, QUESTION_MAP, SUGGESTION_RULES


@st.cache_resource
def load_model():
    """Load the trained logistic regression model."""
    if not MODEL_PATH.exists():
        st.error("Model file not found. Train baseline first: python src/models/01_train_baseline.py")
        st.stop()
    return joblib.load(MODEL_PATH)


def get_feature_names():
    """Get feature names from the processed dataset."""
    if not DATA_PATH.exists():
        st.error("Processed dataset not found. Run cleaning first.")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    return [c for c in df.columns if c != "stress_level"]


def explain_with_coefficients(pipeline, user_df, feature_names, top_k=6):
    """
    Explain prediction using model coefficients.
    
    Args:
        pipeline: Trained sklearn pipeline
        user_df: DataFrame with user inputs
        feature_names: List of feature names
        top_k: Number of top contributors to return
        
    Returns:
        tuple: (predicted_class, top_contributions)
    """
    scaler = pipeline.named_steps["scaler"]
    model = pipeline.named_steps["model"]

    # Use pipeline for prediction (handles scaling internally)
    pred_class = int(pipeline.predict(user_df[feature_names])[0])
    
    # Get scaled data for coefficient explanation
    x_scaled = scaler.transform(user_df[feature_names])
    
    # Handle coefficient access - works for both binary and multiclass
    if len(model.coef_.shape) == 1:
        # Binary classification
        coef = model.coef_
    else:
        # Multiclass classification
        coef = model.coef_[pred_class]
    
    contributions = x_scaled.flatten() * coef
    expl = pd.Series(contributions, index=feature_names).sort_values(key=np.abs, ascending=False)
    return pred_class, expl.head(top_k)


def format_feature_label(feat: str) -> str:
    """Convert feature name to human-friendly label."""
    meta = QUESTION_MAP.get(feat)
    if meta:
        return meta["label"]
    return feat.replace("_", " ").title()


def make_report_text(pred_label, probs, top_contrib, suggestions):
    """
    Generate downloadable text report.
    
    Args:
        pred_label: Predicted stress level label
        probs: Probability distribution
        top_contrib: Top contributing features
        suggestions: List of suggestions
        
    Returns:
        str: Formatted report text
    """
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
    """Initialize session state with default values for all features."""
    for feat in feature_names:
        meta = QUESTION_MAP.get(feat, {})
        default = meta.get("default", 3)
        st.session_state[f"inp_{feat}"] = default


def predict_proba_safe(pipeline, X):
    """
    Robustly compute probability estimates for a sklearn pipeline where the
    final estimator may not expose `predict_proba` properly due to serialization
    / sklearn version differences.

    Args:
        pipeline: sklearn Pipeline with steps including a scaler and a model
        X: array-like or DataFrame of input features (unscaled)

    Returns:
        np.ndarray: probability estimates with shape (n_samples, n_classes)
    """
    scaler = pipeline.named_steps.get("scaler")
    model = pipeline.named_steps.get("model")

    # Prepare scaled inputs if a scaler is present
    if scaler is not None:
        X_in = scaler.transform(X)
    else:
        X_in = X

    # Prefer pipeline.predict_proba when available
    try:
        return pipeline.predict_proba(X)
    except Exception:
        pass

    # Try model-specific fallbacks
    # 1) If estimator exposes _predict_proba_lr (LogisticRegression internals)
    if hasattr(model, "_predict_proba_lr"):
        try:
            return model._predict_proba_lr(X_in)
        except Exception:
            pass

    # 2) Use decision_function + softmax / sigmoid
    import numpy as _np
    if hasattr(model, "decision_function"):
        scores = model.decision_function(X_in)
        # Binary case: scores shape (n_samples,)
        if scores.ndim == 1:
            probs_pos = 1.0 / (1.0 + _np.exp(-scores))
            probs = _np.vstack([1 - probs_pos, probs_pos]).T
            return probs
        # Multiclass: apply softmax row-wise
        exp = _np.exp(scores - _np.max(scores, axis=1, keepdims=True))
        probs = exp / _np.sum(exp, axis=1, keepdims=True)
        return probs

    # 3) Last resort: if model has predict_proba but pipeline call failed, try estimator directly
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X_in)

    # Could not compute probabilities
    raise AttributeError("Unable to compute probability estimates for the provided model.")
