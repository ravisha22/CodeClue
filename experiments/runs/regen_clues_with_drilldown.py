"""File 2 drill-down protocol: combined File 1 + source snippets for MECHANISTIC questions.

For each blind-eval task:
  1. Load the pre-generated File 1 clue
  2. Parse the GAPS section to determine question type and drill targets
  3. For MECHANISTIC questions, select high-value File 2 records and source snippets
  4. Write a combined prompt (clue + source drill-down) for evaluation

Budget: max 3000 tokens of drill-down content (keeps total under ~7.5K).
Prioritisation: FOCUS symbols lacking behavioral annotations (highest info gap).

Usage:
  python regen_clues_with_drilldown.py              # full pipeline (extract + render + drilldown)
  python regen_clues_with_drilldown.py --reuse       # reuse existing clue/detail files (fast)
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

import tiktoken

_ENC = tiktoken.get_encoding("cl100k_base")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GOLD_TASKS = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "blind-gold-tasks.json"
CLUE_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "clues"
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "prompts"

LANG_MAP = {
    "aiohttp": "python",
    "click": "python",
    "flask": "python",
    "httpx": "python",
    "fastapi": "python",
    "django": "python",
    "fiber": "go",
    "gin": "go",
    "chi": "go",
    "echo": "go",
    "express": "typescript",
    "nest": "typescript",
    "typeorm": "typescript",
}

DRILLDOWN_TOKEN_BUDGET = 3000

DRILLDOWN_PROMPT_TEMPLATE = """\
# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: {task_id}

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
{clue}
--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
{drill_down_snippets}
--- END SOURCE SNIPPETS ---

QUESTION: {question}

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
"""

# Also keep a plain (non-drilldown) template for STRUCTURAL/RELATIONAL questions
PLAIN_PROMPT_TEMPLATE = """\
# Blind Evaluation Prompt - MRLF v2.1
# Task: {task_id}

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
{clue}
--- CLUE FILE END ---

QUESTION: {question}

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
"""


def _token_count(text: str) -> int:
    return len(_ENC.encode(text))


def _parse_gaps(clue: str) -> dict:
    """Parse the GAPS section from a rendered clue to extract question type and drill targets.

    Returns:
        {
            "question_type": "MECHANISTIC" | "STRUCTURAL" | "RELATIONAL",
            "drill_targets": [{"file": str, "symbol": str, "est_lines": int}, ...],
        }
    """
    result: dict = {"question_type": "STRUCTURAL", "drill_targets": []}

    # GAPS is always the last section — grab everything after "-- GAPS\n"
    gaps_idx = clue.find("\n-- GAPS\n")
    if gaps_idx == -1:
        return result

    gaps_text = clue[gaps_idx + len("\n-- GAPS\n"):]

    # Extract question type
    type_match = re.search(r"type:\s*(STRUCTURAL|RELATIONAL|MECHANISTIC)", gaps_text)
    if type_match:
        result["question_type"] = type_match.group(1)

    # Extract drill targets: "drill: path (~N lines, symbol_name)"
    for drill_match in re.finditer(
        r"drill:\s*(.+?)\s+\(~(\d+)\s+lines?,\s*(.+?)\)", gaps_text
    ):
        result["drill_targets"].append({
            "file": drill_match.group(1),
            "symbol": drill_match.group(3).strip(),
            "est_lines": int(drill_match.group(2)),
        })

    return result


def _load_detail_store(detail_path: Path) -> list[dict]:
    """Load JSONL detail store records."""
    records = []
    if not detail_path.is_file():
        return records
    with open(detail_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _parse_focus_callees(clue: str) -> dict[str, list[str]]:
    """Extract calls: lists from FOCUS entries in the clue.

    Returns: {symbol_name: [callee1, callee2, ...]}
    """
    callees: dict[str, list[str]] = {}
    current_sym = None
    for line in clue.splitlines():
        # FOCUS entry header: "symbol_name (file:line-line)"
        if line and not line.startswith(" ") and "(" in line and not line.startswith("--"):
            current_sym = line.split("(")[0].strip()
        elif current_sym and line.strip().startswith("calls:"):
            calls_text = line.strip()[len("calls:"):].strip()
            callees[current_sym] = [c.strip() for c in calls_text.split(",") if c.strip()]
    return callees


def _extract_question_keywords(question: str) -> set[str]:
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "of", "in", "to", "for",
        "with", "on", "at", "from", "by", "about", "as", "into", "through",
        "during", "before", "after", "above", "below", "between", "out",
        "up", "down", "and", "but", "or", "nor", "not", "so", "yet",
        "what", "which", "who", "whom", "this", "that", "these", "those",
        "how", "when", "where", "why", "all", "each", "every", "both",
        "few", "more", "most", "other", "some", "such", "no", "only",
        "same", "than", "too", "very", "just", "if", "it", "its",
    }
    return set(re.findall(r"[a-zA-Z_]\w{2,}", question.lower())) - stop_words


def _split_compound_words(text: str) -> set[str]:
    parts = re.sub(r"[^a-zA-Z]", " ", text)
    parts = re.sub(r"([a-z])([A-Z])", r"\1 \2", parts)
    return set(re.findall(r"[a-z]{3,}", parts.lower()))


def _record_relevance(rec: dict, question_keywords: set[str]) -> float:
    if not question_keywords:
        return 0.0
    content = " ".join(
        str(rec.get(key, ""))
        for key in ("symbol", "file", "source")
    )
    tokens = _split_compound_words(content)
    return len(tokens & question_keywords) / max(len(question_keywords), 1)


def _select_drill_snippets(
    drill_targets: list[dict],
    detail_records: list[dict],
    repo_path: Path,
    budget: int = DRILLDOWN_TOKEN_BUDGET,
    clue_text: str = "",
    question: str = "",
) -> str:
    """Select and format source snippets for drill-down, within token budget.

    v2.1.1 prioritisation:
      1. Symbols named in drill targets (GAPS-identified, ranked by body size)
      2. Callees of drill-target symbols found in FOCUS (call-chain depth)
      3. If budget remains, other detail records from the same files

    For each selected symbol, prefer the actual source from the detail store
    record, falling back to reading the file from disk using the line range.
    """
    # Build lookup: symbol -> detail record
    by_symbol: dict[str, dict] = {}
    by_file: dict[str, list[dict]] = {}
    for rec in detail_records:
        sym = rec.get("symbol", "")
        by_symbol[sym] = rec
        fp = rec.get("file", "")
        by_file.setdefault(fp, []).append(rec)

    # Parse call chains from FOCUS for Phase 2
    focus_callees = _parse_focus_callees(clue_text) if clue_text else {}

    selected: list[str] = []
    used_symbols: set[str] = set()
    tokens_used = 0
    question_keywords = _extract_question_keywords(question)

    def _try_add(sym: str, target: dict | None = None) -> bool:
        nonlocal tokens_used
        if sym in used_symbols:
            return False
        rec = by_symbol.get(sym)
        snippet = _format_snippet(rec, target, repo_path)
        if not snippet:
            return False
        snippet_tokens = _token_count(snippet)
        if tokens_used + snippet_tokens > budget:
            snippet = _truncate_to_budget(snippet, budget - tokens_used)
            if not snippet:
                return False
        selected.append(snippet)
        used_symbols.add(sym)
        tokens_used += _token_count(snippet)
        return True

    target_order = sorted(
        drill_targets,
        key=lambda target: (
            -_record_relevance(
                by_symbol.get(target["symbol"], {"symbol": target["symbol"], "file": target["file"]}),
                question_keywords,
            ),
            target.get("est_lines", 0),
        ),
    )

    # Phase 1: drill targets from GAPS (ranked by semantic relevance)
    for target in target_order:
        _try_add(target["symbol"], target)
        if tokens_used >= budget:
            break

    # Phase 2: callees of drill-target symbols (call-chain bodies)
    if tokens_used < budget:
        drill_syms = [t["symbol"] for t in drill_targets]
        callee_set: list[str] = []
        for sym in drill_syms:
            for callee in focus_callees.get(sym, []):
                if callee not in callee_set and callee not in used_symbols:
                    callee_set.append(callee)
        callee_set.sort(
            key=lambda sym: -_record_relevance(by_symbol.get(sym, {"symbol": sym}), question_keywords)
        )
        for callee in callee_set:
            _try_add(callee)
            if tokens_used >= budget:
                break

    # Phase 3: other symbols from the same files as drill targets
    if tokens_used < budget:
        target_files = {t["file"] for t in drill_targets}
        for fp in target_files:
            file_records = sorted(
                by_file.get(fp, []),
                key=lambda rec: -_record_relevance(rec, question_keywords),
            )
            for rec in file_records:
                sym = rec.get("symbol", "")
                _try_add(sym)
                if tokens_used >= budget:
                    break
            if tokens_used >= budget:
                break

    if not selected:
        return "(No drill-down snippets available)"

    return "\n\n".join(selected)


def _format_snippet(
    rec: dict | None,
    target: dict | None,
    repo_path: Path,
) -> str | None:
    """Format a single source snippet block for inclusion in the prompt.

    Uses the detail record's source field if available; otherwise reads from disk.
    """
    if rec:
        sym = rec.get("symbol", "unknown")
        fp = rec.get("file", "")
        lines = rec.get("lines", [0, 0])
        source = rec.get("source", "")
    elif target:
        sym = target["symbol"]
        fp = target["file"]
        lines = [0, 0]
        source = ""
    else:
        return None

    # If no source from record, try reading from disk
    if not source and fp:
        source = _read_source_from_disk(repo_path, fp, lines)

    if not source:
        return None

    line_range = f"L{lines[0]}-{lines[1]}" if lines[0] and lines[1] else ""
    header = f"## {sym}  ({fp} {line_range})"
    return f"{header}\n```\n{source}\n```"


def _read_source_from_disk(repo_path: Path, file_path: str, lines: list[int]) -> str:
    """Read source lines from disk as fallback."""
    full_path = repo_path / file_path
    if not full_path.is_file():
        return ""
    try:
        all_lines = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
        start = max(0, (lines[0] or 1) - 1)
        end = lines[1] or len(all_lines)
        return "\n".join(all_lines[start:end])
    except OSError:
        return ""


def _truncate_to_budget(snippet: str, budget_tokens: int) -> str | None:
    """Truncate a snippet to fit within a token budget, keeping the header."""
    if budget_tokens <= 20:
        return None

    lines = snippet.splitlines()
    # Keep removing lines from the end until it fits
    while lines and _token_count("\n".join(lines)) > budget_tokens:
        lines.pop()

    if len(lines) <= 2:  # Only header + code fence left
        return None

    # Ensure we close the code fence
    text = "\n".join(lines)
    if not text.rstrip().endswith("```"):
        text += "\n... (truncated)\n```"

    return text


def main():
    reuse = "--reuse" in sys.argv

    with open(GOLD_TASKS) as f:
        tasks = json.load(f)

    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    CLUE_DIR.mkdir(parents=True, exist_ok=True)

    # Group tasks by repo
    repos: dict[str, dict] = {}
    for t in tasks:
        repo = t["repo"]
        if repo not in repos:
            repos[repo] = {"path": t["repo_path"], "tasks": []}
        repos[repo]["tasks"].append(t)

    stats = {"total": 0, "mechanistic": 0, "structural": 0, "relational": 0}

    for repo, info in repos.items():
        print(f"\n--- Processing {repo} ---")
        repo_path = REPO_ROOT / info["path"]
        lang = LANG_MAP.get(repo, "python")
        detail_path = CLUE_DIR / f"{repo}.codeclue-detail"

        if reuse:
            # Fast path: load existing artifacts
            detail_records = _load_detail_store(detail_path)
            print(f"  Reusing detail store: {len(detail_records)} records")
        else:
            # Full pipeline: extract graph, generate clue + detail store
            from codeclue_research.extractor import extract_graph
            from codeclue_research.clue_view_mrlf import generate_detail_store

            graph = extract_graph(repo_path, language=lang)
            print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

            detail_records = generate_detail_store(graph, repo_root=repo_path)
            with open(detail_path, "w", encoding="utf-8") as f:
                for rec in detail_records:
                    f.write(json.dumps(rec) + "\n")
            print(f"  Detail store: {len(detail_records)} records")

        for t in info["tasks"]:
            task_id = t["task_id"]
            question = t["question"]
            stats["total"] += 1

            # Load or generate File 1 clue
            clue_path = CLUE_DIR / f"{task_id}.codeclue"
            if reuse and clue_path.is_file():
                clue = clue_path.read_text(encoding="utf-8")
            else:
                from codeclue_research.clue_view_mrlf import render_mrlf
                clue = render_mrlf(graph, question, repo_root=repo_path)
                clue_path.write_text(clue, encoding="utf-8")

            # Parse GAPS to decide protocol
            gaps_info = _parse_gaps(clue)
            q_type = gaps_info["question_type"]
            drill_targets = gaps_info["drill_targets"]

            if q_type == "MECHANISTIC" and drill_targets:
                stats["mechanistic"] += 1
                snippets = _select_drill_snippets(
                    drill_targets, detail_records, repo_path,
                    clue_text=clue,
                    question=question,
                )
                snippet_tokens = _token_count(snippets)
                clue_tokens = _token_count(clue)

                prompt = DRILLDOWN_PROMPT_TEMPLATE.format(
                    task_id=task_id,
                    clue=clue,
                    drill_down_snippets=snippets,
                    question=question,
                )
                prompt_path = PROMPT_DIR / f"{task_id}-drilldown.prompt.md"
                prompt_path.write_text(prompt, encoding="utf-8")

                print(f"  {task_id}: MECHANISTIC — drilldown prompt")
                print(f"    clue: {clue_tokens} tok, snippets: {snippet_tokens} tok, "
                      f"total: {_token_count(prompt)} tok")
                print(f"    drill targets: {[dt['symbol'] for dt in drill_targets]}")
            else:
                key = q_type.lower()
                if key == "mechanistic":
                    stats["mechanistic"] += 1
                else:
                    stats[key] += 1
                prompt = PLAIN_PROMPT_TEMPLATE.format(
                    task_id=task_id,
                    clue=clue,
                    question=question,
                )
                prompt_path = PROMPT_DIR / f"{task_id}-drilldown.prompt.md"
                prompt_path.write_text(prompt, encoding="utf-8")

                print(f"  {task_id}: {q_type} — plain prompt (no drill-down needed)")
                print(f"    clue: {_token_count(clue)} tok, total: {_token_count(prompt)} tok")

    print()
    print("=" * 60)
    print(f"DONE: {stats['total']} tasks processed")
    print(f"  MECHANISTIC (drilldown): {stats['mechanistic']}")
    print(f"  STRUCTURAL (plain):      {stats['structural']}")
    print(f"  RELATIONAL (plain):      {stats['relational']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
