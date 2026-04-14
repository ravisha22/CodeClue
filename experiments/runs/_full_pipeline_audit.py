"""COMPREHENSIVE EXTRACTION PIPELINE AUDIT

Systematically tests what the extractor captures and misses across
all call patterns, knowledge types, and repo sizes.
"""
import ast
import json
from pathlib import Path
from codeclue_research.extractor import extract_graph, SymbolCollector
from codeclue_research.clue_view_mrlf import render_mrlf, _token_count, _select_focus_nodes

def audit_call_edge_patterns():
    """Test every Python call pattern against the extractor."""
    test_code = '''
class MyClass:
    def method_a(self):
        self.method_b()           # Pattern 1: self.method()
        self._private()           # Pattern 2: self._private()
        result = self.compute()   # Pattern 3: self.method() in assignment

    def method_b(self):
        pass

    def _private(self):
        pass

    def compute(self):
        return helper_func()      # Pattern 4: module-level call

    def uses_super(self):
        super().method_b()        # Pattern 5: super().method()

def helper_func():
    obj = MyClass()               # Pattern 6: class instantiation
    obj.method_a()                # Pattern 7: instance.method()
    return obj

class Child(MyClass):
    def method_a(self):
        super().method_a()        # Pattern 8: super in child
        self.child_only()         # Pattern 9: child self-call

    def child_only(self):
        pass
'''
    collector = SymbolCollector("test.py")
    tree = ast.parse(test_code, "test.py")
    collector.visit(tree)
    
    # Check what symbols were found
    print("=== CALL EDGE PATTERN AUDIT ===\n")
    print("Symbols extracted:")
    for sym in collector.symbols:
        print(f"  {sym.symbol_name} ({sym.symbol_type})")
    
    # Now run full extraction to get edges
    # We need to simulate what extract_python_nodes_edges does
    from codeclue_research.extractor import extract_python_nodes_edges
    import tempfile, os
    
    # Write test code to temp dir
    tmpdir = Path(tempfile.mkdtemp())
    test_file = tmpdir / "test.py"
    test_file.write_text(test_code)
    
    nodes, edges = extract_python_nodes_edges(tmpdir)
    
    call_edges = [(e.from_node, e.to_node) for e in edges if e.edge_type == "calls"]
    print(f"\nCall edges found: {len(call_edges)}")
    for fr, to in call_edges:
        fr_short = fr.split(":")[-2] if ":" in fr else fr
        to_short = to.split(":")[-2] if ":" in to else to
        print(f"  {fr_short} -> {to_short}")
    
    # Check which patterns are captured
    patterns = {
        "self.method()": False,
        "self._private()": False,
        "self.method() in assign": False,
        "module-level call": False,
        "super().method()": False,
        "class instantiation": False,
        "instance.method()": False,
    }
    
    for fr, to in call_edges:
        if "method_a" in fr and "method_b" in to: patterns["self.method()"] = True
        if "method_a" in fr and "_private" in to: patterns["self._private()"] = True
        if "method_a" in fr and "compute" in to: patterns["self.method() in assign"] = True
        if "compute" in fr and "helper_func" in to: patterns["module-level call"] = True
        if "helper_func" in fr and "MyClass" in to: patterns["class instantiation"] = True
    
    print(f"\n--- Pattern Coverage ---")
    for pattern, found in patterns.items():
        status = "CAPTURED" if found else "MISSED"
        print(f"  [{status:8s}] {pattern}")
    
    # Cleanup
    test_file.unlink()
    tmpdir.rmdir()
    return patterns


def audit_blind_clue_coverage():
    """For each blind task, check what gold symbols ARE vs AREN'T in the clue."""
    print("\n\n=== BLIND CLUE CONTENT vs GOLD FACTS AUDIT ===\n")
    
    gold_path = Path("experiments/runs/blind-eval/blind-gold-tasks.json")
    if not gold_path.exists():
        print("No blind gold tasks found")
        return
    
    golds = json.loads(gold_path.read_text(encoding="utf-8"))
    
    for gold in golds:
        task_id = gold["task_id"]
        clue_path = Path(f"experiments/runs/blind-eval/clues/{task_id}.codeclue")
        if not clue_path.exists():
            print(f"  {task_id}: NO CLUE FILE")
            continue
        
        clue = clue_path.read_text(encoding="utf-8")
        
        print(f"--- {task_id} ({gold['repo']}) ---")
        
        # Check gold symbols
        for gs in gold.get("gold_symbols", []):
            short = gs.rsplit(".", 1)[-1]
            in_sym = short in clue and "-- SYM" in clue  # rough check
            in_focus = False
            for line in clue.split("\n"):
                if line.strip().startswith(short + " (") or line.strip().startswith(short + " "):
                    # Check if it's in FOCUS section
                    idx = clue.index(line)
                    focus_start = clue.find("-- FOCUS")
                    gaps_start = clue.find("-- GAPS")
                    if focus_start < idx < gaps_start:
                        in_focus = True
                        break
            
            loc = "FOCUS" if in_focus else ("SYM" if short.lower() in clue.lower() else "ABSENT")
            print(f"  [{loc:6s}] {gs}")
        
        # Check gold facts - what keywords from each fact appear
        for i, fact in enumerate(gold.get("gold_facts", []), 1):
            # Extract key identifiers from fact (CamelCase and snake_case)
            import re
            identifiers = set(re.findall(r'[A-Z][a-zA-Z]+|[a-z_]{4,}', fact))
            found = sum(1 for ident in identifiers if ident.lower() in clue.lower())
            total = len(identifiers)
            pct = found / total * 100 if total else 0
            print(f"  FACT {i}: {found}/{total} identifiers in clue ({pct:.0f}%) - {fact[:70]}...")
        
        print()


def audit_focus_quality():
    """Check what FOCUS entries look like - do they have calls? docstrings? useful info?"""
    print("\n=== FOCUS ENTRY QUALITY AUDIT ===\n")
    
    clue_dir = Path("experiments/runs/blind-eval/clues")
    for clue_path in sorted(clue_dir.glob("*.codeclue")):
        clue = clue_path.read_text(encoding="utf-8")
        
        # Parse FOCUS entries
        in_focus = False
        entries = []
        current = []
        for line in clue.split("\n"):
            if "-- FOCUS" in line:
                in_focus = True
                continue
            if "-- GAPS" in line:
                if current:
                    entries.append(current)
                in_focus = False
                continue
            if not in_focus:
                continue
            if line and not line.startswith("  "):
                if current:
                    entries.append(current)
                current = [line]
            elif line.startswith("  ") and current:
                current.append(line)
        
        # Analyze entry quality
        has_calls = sum(1 for e in entries if any("calls:" in l for l in e))
        has_docstring = sum(1 for e in entries if len(e) > 1 and not e[1].strip().startswith(("sig:", "extends:", "imports:", "attrs:", "calls:", "called_by:", "raises:", "uses:", "methods:")))
        has_sig = sum(1 for e in entries if any("sig:" in l for l in e))
        has_uses = sum(1 for e in entries if any("uses:" in l for l in e))
        has_raises = sum(1 for e in entries if any("raises:" in l for l in e))
        total = len(entries)
        
        print(f"{clue_path.name}: {total} entries")
        print(f"  calls:     {has_calls}/{total} ({has_calls/total*100:.0f}%)")
        print(f"  docstring: {has_docstring}/{total} ({has_docstring/total*100:.0f}%)")
        print(f"  sig:       {has_sig}/{total} ({has_sig/total*100:.0f}%)")
        print(f"  uses:      {has_uses}/{total} ({has_uses/total*100:.0f}%)")
        print(f"  raises:    {has_raises}/{total} ({has_raises/total*100:.0f}%)")
        print()


if __name__ == "__main__":
    patterns = audit_call_edge_patterns()
    audit_blind_clue_coverage()
    audit_focus_quality()
    
    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE AUDIT SUMMARY")
    print("=" * 70)
    missed = [p for p, v in patterns.items() if not v]
    print(f"\nCall patterns MISSED: {len(missed)}/{len(patterns)}")
    for m in missed:
        print(f"  - {m}")
    print(f"\nThese missing patterns break the call graph for any method-heavy")
    print(f"codebase. self.method() is the PRIMARY call pattern in Python OOP.")
