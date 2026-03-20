import streamlit as st
from trust_engine import run
import pandas as pd

# Hide UI
hide_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

st.set_page_config(page_title="SAZT System", layout="centered")

# Header
col1, col2 = st.columns([2, 5])

with col1:
    st.image("logo.png", width=250)

with col2:
    st.markdown("<h1>Situational-Aware Zero Trust</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray;'>Adaptive access control for healthcare systems</p>", unsafe_allow_html=True)

st.markdown("---")

# Inputs
st.subheader("Access Request Configuration")

col1, col2 = st.columns(2)

with col1:
    role = st.selectbox("User Role", ["doctor", "nurse", "admin"])
    context = st.selectbox("Context", ["Normal", "Emergency"])

with col2:
    behavior = st.slider("Behavior Score", 0.0, 1.0, 0.8)
    sensitivity = st.slider("Resource Sensitivity", 0.0, 1.0, 0.5)

context_val = 1 if context == "Emergency" else 0

st.markdown("---")

if st.button("Evaluate Access"):

    df = pd.DataFrame([{
        "user_role": role,
        "context": context_val,
        "behavior_score": behavior,
        "resource_sensitivity": sensitivity
    }])

    df = run(df)
    row = df.iloc[0]

    st.subheader("System Output")

    col1, col2, col3 = st.columns(3)
    col1.metric("Trust Score", f"{row['trust_score']:.2f}")
    col2.metric("Risk Level", row["risk_level"])
    col3.metric("Policy Mode", row["policy_mode"])

    st.markdown("---")

    st.subheader("System Decision")

    # 🔥 NEW FEATURE HERE
    if context == "Emergency" and row["trust_score"] < 0.4:
        st.warning("⚠️ Emergency Override Activated – Access Allowed with Monitoring")
    else:
        if row["decision"] == "ALLOW_FAST":
            st.success("⚡ Access Granted Instantly")
        elif row["decision"] == "AUTH_REQUIRED":
            st.warning("🔐 Additional Authentication Required")
        else:
            st.error("🚫 Access Blocked - Threat Detected")

    st.markdown("---")

    st.subheader("Decision Explanation")

    st.write(f"""
    ➡ Trust Score: {row['trust_score']:.2f}  
    ➡ Risk Level: {row['risk_level']}  
    ➡ Policy Mode: {row['policy_mode']}  
    ➡ Decision: {row['decision']}  

    🧠 {row['explanation']}
    """)

    st.markdown("---")

    st.subheader("Live System Log")

    st.code(f"""
[INFO] Incoming request
[INFO] Role: {role}
[INFO] Context: {context}

[INFO] Trust Score: {row['trust_score']:.2f}
[INFO] Decision: {row['decision']}

[INFO] Emergency Override: {"YES" if context == "Emergency" and row["trust_score"] < 0.4 else "NO"}
""")

st.caption("Prototype system for adaptive zero trust decision-making")