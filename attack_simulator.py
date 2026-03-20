"""
attack_simulator.py
Simulates a suspicious access attempt:
  admin + low behavior + high sensitivity + no emergency.
"""

import pandas as pd
from trust_engine import run


def simulate_attack():
    """
    Runs a single attack scenario through the trust engine
    and prints the result.
    """
    attack_case = pd.DataFrame([{
        "user_role":            "admin",
        "context":              0,
        "behavior_score":       0.10,
        "resource_sensitivity": 0.95,
    }])

    result = run(attack_case)
    row    = result.iloc[0]

    print("\n── ATTACK SIMULATION " + "─" * 27)
    print(f"   Role        : {row['user_role']}")
    print(f"   Context     : Normal (no emergency)")
    print(f"   Behavior    : {row['behavior_score']:.2f}  ← suspicious")
    print(f"   Sensitivity : {row['resource_sensitivity']:.2f}  ← high-value resource")
    print(f"   Trust Score : {row['trust_score']:.2f}")
    print(f"   Decision    : {row['decision']}")

    if row["decision"] == "BLOCK":
        print("\n   🚨 Attack Detected and Blocked")
    else:
        print(f"\n   ⚡ Suspicious — {row['decision']}")

    print("─" * 48)
