import json
from pathlib import Path

lines = Path("experiments/runs/mrlf-benchmark/flask.codeclue-detail").read_text(encoding="utf-8").strip().split("\n")
for line in lines:
    rec = json.loads(line)
    sym = rec["symbol"]
    if "session" in sym.lower() or "Session" in sym:
        print(f"=== {sym} ({rec['type']}) ===")
        print(f"  file: {rec['file']}:{rec['lines']}")
        print(f"  purpose: {rec['purpose']}")
        print(f"  calls: {rec['calls'][:5]}")
        print(f"  called_by: {rec['called_by'][:5]}")
        src = rec["source"][:300] if rec["source"] else "(no source)"
        print(f"  source: {src}...")
        print()
