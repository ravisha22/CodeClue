"""Compute Wilson CIs and cluster-aware bootstrap CIs for v2.5 results."""
import math
import random

random.seed(42)

def wilson_ci(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return (max(0, center - spread), min(1, center + spread))

def cluster_bootstrap(repo_scores, n_boot=10000):
    """Bootstrap CI treating each repo as a cluster (non-independent facts)."""
    repos = list(repo_scores.keys())
    boot_means = []
    for _ in range(n_boot):
        sample = [random.choice(repos) for _ in repos]
        total_c = sum(repo_scores[r][0] for r in sample)
        total_t = sum(repo_scores[r][1] for r in sample)
        if total_t > 0:
            boot_means.append(total_c / total_t)
    boot_means.sort()
    lo = boot_means[int(0.025 * n_boot)]
    hi = boot_means[int(0.975 * n_boot)]
    return (lo, hi)

# v2.5 blind results by repo
blind_repos = {
    "requests": (17, 24), "echo": (14, 24), "zod": (20, 24),
    "fastapi": (6, 24), "gin": (10, 24), "express": (11, 24), "httpx": (8, 24),
}

# By task family across blind repos
blind_struct = {
    "requests": (6, 8), "echo": (5, 8), "zod": (7, 8),
    "fastapi": (2, 8), "gin": (3, 8), "express": (4, 8), "httpx": (2, 8),
}
blind_rel = {
    "requests": (6, 8), "echo": (5, 8), "zod": (7, 8),
    "fastapi": (2, 8), "gin": (5, 8), "express": (5, 8), "httpx": (4, 8),
}
blind_mech = {
    "requests": (5, 8), "echo": (4, 8), "zod": (6, 8),
    "fastapi": (2, 8), "gin": (2, 8), "express": (2, 8), "httpx": (2, 8),
}

# Dev results
dev_repos = {"aiohttp": (10, 16), "fiber": (5, 16), "click": (7, 8)}

print("=" * 80)
print("CodeClue v2.5 — Confidence Intervals")
print("=" * 80)

metrics = [
    ("BLIND OVERALL", blind_repos),
    ("BLIND STRUCTURAL", blind_struct),
    ("BLIND RELATIONAL", blind_rel),
    ("BLIND MECHANISTIC", blind_mech),
    ("DEV OVERALL", dev_repos),
]

print(f"\n{'Metric':<25s} {'Score':>10s} {'Wilson 95%':>18s} {'Cluster 95%':>18s}")
print("-" * 75)

for label, repo_data in metrics:
    total_c = sum(v[0] for v in repo_data.values())
    total_t = sum(v[1] for v in repo_data.values())
    pct = 100 * total_c / total_t
    w_lo, w_hi = wilson_ci(total_c, total_t)
    c_lo, c_hi = cluster_bootstrap(repo_data)
    print(f"{label:<25s} {total_c:>3d}/{total_t:<3d} = {pct:5.1f}%"
          f"   [{100*w_lo:5.1f}%, {100*w_hi:5.1f}%]"
          f"   [{100*c_lo:5.1f}%, {100*c_hi:5.1f}%]")

# Individual repos
print(f"\n{'Repo':<15s} {'Score':>10s} {'Wilson 95%':>18s}")
print("-" * 50)
for repo in sorted(blind_repos, key=lambda r: blind_repos[r][0]/blind_repos[r][1], reverse=True):
    c, t = blind_repos[repo]
    pct = 100 * c / t
    w_lo, w_hi = wilson_ci(c, t)
    print(f"{repo:<15s} {c:>3d}/{t:<3d} = {pct:5.1f}%   [{100*w_lo:5.1f}%, {100*w_hi:5.1f}%]")

# Cross-model
print(f"\n{'Model':<15s} {'Score':>10s} {'Wilson 95%':>18s}")
print("-" * 50)
cross = [("GPT-5.4", 24, 32), ("Sonnet 4.6 +scaffold", 26, 32),
         ("Sonnet 4.6", 16, 32), ("Goldeneye", 14, 32)]
for name, c, t in cross:
    pct = 100 * c / t
    w_lo, w_hi = wilson_ci(c, t)
    print(f"{name:<20s} {c:>3d}/{t:<3d} = {pct:5.1f}%   [{100*w_lo:5.1f}%, {100*w_hi:5.1f}%]")

# Baselines
print(f"\n{'Baseline':<20s} {'Score':>10s} {'Wilson 95%':>18s}")
print("-" * 55)
baselines = [("Raw top-k (6K tok)", 2, 24), ("Summary (filenames)", 0, 24)]
for name, c, t in baselines:
    pct = 100 * c / t
    w_lo, w_hi = wilson_ci(c, t)
    print(f"{name:<20s} {c:>3d}/{t:<3d} = {pct:5.1f}%   [{100*w_lo:5.1f}%, {100*w_hi:5.1f}%]")

# Ablation
print(f"\n{'Ablation':<25s} {'Score':>10s} {'Wilson 95%':>18s}")
print("-" * 60)
ablation = [("File 1 only", 11, 48), ("File 1 + File 2", 23, 48)]
for name, c, t in ablation:
    pct = 100 * c / t
    w_lo, w_hi = wilson_ci(c, t)
    print(f"{name:<25s} {c:>3d}/{t:<3d} = {pct:5.1f}%   [{100*w_lo:5.1f}%, {100*w_hi:5.1f}%]")
