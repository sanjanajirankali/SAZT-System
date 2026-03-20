from dataset_generator import generate_dataset
from trust_engine import run, print_summary, print_sample
from attack_simulator import simulate_attack
from visualization import plot_results


# -----------------------------
# LIVE LOGS (🔥 WOW FEATURE)
# -----------------------------
def live_logs(df):
    print("\n" + "="*50)
    print("🚨 LIVE SECURITY STREAM")
    print("="*50)

    for i, row in df.head(10).iterrows():
        print(f"[REQUEST {i}] {row['user_role']} accessing system")
        print(f"  → Trust Score : {row['trust_score']:.2f}")
        print(f"  → Decision    : {row['decision']}")
        print(f"  → Risk Level  : {row['risk_level']}")
        print(f"  → Reason      : {row['explanation']}")
        print("-"*50)


# -----------------------------
# DEMO MODE (INTERACTIVE)
# -----------------------------
def run_demo_mode():
    print("\n" + "="*50)
    print("🎯 SAZT DEMO MODE")
    print("="*50)

    print("\nSelect Policy Mode:")
    print("1. Strict")
    print("2. Balanced")
    print("3. Emergency-First")

    policy_choice = input("Enter choice (1-3): ")

    if policy_choice == "1":
        weights = (0.3, 0.3, 0.2, 0.2)
        policy = "STRICT"
    elif policy_choice == "3":
        weights = (0.5, 0.2, 0.2, 0.1)
        policy = "EMERGENCY-FIRST"
    else:
        weights = (0.4, 0.3, 0.2, 0.1)
        policy = "BALANCED"

    print(f"\n[LOG] Policy Mode: {policy}")

    print("\nChoose scenario:")
    print("1. Normal")
    print("2. Emergency")
    print("3. Attack")
    print("4. Custom")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        user_role, context, behavior, sensitivity = "nurse", 0, 0.8, 0.4
    elif choice == "2":
        user_role, context, behavior, sensitivity = "doctor", 1, 0.9, 0.6
    elif choice == "3":
        user_role, context, behavior, sensitivity = "admin", 0, 0.1, 0.95
    elif choice == "4":
        user_role = input("Role: ")
        context = int(input("Context (0/1): "))
        behavior = float(input("Behavior (0-1): "))
        sensitivity = float(input("Sensitivity (0-1): "))
    else:
        print("Invalid choice")
        return

    print("\n[LOG] Computing trust...")

    role_map = {"doctor":1.0, "nurse":0.8, "admin":0.6}
    role_weight = role_map.get(user_role, 0.5)

    trust = (
        weights[0]*context +
        weights[1]*behavior +
        weights[2]*role_weight +
        weights[3]*(1-sensitivity)
    )

    if behavior < 0.4:
        print("[LOG] Anomaly detected → reducing trust")
        trust -= 0.4

    trust = max(trust, 0)

    if trust > 0.7:
        decision, risk = "ALLOW_FAST", "LOW"
    elif trust > 0.4:
        decision, risk = "AUTH_REQUIRED", "MEDIUM"
    else:
        decision, risk = "BLOCK", "HIGH"

    confidence = trust * 100

    print("\n" + "="*50)
    print("🔍 RESULT")
    print("="*50)

    print(f"Trust Score : {trust:.2f}")
    print(f"Confidence  : {confidence:.1f}%")
    print(f"Risk Level  : {risk}")
    print(f"Decision    : {decision}")

    if decision == "BLOCK":
        print("🚨 Attack Detected / Access Denied")


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":

    print("\nSAZT — Starting System...\n")

    # 1. Generate dataset
    df = generate_dataset(n=300)

    # 2. Run trust engine
    df = run(df)

    # 3. Summary + sample
    print_summary(df)
    print_sample(df)

    # 4. Attack simulation
    simulate_attack()

    # 5. 🔥 Live logs (NEW WOW FEATURE)
    live_logs(df)

    # 6. Save dataset
    df.to_csv("sazt_output.csv", index=False)
    print("\nDataset saved → sazt_output.csv")

    # 7. Graphs
    plot_results(df)

    # 8. Demo mode (interactive)
    run_demo_mode()