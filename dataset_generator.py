"""
dataset_generator.py
Generates a synthetic hospital access control dataset with anomalies.
"""

import numpy as np
import pandas as pd


def generate_dataset(n=300, seed=42):
    """
    Returns a DataFrame with n rows of synthetic hospital access data.
    Includes ~15% anomalous rows with low behavior_score.
    """
    np.random.seed(seed)

    # User roles
    roles = np.random.choice(
        ["doctor", "nurse", "admin"], size=n, p=[0.35, 0.45, 0.20]
    )

    # Context: doctors skewed toward emergency
    context = np.array([
        np.random.choice([0, 1], p=[0.40, 0.60]) if r == "doctor"
        else np.random.choice([0, 1], p=[0.75, 0.25])
        for r in roles
    ])

    # Behavior score: 15% anomalous (< 0.4), 85% normal (>= 0.6)
    is_anomaly = np.random.choice([True, False], size=n, p=[0.15, 0.85])
    behavior_score = np.where(
        is_anomaly,
        np.random.uniform(0.05, 0.39, size=n),
        np.random.uniform(0.60, 1.00, size=n)
    ).round(4)

    # Resource sensitivity: varies by role
    sens_range = {"doctor": (0.5, 1.0), "nurse": (0.3, 0.85), "admin": (0.1, 0.60)}
    resource_sensitivity = np.array([
        round(np.random.uniform(*sens_range[r]), 4) for r in roles
    ])

    return pd.DataFrame({
        "user_role":            roles,
        "context":              context,
        "behavior_score":       behavior_score,
        "resource_sensitivity": resource_sensitivity,
        "is_anomaly":           is_anomaly.astype(int)
    })
