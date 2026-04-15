"""Generate baseline comparison prompts for the same blind-eval gold tasks.

Baselines:
  1. raw-topk: Give GPT-5.4 the top-k most relevant source files (by filename
     match to question keywords), within ~6K token budget. No clue format.
  2. summary: A plain English repo description (tree + module list), ~500 tokens.
     No symbols, no call graph, no behavioral patterns.

Both use the same gold tasks, same answerer, same scoring protocol.
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
PROMPT_DIR = REPO_ROOT / "experiments" / "runs" / "blind-eval" / "baselines"
TOKEN_BUDGET = 6000  # match clue+drill-down budget


def _tok(text: str) -> int:
    return len(_ENC.encode(text))


def _question_keywords(question: str) -> list[str]:
    """Extract meaningful keywords from a question for file ranking."""
    stop = {"the", "a", "an", "is", "are", "does", "do", "how", "what", "when",
            "where", "which", "and", "or", "not", "if", "in", "on", "to", "for",
            "of", "from", "by", "with", "that", "this", "it", "its", "into",
            "can", "be", "has", "have", "will", "was", "were", "been"}
    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", question.lower())
    return [w for w in words if w not in stop and len(w) > 2]


def _score_file(file_path: str, keywords: list[str]) -> float:
    """Score a file's relevance to question keywords based on path/name."""
    fp_lower = file_path.lower()
    score = 0.0
    for kw in keywords:
        if kw in fp_lower:
            score += 2.0
        # partial match
        if any(kw in part for part in fp_lower.split("/")):
            score += 1.0
    return score


def _get_source_files(repo_path: Path, lang: str) -> list[Path]:
    ext_map = {"python": "*.py", "go": "*.go", "typescript": "*.ts"}
    ext = ext_map.get(lang, "*.py")
    files = []
    for f in repo_path.rglob(ext):
        if any(p.startswith(".") for p in f.parts):
            continue
        if "_test" in f.name or "test_" in f.name:
            continue
        files.append(f)
    return sorted(files)


LANG_MAP = {
    "aiohttp": "python", "click": "python", "fiber": "go",
}

RAW_PROMPT = (
    "# Baseline Evaluation: Raw Source Files\n"
    "# Task: {task_id}\n\n"
    "You are a senior software engineer. You have been given raw source code\n"
    "excerpts from a repository. Answer the question using ONLY the source\n"
    "code below. Do not use any external knowledge about the framework.\n\n"
    "--- SOURCE CODE ---\n{source}\n--- END SOURCE CODE ---\n\n"
    "QUESTION: {question}\n\n"
    "Provide a detailed answer citing specific functions/files from the source.\n"
)

SUMMARY_PROMPT = (
    "# Baseline Evaluation: Plain Summary\n"
    "# Task: {task_id}\n\n"
    "You are a senior software engineer. You have been given a brief summary\n"
    "of a repository's structure. Answer the question using ONLY this summary.\n"
    "Do not use any external knowledge about the framework.\n\n"
    "--- REPOSITORY SUMMARY ---\n{summary}\n--- END SUMMARY ---\n\n"
    "QUESTION: {question}\n\n"
    "Provide a detailed answer based solely on the summary above.\n"
    "If the summary doesn't contain enough information, say what you CAN and CANNOT determine.\n"
)


def _build_summary(repo_path: Path, lang: str) -> str:
    """Build a plain-text repo summary (~500 tokens)."""
    lines = [f"Repository: {repo_path.name}"]
    # Tree
    lines.append("\nDirectory structure:")
    for d in sorted(repo_path.iterdir()):
        if d.name.startswith("."):
            continue
        if d.is_dir():
            n_files = sum(1 for _ in d.rglob("*") if _.is_file())
            lines.append(f"  {d.name}/ ({n_files} files)")
        else:
            lines.append(f"  {d.name}")

    # Module listing
    ext_map = {"python": "*.py", "go": "*.go", "typescript": "*.ts"}
    ext = ext_map.get(lang, "*.py")
    src_files = _get_source_files(repo_path, lang)
    lines.append(f"\nSource files ({len(src_files)} {lang} files):")
    for f in src_files[:30]:
        rel = f.relative_to(repo_path)
        lines.append(f"  {rel} ({f.stat().st_size // 1024}KB)")
    if len(src_files) > 30:
        lines.append(f"  ... and {len(src_files) - 30} more files")

    return "\n".join(lines)


def _build_raw_topk(repo_path: Path, lang: str, question: str, budget: int) -> str:
    """Select top-k source files by keyword relevance, within token budget."""
    keywords = _question_keywords(question)
    src_files = _get_source_files(repo_path, lang)

    # Score and rank
    scored = []
    for f in src_files:
        rel = str(f.relative_to(repo_path))
        score = _score_file(rel, keywords)
        scored.append((score, rel, f))

    scored.sort(key=lambda x: (-x[0], x[1]))

    # Take top files within budget
    selected = []
    tokens_used = 0
    for score, rel, fp in scored:
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_tokens = _tok(content)

        if tokens_used + file_tokens > budget:
            # Try truncating
            remaining = budget - tokens_used
            if remaining > 100:
                lines = content.splitlines()
                truncated = []
                t = 0
                for line in lines:
                    lt = _tok(line)
                    if t + lt > remaining - 20:
                        break
                    truncated.append(line)
                    t += lt
                if truncated:
                    content = "\n".join(truncated) + "\n... (truncated)"
                else:
                    continue
            else:
                continue

        header = f"## {rel} (score: {score:.1f})"
        block = f"{header}\n```\n{content}\n```"
        selected.append(block)
        tokens_used += _tok(block)

        if tokens_used >= budget:
            break

    if not selected:
        return "(No source files matched the question keywords)"

    return "\n\n".join(selected)


def main():
    with open(GOLD_TASKS) as f:
        tasks = json.load(f)

    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    for t in tasks:
        task_id = t["task_id"]
        repo = t["repo"]
        question = t["question"]
        repo_path = REPO_ROOT / t["repo_path"]
        lang = LANG_MAP.get(repo, "python")

        # Raw top-k baseline
        raw_source = _build_raw_topk(repo_path, lang, question, TOKEN_BUDGET)
        raw_prompt = RAW_PROMPT.format(
            task_id=task_id, source=raw_source, question=question
        )
        raw_path = PROMPT_DIR / f"{task_id}-raw-topk.prompt.md"
        raw_path.write_text(raw_prompt, encoding="utf-8")
        print(f"{task_id} raw-topk: {_tok(raw_prompt)} tokens")

        # Summary baseline
        summary = _build_summary(repo_path, lang)
        summary_prompt = SUMMARY_PROMPT.format(
            task_id=task_id, summary=summary, question=question
        )
        summary_path = PROMPT_DIR / f"{task_id}-summary.prompt.md"
        summary_path.write_text(summary_prompt, encoding="utf-8")
        print(f"{task_id} summary: {_tok(summary_prompt)} tokens")

    print("\nDone.")


if __name__ == "__main__":
    main()
