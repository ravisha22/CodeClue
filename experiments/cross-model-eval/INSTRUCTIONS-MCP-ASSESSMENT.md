# Instructions for Independent MCP Server Assessment
# Use this file with ANY LLM in a Copilot tab with this workspace open.
# Say: "Read experiments/cross-model-eval/INSTRUCTIONS-MCP-ASSESSMENT.md and follow all instructions."

## Your Role

You are an INDEPENDENT TESTER of the CodeClue MCP server. You did not build it.
Your job is to:
1. Verify all 5 tools work correctly on real data.
2. Test edge cases the original developer may have missed.
3. Assess whether the tools produce useful output for code comprehension tasks.
4. Run the existing test suite and report results.
5. Attempt adversarial inputs to find bugs.

## Step 1: Run the Existing Test Suite

Run this command in the terminal:
```bash
.\.venv\Scripts\python.exe -m pytest tests/mcp/ --tb=short -v
```

Record the output. Report:
- Total tests passed/failed/skipped
- Any failures with the error message

Save to: `experiments/cross-model-eval/results/mcp-assessment-test-suite.json`
```json
{
  "model": "<your model name>",
  "timestamp": "ISO 8601",
  "test_suite_results": {
    "total": 0, "passed": 0, "failed": 0, "skipped": 0,
    "failures": []
  }
}
```

## Step 2: Manual Tool Testing on Flask

Use the MCP server programmatically. Run each tool and assess the output quality.

### 2a: code_slice

Run in terminal:
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_mcp.tools import code_slice
import json

# Test 1: Fetch a known Flask function
r = code_slice(repo_root='experiments/external-repos/flask', file_path='src/flask/app.py', start_line=966, end_line=990)
print(json.dumps(r, indent=2))
"
```

Assess:
- Does it return the `dispatch_request` function?
- Are line numbers correct?
- Is content readable?

### 2b: resolve_dependency

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.tools import resolve_dependency
from pathlib import Path
import json

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
# Find a function node
func = [n for n in g.nodes if n.node_type == 'function' and 'dispatch' in n.node_id][0]
print(f'Seed: {func.node_id}')
r = resolve_dependency(graph=g, node_id=func.node_id, depth=2)
print(f'Nodes: {len(r[\"nodes\"])}, Edges: {len(r[\"edges\"])}')
print(json.dumps(r, indent=2)[:2000])
"
```

Assess:
- Does it expand to related functions?
- Are the edges meaningful (calls, contains)?
- Does depth=2 return more than depth=1?

### 2c: check_freshness

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.tools import check_freshness
from pathlib import Path
import json

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
module = [n for n in g.nodes if n.node_type == 'module' and 'app.py' in n.node_id][0]
r = check_freshness(graph=g, repo_root='experiments/external-repos/flask', module_id=module.node_id)
print(json.dumps(r, indent=2))
"
```

Assess:
- Does it correctly report stale/fresh?
- Does the hash comparison work?

### 2d: expand_projection

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.tools import expand_projection
from pathlib import Path
import json

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
module = [n for n in g.nodes if n.node_type == 'module' and 'app.py' in n.node_id][0]
r1 = expand_projection(graph=g, node_id=module.node_id, additional_hops=0, edge_types=['contains'])
r2 = expand_projection(graph=g, node_id=module.node_id, additional_hops=1, edge_types=['contains'])
print(f'0 hops: {len(r1[\"projected_nodes\"])} nodes')
print(f'1 hop:  {len(r2[\"projected_nodes\"])} nodes')
assert len(r2['projected_nodes']) > len(r1['projected_nodes']), 'FAIL: 1 hop should have more nodes'
print('PASS: expansion works')
"
```

### 2e: fetch_contract

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.tools import fetch_contract
from pathlib import Path
import json

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
func = [n for n in g.nodes if n.node_type == 'function'][0]
r = fetch_contract(graph=g, node_id=func.node_id)
print(json.dumps(r, indent=2))
# Check Tier 1 fields present
sc = r['semantic_contract']
for field in ['purpose', 'language', 'symbol_name', 'symbol_type', 'tier']:
    assert field in sc, f'MISSING: {field}'
print('All Tier 1 fields present')
"
```

## Step 3: Adversarial Testing

Try to break the tools. For EACH test, record whether the tool handled it gracefully or crashed.

### 3a: Path traversal
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_mcp.tools import code_slice
r = code_slice(repo_root='experiments/external-repos/flask', file_path='../../../etc/passwd', start_line=1, end_line=5)
print(r)  # Should return status=error, NOT file contents
"
```

### 3b: Nonexistent node
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.tools import resolve_dependency, fetch_contract, expand_projection
from pathlib import Path

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
for tool_name, tool_fn, args in [
    ('resolve_dependency', resolve_dependency, {'graph': g, 'node_id': 'FAKE_NODE', 'depth': 1}),
    ('fetch_contract', fetch_contract, {'graph': g, 'node_id': 'FAKE_NODE'}),
    ('expand_projection', expand_projection, {'graph': g, 'node_id': 'FAKE_NODE', 'additional_hops': 1}),
]:
    r = tool_fn(**args)
    assert r['status'] == 'error', f'{tool_name} should return error for fake node'
    print(f'{tool_name}: correctly returns error')
"
```

### 3c: Extreme line ranges
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_mcp.tools import code_slice
r = code_slice(repo_root='experiments/external-repos/flask', file_path='src/flask/app.py', start_line=-100, end_line=999999)
print(f'Status: {r[\"status\"]}, Lines returned: {len(r.get(\"lines\",[]))}')
# Should not crash, should return available lines
"
```

### 3d: Empty file
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_mcp.tools import code_slice
r = code_slice(repo_root='experiments/external-repos/flask', file_path='src/flask/__init__.py', start_line=1, end_line=5)
print(f'Status: {r[\"status\"]}, Lines: {len(r.get(\"lines\",[]))}')
"
```

### 3e: Budget tracker exhaustion
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_mcp.budget import BudgetTracker
t = BudgetTracker(operation_family='OF1')
for i in range(10):
    if t.can_call():
        t.record_call(tool='code_slice', node_id=f'n{i}')
        print(f'Call {i+1}: allowed, remaining={t.remaining()}')
    else:
        t.register_unresolved([f'n{j}' for j in range(i, 10)])
        esc = t.get_escalation()
        print(f'Call {i+1}: BLOCKED. Escalation: {esc}')
        break
"
```

## Step 4: Cross-Repo Smoke Test

Test tools on a NON-Flask repo to verify multi-language support:

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.server import CodeClueServer
from pathlib import Path
import json

# Test on Gin (Go)
g = load_graph(Path('experiments/runs/v2-lane-a-gin/graph.json'))
server = CodeClueServer(graph=g, repo_root='experiments/external-repos/gin')

tools = server.list_tools()
print(f'Tools: {len(tools)}')

# code_slice on Go file
r = server.call_tool('code_slice', {'file_path': 'gin.go', 'start_line': 1, 'end_line': 10})
print(f'Go code_slice: {r[\"status\"]}, lines={len(r.get(\"lines\",[]))}')

# fetch_contract on Go node
node = g.nodes[5]
r = server.call_tool('fetch_contract', {'node_id': node.node_id})
print(f'Go fetch_contract: {r[\"status\"]}, type={r.get(\"node_type\",\"?\")}')
print(f'Contract keys: {list(r.get(\"semantic_contract\",{}).keys())}')
"
```

Also test on TypeScript (NestJS):
```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_mcp.server import CodeClueServer
from pathlib import Path

g = load_graph(Path('experiments/runs/v2-lane-a-nest/graph.json'))
server = CodeClueServer(graph=g, repo_root='experiments/external-repos/nest')
node = [n for n in g.nodes if n.node_type == 'function'][0]
r = server.call_tool('resolve_dependency', {'node_id': node.node_id, 'depth': 1})
print(f'TS resolve_dependency: status={r[\"status\"]}, nodes={len(r[\"nodes\"])}')
"
```

## Step 5: End-to-End Drill-Down Assessment

Simulate the actual use case: read a projection, find a low-confidence node, drill down.

```bash
.\.venv\Scripts\python.exe -c "
from codeclue_research.io import load_graph
from codeclue_research.operation_projection import project_operation
from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.tracer import InvocationTracer, hash_output
from pathlib import Path
import json

g = load_graph(Path('experiments/runs/v2-lane-a-flask/graph.json'))
server = CodeClueServer(graph=g, repo_root='experiments/external-repos/flask')
tracer = InvocationTracer(trace_dir=Path('experiments/cross-model-eval/results/mcp-traces'))

# Project OF4 (debugging) on Flask
trace = project_operation(graph=g, operation_family='OF4',
    prompt_profile={'profile_id': 'mcp-test', 'intent': 'debugging',
        'constraints': {'max_context': 'focused'},
        'focus_files': ['src/flask/app.py'],
        'focus_symbols': ['do_teardown_request']})

conf = trace.get('confidence', {})
print(f'Projection: {trace[\"stats\"][\"projected_node_count\"]} nodes, conf={conf.get(\"confidence_overall\")}')

# Find nodes with suggested actions
actions_found = 0
for nc in conf.get('per_node_confidence', []):
    for action in nc.get('suggested_actions', []):
        result = server.call_tool(action['tool'], action.get('args', {}))
        tracer.log(tool=action['tool'], args=action.get('args', {}),
            output_hash=hash_output(result), source_anchor=nc['node_id'],
            confidence_trigger=nc['confidence'], session_id='mcp-assessment')
        actions_found += 1
        if actions_found >= 3:
            break
    if actions_found >= 3:
        break

print(f'Drill-down actions executed: {actions_found}')
print(f'Trace file: {tracer.trace_path}')

# Verify trace
lines = tracer.trace_path.read_text().strip().split(chr(10))
print(f'Trace entries: {len(lines)}')
for line in lines:
    entry = json.loads(line)
    print(f'  {entry[\"tool\"]}: conf_trigger={entry[\"confidence_trigger\"]}')
"
```

## Step 6: Write Assessment Report

Save your complete assessment to:
`experiments/cross-model-eval/results/mcp-assessment-report.json`

```json
{
  "assessor_model": "<your model name>",
  "timestamp": "ISO 8601",
  "test_suite": {
    "passed": 0, "failed": 0, "skipped": 0, "verdict": "PASS/FAIL"
  },
  "manual_testing": {
    "code_slice": {"works": true, "notes": ""},
    "resolve_dependency": {"works": true, "notes": ""},
    "check_freshness": {"works": true, "notes": ""},
    "expand_projection": {"works": true, "notes": ""},
    "fetch_contract": {"works": true, "notes": ""}
  },
  "adversarial_testing": {
    "path_traversal_blocked": true,
    "nonexistent_node_handled": true,
    "extreme_ranges_handled": true,
    "empty_file_handled": true,
    "budget_exhaustion_works": true,
    "bugs_found": []
  },
  "cross_repo": {
    "go_works": true,
    "typescript_works": true,
    "python_works": true
  },
  "e2e_drill_down": {
    "projection_works": true,
    "suggested_actions_found": true,
    "tools_executed_successfully": true,
    "trace_logging_works": true
  },
  "overall_verdict": "PASS/FAIL",
  "quality_score": 0,
  "bugs_found": [],
  "improvement_suggestions": [],
  "summary": "2-3 sentence overall assessment"
}
```

Write a completion marker:
`experiments/cross-model-eval/results/mcp-assessment-COMPLETE.json`
```json
{"model": "<name>", "timestamp": "ISO 8601", "status": "complete", "verdict": "PASS/FAIL"}
```
