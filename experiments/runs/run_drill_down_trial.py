"""End-to-end drill-down trial: measure H5 and H7.

H5: On tasks where confidence < 0.85, does drill-down raise fidelity by >= 0.10?
H7: Does ETRR (effective TRR including drill-down tokens) remain >= 0.65?

Uses self-as-consumer: project a low-confidence task, execute suggested tool actions,
read the tool outputs, and re-assess what the improved answer would be.
"""
import json
from pathlib import Path
from codeclue_research.io import load_graph
from codeclue_research.operation_projection import project_operation
from codeclue_mcp.server import CodeClueServer
from codeclue_mcp.tracer import InvocationTracer, hash_output
from codeclue_mcp.budget import BudgetTracker


def run_drill_down_trial(
    graph_path: str,
    repo_root: str,
    operation_family: str,
    prompt_profile: dict,
    task_question: str,
    ground_truth: str,
    output_dir: str,
) -> dict:
    graph = load_graph(Path(graph_path))
    server = CodeClueServer(graph=graph, repo_root=repo_root)
    tracer = InvocationTracer(trace_dir=Path(output_dir) / "traces")
    tracker = BudgetTracker(operation_family=operation_family)

    # Step 1: Project
    trace = project_operation(graph=graph, operation_family=operation_family, prompt_profile=prompt_profile)
    conf = trace.get("confidence", {})
    conf_overall = conf.get("confidence_overall", 0)
    hint = conf.get("lookup_decision_hint", "unknown")

    # Step 2: Count clue tokens (approximate)
    clue_token_estimate = len(json.dumps(trace.get("projected_nodes", []))) // 4

    # Step 3: Execute suggested drill-down actions
    drill_down_results = []
    drill_down_tokens = 0
    actions_executed = 0

    for nc in conf.get("per_node_confidence", []):
        if not tracker.can_call():
            break
        for action in nc.get("suggested_actions", []):
            if not tracker.can_call():
                break
            result = server.call_tool(action["tool"], action.get("args", {}))
            if result.get("status") == "ok":
                tracker.record_call(tool=action["tool"], node_id=nc["node_id"])
                tracer.log(
                    tool=action["tool"], args=action.get("args", {}),
                    output_hash=hash_output(result),
                    source_anchor=nc["node_id"],
                    confidence_trigger=nc.get("confidence", 0),
                    session_id="drill-down-trial",
                )
                result_str = json.dumps(result)
                drill_down_tokens += len(result_str) // 4
                actions_executed += 1
                drill_down_results.append({
                    "tool": action["tool"],
                    "node_id": nc["node_id"],
                    "confidence_trigger": nc.get("confidence", 0),
                    "output_size_tokens": len(result_str) // 4,
                })

    # Step 4: Compute metrics
    # Raw token estimate (sum of source file sizes for relevant files)
    raw_token_estimate = 0
    seen_files = set()
    for node in graph.nodes:
        fp = node.source_anchor.file_path
        if fp not in seen_files:
            seen_files.add(fp)
            full_path = Path(repo_root) / fp
            if full_path.exists():
                raw_token_estimate += full_path.stat().st_size // 4

    total_clue_plus_drill = clue_token_estimate + drill_down_tokens
    etrr = 1.0 - (total_clue_plus_drill / max(raw_token_estimate, 1))

    escalation = tracker.get_escalation()

    trial_result = {
        "task_question": task_question,
        "operation_family": operation_family,
        "confidence_overall": conf_overall,
        "lookup_hint": hint,
        "projected_nodes": trace["stats"]["projected_node_count"],
        "actions_executed": actions_executed,
        "budget_exhausted": escalation["budget_exhausted"],
        "tokens": {
            "clue": clue_token_estimate,
            "drill_down": drill_down_tokens,
            "total": total_clue_plus_drill,
            "raw_estimate": raw_token_estimate,
        },
        "etrr": round(etrr, 4),
        "h7_pass": etrr >= 0.65,
        "drill_down_actions": drill_down_results,
        "escalation": escalation,
    }

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(output_dir, "drill-down-trial.json").write_text(json.dumps(trial_result, indent=2))
    return trial_result


if __name__ == "__main__":
    # Run on Flask OF2 (worst family, most need for drill-down)
    result = run_drill_down_trial(
        graph_path="experiments/runs/v2-lane-a-flask/graph.json",
        repo_root="experiments/external-repos/flask",
        operation_family="OF2",
        prompt_profile={
            "profile_id": "drill-down-trial",
            "intent": "impact-analysis",
            "constraints": {"max_context": "focused"},
            "focus_files": ["src/flask/ctx.py"],
            "focus_symbols": ["push", "RequestContext"],
            "focus_keywords": ["push", "context"],
        },
        task_question="If I change the push method in RequestContext to be async, what components would be impacted?",
        ground_truth="RequestContext.push() is called by wsgi_app, __enter__, test_request_context. Making it async requires wsgi_app, full_dispatch_request, before/after_request handlers, and testing client to be async-compatible.",
        output_dir="experiments/reports/drill-down-trial",
    )

    print(f"Confidence: {result['confidence_overall']}")
    print(f"Actions executed: {result['actions_executed']}")
    print(f"Tokens — clue: {result['tokens']['clue']}, drill-down: {result['tokens']['drill_down']}, raw: {result['tokens']['raw_estimate']}")
    print(f"ETRR: {result['etrr']} (H7 pass: {result['h7_pass']})")
    print(f"Budget exhausted: {result['budget_exhausted']}")

    # Also run on Flask OF5 (security)
    result2 = run_drill_down_trial(
        graph_path="experiments/runs/v2-lane-a-flask/graph.json",
        repo_root="experiments/external-repos/flask",
        operation_family="OF5",
        prompt_profile={
            "profile_id": "drill-down-trial-sec",
            "intent": "security-compliance",
            "constraints": {"max_context": "balanced"},
            "focus_files": ["src/flask/sessions.py"],
            "focus_symbols": ["SecureCookieSessionInterface"],
            "focus_keywords": ["session", "secret", "cookie"],
        },
        task_question="How does Flask handle session security?",
        ground_truth="Sessions signed with itsdangerous using secret_key. HMAC-SHA1. Not encrypted, only signed. httponly, secure, samesite configurable.",
        output_dir="experiments/reports/drill-down-trial-sec",
    )

    print(f"\nSecurity trial:")
    print(f"Confidence: {result2['confidence_overall']}")
    print(f"Actions: {result2['actions_executed']}")
    print(f"ETRR: {result2['etrr']} (H7 pass: {result2['h7_pass']})")
