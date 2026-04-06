"""Judge module: scoring consumer answers against gold-path specs.

Mode A: Gold-path heuristic — fully automated, deterministic.
Mode B: LLM judge — structured rubric, requires API call.
"""

from __future__ import annotations

import re
from typing import Any


def _normalize(text: str) -> str:
    """Normalize text for fuzzy matching."""
    return re.sub(r"\s+", " ", text.lower().strip())


def _extract_cited_symbols(answer_text: str) -> set[str]:
    """Extract symbol names cited in the answer text."""
    # Match patterns like Flask.wsgi_app, dispatch_request, n1, n2, etc.
    symbols: set[str] = set()
    # Dotted names
    for m in re.finditer(r"\b([A-Z]\w+\.\w+(?:\.\w+)*)\b", answer_text):
        symbols.add(m.group(1).lower())
    # Short IDs like n1, n2
    for m in re.finditer(r"\bn(\d+)\b", answer_text):
        symbols.add(f"n{m.group(1)}")
    # Snake case function names
    for m in re.finditer(r"\b([a-z_]\w*_\w+)\b", answer_text):
        symbols.add(m.group(1).lower())
    return symbols


def score_heuristic(
    answer_text: str,
    gold_spec: dict[str, Any],
    clue: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Score a consumer answer against a gold-path spec using heuristic matching.

    Args:
        answer_text: The consumer model's answer (plain text).
        gold_spec: Gold path spec with expected nodes/edges.
        clue: Optional clue artifact for context.

    Returns:
        Scoring result with metrics and sufficiency verdict.
    """
    # Extract gold path info
    gold_path = gold_spec.get("gold_path", {})
    expected_nodes = set(gold_path.get("nodes", []))
    expected_edges = set(gold_path.get("edges", []))

    # Extract what the answer mentions
    cited = _extract_cited_symbols(answer_text)
    normalized_answer = _normalize(answer_text)

    # Node recall: how many expected nodes are mentioned in the answer
    node_hits = 0
    for node_id in expected_nodes:
        # Extract the symbol name from the node_id
        parts = node_id.split(":")
        if len(parts) >= 3:
            symbol = parts[2]  # e.g., "Flask.wsgi_app" from "symbol:src/flask/app.py:Flask.wsgi_app:1566"
            if symbol.lower() in normalized_answer or symbol.lower() in cited:
                node_hits += 1
        elif node_id.lower() in normalized_answer:
            node_hits += 1

    node_recall = node_hits / len(expected_nodes) if expected_nodes else 1.0

    # Edge recall: how many expected relationships are implied in the answer
    edge_hits = 0
    for edge_id in expected_edges:
        parts = edge_id.split(":")
        if len(parts) >= 4:
            # Extract from and to symbols
            from_sym = parts[1].split(":")[-1] if ":" in parts[1] else ""
            to_sym = parts[2].split(":")[-1] if ":" in parts[2] else ""
            # Check if both endpoints mentioned
            if from_sym and to_sym:
                from_found = from_sym.lower() in normalized_answer
                to_found = to_sym.lower() in normalized_answer
                if from_found and to_found:
                    edge_hits += 1

    edge_recall = edge_hits / len(expected_edges) if expected_edges else 1.0

    # Path fidelity (combined metric)
    path_fidelity = (node_recall + edge_recall) / 2.0

    # Evidence quality: penalize very short or very vague answers
    word_count = len(answer_text.split())
    evidence_quality = min(1.0, word_count / 50)  # Expect at least 50 words

    # Thresholds
    thresholds = gold_spec.get("thresholds", {})
    fidelity_min = float(thresholds.get("path_fidelity_min", 0.80))

    sufficient = path_fidelity >= fidelity_min

    return {
        "mode": "heuristic",
        "node_recall": round(node_recall, 4),
        "edge_recall": round(edge_recall, 4),
        "path_fidelity": round(path_fidelity, 4),
        "evidence_quality": round(evidence_quality, 4),
        "sufficient": sufficient,
        "threshold": fidelity_min,
        "node_hits": node_hits,
        "node_expected": len(expected_nodes),
        "edge_hits": edge_hits,
        "edge_expected": len(expected_edges),
        "word_count": word_count,
    }


def build_judge_prompt(
    question: str,
    gold_truth: str,
    consumer_answer: str,
    clue_artifact: dict[str, Any] | None = None,
) -> str:
    """Build a structured judge prompt for LLM-based scoring.

    Args:
        question: The task question.
        gold_truth: Gold-standard answer summary.
        consumer_answer: The consumer model's answer.
        clue_artifact: Optional clue artifact for context.

    Returns:
        Formatted judge prompt string.
    """
    prompt = f"""You are an independent judge scoring a code comprehension answer.

## Task Question
{question}

## Gold-Standard Answer
{gold_truth}

## Consumer's Answer
{consumer_answer}

## Scoring Rubric (score each 0.0 to 1.0)

1. **Accuracy** [weight: 0.4]: Are the factual claims correct? Does the answer correctly identify the right code elements and their behavior?

2. **Completeness** [weight: 0.3]: Does the answer cover all the key elements in the gold standard? Are important aspects missing?

3. **Groundedness** [weight: 0.2]: Are claims traceable to the clue content provided? Does the answer avoid unsupported speculation?

4. **Specificity** [weight: 0.1]: Does the answer cite specific symbols, files, or code elements rather than giving vague generalities?

## Required Output Format (JSON only)
{{
  "accuracy": <float 0-1>,
  "completeness": <float 0-1>,
  "groundedness": <float 0-1>,
  "specificity": <float 0-1>,
  "overall": <weighted average>,
  "sufficient": <true if overall >= 0.60>,
  "reasoning": "<one sentence justification>"
}}
"""
    return prompt


def parse_judge_response(response_text: str) -> dict[str, Any]:
    """Parse JSON from a judge model's response.

    Returns:
        Parsed scoring dict, or a fallback error dict.
    """
    import json

    # Try to extract JSON from the response
    # Look for JSON block
    json_match = re.search(r"\{[^{}]*\}", response_text, re.DOTALL)
    if json_match:
        try:
            result = json.loads(json_match.group())
            # Compute overall if not present
            if "overall" not in result:
                result["overall"] = (
                    result.get("accuracy", 0) * 0.4
                    + result.get("completeness", 0) * 0.3
                    + result.get("groundedness", 0) * 0.2
                    + result.get("specificity", 0) * 0.1
                )
            result["mode"] = "llm_judge"
            result.setdefault("sufficient", result.get("overall", 0) >= 0.60)
            return result
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "mode": "llm_judge",
        "accuracy": 0.0,
        "completeness": 0.0,
        "groundedness": 0.0,
        "specificity": 0.0,
        "overall": 0.0,
        "sufficient": False,
        "reasoning": "Failed to parse judge response",
        "parse_error": True,
    }
