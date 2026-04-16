"""Compute Wilson confidence intervals for all CodeClue metrics."""
import math

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0, center - spread), min(1, center + spread))

data = [
    ("v2.3 STRUCTURAL (combined)", 29, 32),
    ("v2.3 RELATIONAL (combined)", 25, 32),
    ("v2.3 MECHANISTIC (combined)", 26, 48),
    ("v2.3 TOTAL (combined)", 80, 112),
    ("v2.3 Dev", 27, 40),
    ("v2.3 Blind", 53, 72),
    ("v2.3 Blind requests", 16, 24),
    ("v2.3 Blind echo", 19, 24),
    ("v2.3 Blind zod", 18, 24),
    ("Baseline raw-topk", 2, 24),
    ("Ablation File1-only (mech)", 18, 36),
]

print(f"{'Metric':<35s} {'Score':>10s} {'95% CI':>20s}")
print("-" * 70)
for label, k, n in data:
    lo, hi = wilson_ci(k, n)
    pct = 100 * k / n
    print(f"{label:<35s} {k:>3d}/{n:<3d} = {pct:5.1f}%   [{100*lo:5.1f}%, {100*hi:5.1f}%]")
