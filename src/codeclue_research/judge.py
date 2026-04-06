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
    """Score a consumer answer using content-quality heuristics.

    Evaluates answer richness against the clue artifact itself:
    - Symbol coverage: how many clue symbols are cited in the answer
    - Behavioral coverage: whether behavioral risks/invariants are mentioned
    - Structural coverage: whether relationships/flows are described
    - Evidence quality: answer length and specificity

    Args:
        answer_text: The consumer model's answer (plain text).
        gold_spec: Gold path spec (used for thresholds only).
        clue: The clue artifact for symbol/behavior matching.

    Returns:
        Scoring result with metrics and sufficiency verdict.
    """
    normalized = _normalize(answer_text)
    cited = _extract_cited_symbols(answer_text)

    # Extract symbols and behaviors from the clue
    clue_symbols: list[str] = []
    clue_risks: list[str] = []
    clue_behaviors: list[str] = []
    clue_relations: int = 0

    if clue:
        # Plan A entities
        for entity in clue.get("entities", []):
            name = entity.get("name", "")
            if name:
                clue_symbols.append(name)
            clue_risks.extend(entity.get("risks", []))
            behavior = entity.get("behavior", "")
            if behavior:
                clue_behaviors.append(behavior)
            clue_relations += len(entity.get("inflow", [])) + len(entity.get("outflow", []))

        # Plan B nodes
        for node in clue.get("nodes", []):
            name = node.get("name", "")
            if name:
                clue_symbols.append(name)
            clue_risks.extend(node.get("risks", []))
            summary = node.get("summary", "")
            if summary:
                clue_behaviors.append(summary)

        clue_relations += len(clue.get("relations", []))

    # Symbol coverage: how many clue symbols appear in the answer
    symbol_hits = 0
    for sym in clue_symbols:
        short = sym.rsplit(".", 1)[-1].lower() if "." in sym else sym.lower()
        if short in normalized or sym.lower() in normalized:
            symbol_hits += 1
    symbol_recall = symbol_hits / len(clue_symbols) if clue_symbols else 0.0

    # Risk/behavioral coverage
    risk_hits = 0
    for risk in clue_risks:
        risk_words = risk.lower().replace("_", " ")
        if any(w in normalized for w in risk_words.split()):
            risk_hits += 1
    risk_coverage = risk_hits / len(clue_risks) if clue_risks else 1.0  # no risks = full coverage

    # Behavioral coverage: how many behavior summaries are reflected
    behavior_hits = 0
    for beh in clue_behaviors:
        # Check if key words from behavior appear in answer
        key_words = [w for w in _normalize(beh).split() if len(w) > 4]
        if key_words and sum(1 for w in key_words if w in normalized) / len(key_words) > 0.3:
            behavior_hits += 1
    behavior_recall = behavior_hits / len(clue_behaviors) if clue_behaviors else 0.0

    # Evidence quality
    word_count = len(answer_text.split())
    length_score = min(1.0, word_count / 50)

    # Composite fidelity
    path_fidelity = (
        symbol_recall * 0.35
        + behavior_recall * 0.35
        + risk_coverage * 0.15
        + length_score * 0.15
    )

    # Threshold
    thresholds = gold_spec.get("thresholds", {})
    fidelity_min = float(thresholds.get("path_fidelity_min", 0.60))
    sufficient = path_fidelity >= fidelity_min

    return {
        "mode": "heuristic",
        "symbol_recall": round(symbol_recall, 4),
        "behavior_recall": round(behavior_recall, 4),
        "risk_coverage": round(risk_coverage, 4),
        "length_score": round(length_score, 4),
        "path_fidelity": round(path_fidelity, 4),
        "sufficient": sufficient,
        "threshold": fidelity_min,
        "symbol_hits": symbol_hits,
        "symbol_total": len(clue_symbols),
        "behavior_hits": behavior_hits,
        "behavior_total": len(clue_behaviors),
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
