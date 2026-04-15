"""Judge module: scoring consumer answers against gold-path specs.

Mode A: Gold-path heuristic — fully automated, deterministic.
Mode B: LLM judge — structured rubric, requires API call.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_STANDARD_SCORING_RUBRIC = """\
### Fact Labels
- **COVERED**: Response describes the specific mechanism or behavior from the gold fact and includes supporting evidence. Exact wording is not required, but the core behavior must be identified, not just the function or class name.
- **PARTIAL**: Response identifies the right function/class or hints at the behavior, but misses important mechanism detail. Upgrade PARTIAL to COVERED when more than 50% of the mechanism is captured.
- **MISS**: Response does not contain the information, gives the wrong behavior, or explicitly says it cannot determine the answer.

### Grounding Rules
- Judge only what is present in the answer.
- Do not award credit for external framework knowledge.
- Prefer mechanism-level evidence over symbol-name mentions.
- When in doubt between PARTIAL and MISS, use PARTIAL only if the answer points to the correct code element and some correct behavior.
"""


def load_standard_scoring_rubric() -> str:
    """Load the repository-wide scoring rubric used by evaluation prompts."""
    rubric_path = (
        Path(__file__).resolve().parents[2]
        / "experiments"
        / "runs"
        / "blind-eval"
        / "STANDARD-SCORING-RUBRIC.md"
    )
    try:
        return rubric_path.read_text(encoding="utf-8").strip()
    except OSError:
        return _STANDARD_SCORING_RUBRIC.strip()


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
    """Build a structured judge prompt for fact-level LLM scoring.

    Args:
        question: The task question.
        gold_truth: Gold-standard answer summary.
        consumer_answer: The consumer model's answer.
        clue_artifact: Optional clue artifact for context.

    Returns:
        Formatted judge prompt string.
    """
    rubric = load_standard_scoring_rubric()
    prompt = f"""You are an independent judge scoring a code comprehension answer.

## Task Question
{question}

## Gold-Standard Answer
{gold_truth}

## Consumer's Answer
{consumer_answer}

## Standard Scoring Rubric
{rubric}

## Required Output Format (JSON only)
{{
  "fact_verdicts": [
    {{
      "fact": "<gold fact>",
      "label": "COVERED" | "PARTIAL" | "MISS",
      "justification": "<cite the answer text that supports the label>"
    }}
  ],
  "covered": <int>,
  "partial": <int>,
  "missed": <int>,
  "score": <covered / total_facts as float>,
  "sufficient": <true if score >= 0.60>,
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
            verdicts = result.get("fact_verdicts", [])
            if verdicts and "score" not in result:
                covered = sum(1 for verdict in verdicts if verdict.get("label") == "COVERED")
                result["covered"] = covered
                result["partial"] = sum(1 for verdict in verdicts if verdict.get("label") == "PARTIAL")
                result["missed"] = sum(1 for verdict in verdicts if verdict.get("label") == "MISS")
                result["score"] = covered / len(verdicts)
            result["mode"] = "llm_judge"
            result.setdefault("sufficient", result.get("score", result.get("overall", 0)) >= 0.60)
            return result
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "mode": "llm_judge",
        "fact_verdicts": [],
        "covered": 0,
        "partial": 0,
        "missed": 0,
        "score": 0.0,
        "sufficient": False,
        "reasoning": "Failed to parse judge response",
        "parse_error": True,
    }
