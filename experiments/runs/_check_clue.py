from pathlib import Path

clue = Path("experiments/runs/mrlf-benchmark/flask-tf1-refactor-sessions.codeclue").read_text()

in_sym = False
count = 0
for line in clue.split("\n"):
    if line.strip() == "-- SYM":
        in_sym = True
        continue
    if line.startswith("-- ") and in_sym:
        break
    if in_sym and line.strip() and not line.startswith("  ..."):
        count += 1
        if count <= 15:
            print(line[:100])

print(f"\nTotal SYM lines: {count}")
print(f"SessionInterface found: {'SessionInterface' in clue}")
print(f"SecureCookieSession found: {'SecureCookieSession' in clue}")
print(f"wsgi_app found: {'wsgi_app' in clue}")
print(f"dispatch_request found: {'dispatch_request' in clue}")
print(f"Blueprint found: {'Blueprint' in clue}")
print(f"NullSession found: {'NullSession' in clue}")

# Count test lines
test_lines = sum(1 for line in clue.split("\n") if "test" in line.lower() and "-- " not in line)
print(f"Lines mentioning 'test': {test_lines}")
