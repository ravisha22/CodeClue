"""Diagnostic: Check what the extractor produces for Flask session classes."""
from codeclue_research.extractor import SymbolCollector
import ast

flask_sessions = "experiments/external-repos/flask/src/flask/sessions.py"
with open(flask_sessions) as f:
    source = f.read()

ext = SymbolCollector(flask_sessions)
tree = ast.parse(source, flask_sessions)
ext.visit(tree)
for sym in ext.symbols:
    if "Session" in sym.symbol_name:
        print(f"NAME: {sym.symbol_name}")
        print(f"  type={sym.symbol_type}")
        print(f"  raises={sym.raises}")
        print(f"  sig={sym.signature}")
        doc_preview = (sym.docstring or "")[:80]
        print(f"  doc={doc_preview}")
        print()
