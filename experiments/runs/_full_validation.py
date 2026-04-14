"""Full validation: Phase 3 + Phase 4 + Django + Nest + Go (Gin+Chi).

Runs everything from scratch and outputs a consolidated summary.
Writes to experiments/runs/mrlf-benchmark/full-validation.log
"""
import sys, time, json, subprocess
from pathlib import Path

LOG = Path("experiments/runs/mrlf-benchmark/full-validation.log")
LOG.parent.mkdir(parents=True, exist_ok=True)
log_file = LOG.open("w", encoding="utf-8", buffering=1)
orig = sys.stdout
sys.stdout = log_file

print(f"=== FULL VALIDATION RUN ===")
print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Phase 3
print("--- PHASE 3: Localization (4 repos × 5 TFs = 20 tasks) ---")
sys.stdout.flush()
subprocess.run([sys.executable, "experiments/runs/run_phase3_localization.py"],
               stdout=log_file, stderr=log_file)

# Phase 4
print("\n--- PHASE 4: Consumption (20 tasks) ---")
sys.stdout.flush()
subprocess.run([sys.executable, "experiments/runs/run_phase4_consumption.py"],
               stdout=log_file, stderr=log_file)

# Django
print("\n--- DJANGO (5 tasks) ---")
sys.stdout.flush()
subprocess.run([sys.executable, "experiments/runs/_django_full_test.py"],
               stdout=log_file, stderr=log_file)

# Nest
print("\n--- NEST (5 tasks) ---")
sys.stdout.flush()
subprocess.run([sys.executable, "experiments/runs/_nest_validation_test.py"],
               stdout=log_file, stderr=log_file)

# Go (Gin + Chi)
print("\n--- GO: Gin + Chi (8 tasks) ---")
sys.stdout.flush()
subprocess.run([sys.executable, "experiments/runs/_go_validation.py"],
               stdout=log_file, stderr=log_file)

print("\n=== FULL VALIDATION COMPLETE ===")
sys.stdout = orig
log_file.close()

# Print summary
print(LOG.read_text(encoding="utf-8")[-2000:])
