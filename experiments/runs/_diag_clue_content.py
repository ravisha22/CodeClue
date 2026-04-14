"""Diagnostic: Check the actual generated Flask clue for session content."""
import json

# Check if NullSession appears in the clue with raises
clue_file = "experiments/runs/mrlf-benchmark/flask.codeclue"
try:
    with open(clue_file) as f:
        content = f.read()
    
    # Find NullSession in FOCUS section
    in_focus = False
    for line in content.split("\n"):
        if "-- FOCUS" in line:
            in_focus = True
        if "-- GAPS" in line:
            in_focus = False
        if in_focus and "NullSession" in line:
            # Print context around it
            idx = content.index(line)
            start = max(0, content.rfind("\n\n", 0, idx))
            end = content.find("\n\n", idx + len(line))
            if end == -1:
                end = min(len(content), idx + 500)
            print("=== NullSession in FOCUS ===")
            print(content[start:end])
            print()
    
    # Also check SecureCookieSessionInterface
    for line in content.split("\n"):
        if in_focus and "SecureCookieSessionInterface" in line:
            idx = content.index(line)
            start = max(0, content.rfind("\n\n", 0, idx))
            end = content.find("\n\n", idx + len(line))
            if end == -1:
                end = min(len(content), idx + 500)
            print("=== SecureCookieSessionInterface in FOCUS ===")
            print(content[start:end])
            print()
            
    # Count how many FOCUS entries exist
    focus_entries = [l for l in content.split("\n") if l and not l.startswith("  ") and not l.startswith("--") and not l.startswith("=") and not l.startswith("?")]
    
    # Find calls line for SecureCookieSessionInterface
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "SecureCookieSessionInterface" in line and "FOCUS" not in line:
            # Print the entry (next ~10 lines)
            print("=== SecureCookieSessionInterface entry ===")
            for j in range(i, min(i+12, len(lines))):
                print(lines[j])
            print()
            break
            
except FileNotFoundError:
    print(f"Clue file not found: {clue_file}")
    # Try to find where clues are
    import glob
    for f in glob.glob("experiments/runs/**/*.codeclue", recursive=True):
        print(f"Found: {f}")
