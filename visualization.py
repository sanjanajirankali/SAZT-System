"""
visualization.py
Plots latency comparison and decision distribution for the SAZT system.
"""

import matplotlib.pyplot as plt


def plot_results(df):
    """
    Generates and saves two charts:
      1. SAZT vs Static Zero Trust — average latency
      2. Decision distribution (ALLOW_FAST / AUTH_REQUIRED / BLOCK)
    """
    avg_sazt  = df["sazt_latency"].mean()
    avg_stat  = df["static_latency"].mean()
    counts    = df["decision"].value_counts().reindex(["ALLOW_FAST", "AUTH_REQUIRED", "BLOCK"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("SAZT — Performance Overview", fontsize=14, fontweight="bold")

    # ── Chart 1: Latency comparison ───────────────────────────────────────────
    bars1 = axes[0].bar(
        ["SAZT", "Static Zero Trust"],
        [avg_sazt, avg_stat],
        color=["#378ADD", "#888780"],
        width=0.4,
        zorder=3,
    )
    axes[0].set_title("Average Latency Comparison")
    axes[0].set_ylabel("Latency (units)")
    axes[0].set_ylim(0, 5)
    axes[0].yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0)
    axes[0].set_axisbelow(True)
    for bar, val in zip(bars1, [avg_sazt, avg_stat]):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2, val + 0.06,
            f"{val:.2f}", ha="center", fontweight="bold"
        )

    # ── Chart 2: Decision distribution ───────────────────────────────────────
    bars2 = axes[1].bar(
        counts.index,
        counts.values,
        color=["#1D9E75", "#378ADD", "#E24B4A"],
        width=0.5,
        zorder=3,
    )
    axes[1].set_title("Decision Distribution")
    axes[1].set_ylabel("Number of Records")
    axes[1].yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0)
    axes[1].set_axisbelow(True)
    for bar, val in zip(bars2, counts.values):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2, val + 1,
            str(val), ha="center", fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig("sazt_charts.png", dpi=150, bbox_inches="tight")
    print("\n   Charts saved → sazt_charts.png")
    plt.show()
