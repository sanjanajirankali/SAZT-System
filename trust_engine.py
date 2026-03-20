import pandas as pd

# ── Constants ─────────────────────────────────────────────

ROLE_WEIGHTS = {"doctor": 1.0, "nurse": 0.8, "admin": 0.6}

LATENCY_MAP = {
    "ALLOW_FAST": 0.5,
    "AUTH_REQUIRED": 3.0,
    "BLOCK": 6.0,
}

STATIC_LATENCY = 4.0


# ── Core pipeline ─────────────────────────────────────────

def run(df):
    df = df.copy()

    df = _add_role_weight(df)
    df = _compute_trust_score(df)
    df = _apply_anomaly_penalty(df)
    df = _assign_decision(df)
    df = _assign_risk_level(df)
    df = _assign_latency(df)
    df = _add_confidence(df)
    df = _add_policy_mode(df)
    df = _add_explanation(df)

    return df


# ── Internal steps ───────────────────────────────────────

def _add_role_weight(df):
    df["role_weight"] = df["user_role"].map(ROLE_WEIGHTS)
    return df


def _compute_trust_score(df):
    df["trust_score"] = (
        0.4 * df["context"] +
        0.3 * df["behavior_score"] +
        0.2 * df["role_weight"] +
        0.1 * (1 - df["resource_sensitivity"])
    ).round(4)
    return df


def _apply_anomaly_penalty(df):
    df["anomaly_flag"] = (df["behavior_score"] < 0.4).astype(int)
    df["trust_score"] = (df["trust_score"] - 0.4 * df["anomaly_flag"]).clip(0).round(4)
    return df


def _assign_decision(df):
    def decide(score):
        if score > 0.7:
            return "ALLOW_FAST"
        elif score > 0.4:
            return "AUTH_REQUIRED"
        else:
            return "BLOCK"

    df["decision"] = df["trust_score"].apply(decide)
    return df


def _assign_risk_level(df):
    def risk(score):
        if score > 0.7:
            return "LOW"
        elif score > 0.4:
            return "MEDIUM"
        else:
            return "HIGH"

    df["risk_level"] = df["trust_score"].apply(risk)
    return df


def _assign_latency(df):
    df["sazt_latency"] = df["decision"].map(LATENCY_MAP)
    df["static_latency"] = STATIC_LATENCY
    return df


# ── NEW FEATURES (🔥 WOW LAYER) ───────────────────────────

def _add_confidence(df):
    df["confidence"] = df["trust_score"].apply(lambda x: round(x * 100, 2))
    return df


def _add_policy_mode(df):
    def policy(score):
        if score > 0.8:
            return "RELAXED"
        elif score > 0.5:
            return "BALANCED"
        else:
            return "STRICT"

    df["policy_mode"] = df["trust_score"].apply(policy)
    return df


def _add_explanation(df):
    def explain(row):
        reasons = []

        if row["context"] == 1:
            reasons.append("Emergency context")
        else:
            reasons.append("Normal context")

        if row["behavior_score"] < 0.4:
            reasons.append("Suspicious behavior")
        else:
            reasons.append("Normal behavior")

        if row["resource_sensitivity"] > 0.75:
            reasons.append("High sensitivity resource")

        if row["user_role"] == "doctor":
            reasons.append("Trusted doctor role")
        elif row["user_role"] == "admin":
            reasons.append("Lower trust admin role")

        return " | ".join(reasons)

    df["explanation"] = df.apply(explain, axis=1)
    return df


# ── Output Helpers ───────────────────────────────────────

def print_summary(df):
    print("\n" + "="*50)
    print("SAZT — SYSTEM SUMMARY")
    print("="*50)

    print(f"Total records      : {len(df)}")
    print(f"Anomalies detected : {df['anomaly_flag'].sum()}")
    print(f"Avg SAZT latency   : {df['sazt_latency'].mean():.4f}")
    print(f"Avg Static latency : {df['static_latency'].mean():.4f}")
    print(f"Latency saved      : {(df['static_latency'].mean() - df['sazt_latency'].mean()):.4f}")

    print("\nDecision Distribution:")
    print(df["decision"].value_counts())


def print_sample(df):
    row = df.iloc[0]

    print("\n=== SAMPLE DECISION ===")
    print(f"Role        : {row['user_role']}")
    print(f"Trust Score : {row['trust_score']:.2f}")
    print(f"Confidence  : {row['confidence']}%")
    print(f"Policy Mode : {row['policy_mode']}")
    print(f"Risk Level  : {row['risk_level']}")
    print(f"Decision    : {row['decision']}")
    print(f"Explanation : {row['explanation']}")