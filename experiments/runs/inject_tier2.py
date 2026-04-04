"""Inject Tier 2 semantic contracts into the Flask graph."""
import json
import yaml
from pathlib import Path

graph_path = Path("experiments/runs/v2-lane-a-flask/graph.json")
graph = json.loads(graph_path.read_text())
contracts_dir = Path("experiments/runs/tier2-flask")

if not contracts_dir.exists():
    print(f"ERROR: {contracts_dir} does not exist. Run Tier 2 generation first.")
    exit(1)

contract_files = list(contracts_dir.glob("*.contracts.yaml"))
print(f"Found {len(contract_files)} contract files in {contracts_dir}")

injected = 0
skipped = 0

for node in graph["nodes"]:
    file_path = node["source_anchor"]["file_path"]
    symbol = node["semantic_contract"].get("symbol_name", "")
    node_type = node["semantic_contract"].get("symbol_type", "")

    # Only inject into function/method nodes
    if node_type not in ("function", "async_function", "method", "class"):
        continue

    # Find matching contract file
    filename = Path(file_path).name
    contract_file = contracts_dir / f"{filename}.contracts.yaml"

    if not contract_file.exists():
        skipped += 1
        continue

    try:
        contracts = yaml.safe_load(contract_file.read_text())
    except Exception as e:
        print(f"  WARNING: Failed to parse {contract_file}: {e}")
        continue

    if not isinstance(contracts, dict):
        continue

    # Try exact match, then case-insensitive match
    matched_contract = None
    for func_name, contract in contracts.items():
        if func_name == symbol:
            matched_contract = contract
            break
        if func_name.lower() == symbol.lower():
            matched_contract = contract
            break
        # Try ClassName.method format
        if "." in func_name and func_name.split(".")[-1].lower() == symbol.lower():
            matched_contract = contract
            break

    if matched_contract is None:
        skipped += 1
        continue

    # Inject Tier 2 fields
    sc = node["semantic_contract"]
    if "preconditions" in matched_contract:
        sc["preconditions"] = matched_contract["preconditions"]
    if "postconditions" in matched_contract:
        sc["postconditions"] = matched_contract["postconditions"]
    if "failure_modes" in matched_contract:
        sc["failure_modes"] = matched_contract["failure_modes"]
    if "complexity_indicators" in matched_contract:
        existing = sc.get("complexity_indicators", {})
        existing.update(matched_contract["complexity_indicators"])
        sc["complexity_indicators"] = existing
    sc["tier"] = 2
    injected += 1

# Save enriched graph
out = Path("experiments/runs/v2-lane-a-flask/graph-tier2.json")
out.write_text(json.dumps(graph, indent=2, sort_keys=True))
print(f"\nInjected Tier 2 contracts into {injected} nodes (skipped {skipped}).")
print(f"Saved to {out}")
