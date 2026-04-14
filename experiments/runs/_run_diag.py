import sys
from pathlib import Path

# Redirect stdout to file for reliable output capture
out_file = Path("experiments/runs/mrlf-benchmark/focus-diag-out.txt")
original_stdout = sys.stdout
sys.stdout = out_file.open("w", encoding="utf-8")

# Import and run the diagnostic
exec(Path("experiments/runs/diagnose_focus_recall.py").read_text(encoding="utf-8"))

sys.stdout.close()
sys.stdout = original_stdout

# Print the captured output
print(out_file.read_text(encoding="utf-8"))
