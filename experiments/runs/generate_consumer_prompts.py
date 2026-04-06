"""Generate consumer prompts for manual LLM invocation.

Creates one prompt file per task × plan combination. You paste each prompt
into ChatGPT/Gemini/Claude, save the response, then run score_responses.py.

Usage:
    python experiments/runs/generate_consumer_prompts.py

Output:
    experiments/runs/consumer-prompts/
    ├── flask-tf1-001_plan-a.prompt.md
    ├── flask-tf1-001_plan-b.prompt.md
    ├── flask-tf2-001_plan-a.prompt.md
    └── ... (23 tasks × 2 plans = 46 prompt files)

Workflow:
    1. Run this script to generate prompts
    2. For each prompt file, paste content into your LLM chat
    3. Save the response as the same filename but .response.md
       e.g., flask-tf1-001_plan-a.response.md
    4. Run: python experiments/runs/score_responses.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from codeclue_research.clue_view_plan_a import render_clue_plan_a
from codeclue_research.clue_view_plan_b import render_clue_plan_b
from codeclue_research.io import load_graph
from codeclue_research.token_counter import count_tokens


TASKS: list[tuple[str, str, str, str, str]] = [
    ("flask-tf1-001", "v2-lane-a-flask", "v2-proj-flask-tf1-001.json", "What is the high-level architecture of Flask's request handling?", "TF1"),
    ("flask-tf1-002", "v2-lane-a-flask", "v2-proj-flask-tf1-002.json", "How are Flask blueprints structured?", "TF1"),
    ("flask-tf2-001", "v2-lane-a-flask", "v2-proj-flask-tf2-001.json", "What is the downstream impact of modifying Flask.wsgi_app?", "TF2"),
    ("flask-tf2-002", "v2-lane-a-flask", "v2-proj-flask-tf2-002.json", "What is the impact of changing Flask.dispatch_request?", "TF2"),
    ("flask-tf3-001", "v2-lane-a-flask", "v2-proj-flask-tf3-001.json", "Where should the edit be made to add a new request hook?", "TF3"),
    ("flask-tf4-001", "v2-lane-a-flask", "v2-proj-flask-tf4-001.json", "What behavioral gotcha exists in Flask's request dispatch path?", "TF4"),
    ("flask-tf5-001", "v2-lane-a-flask", "v2-proj-flask-tf5-001.json", "What security concerns exist in Flask's session handling?", "TF5"),
    ("fastapi-tf1-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf1-001.json", "What is FastAPI's request routing architecture?", "TF1"),
    ("fastapi-tf3-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf3-001.json", "Where to edit to add middleware in FastAPI?", "TF3"),
    ("fastapi-tf4-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf4-001.json", "What gotcha exists in FastAPI dependency injection?", "TF4"),
    ("fastapi-tf5-001", "v2-lane-a-fastapi", "v2-proj-fastapi-tf5-001.json", "Security concerns in FastAPI's CORS handling?", "TF5"),
    ("nest-tf1-001", "v2-lane-a-nest", "v2-proj-nest-tf1-001.json", "What is NestJS module architecture?", "TF1"),
    ("nest-tf2-001", "v2-lane-a-nest", "v2-proj-nest-tf2-001.json", "Impact of changing NestJS dependency injection container?", "TF2"),
    ("nest-tf4-001", "v2-lane-a-nest", "v2-proj-nest-tf4-001.json", "Behavioral gotchas in NestJS middleware pipeline?", "TF4"),
    ("nest-tf5-001", "v2-lane-a-nest", "v2-proj-nest-tf5-001.json", "Security concerns in NestJS guards?", "TF5"),
    ("httpx-tf2-001", "v2-lane-a-httpx", "v2-proj-httpx-tf2-001.json", "Impact of modifying httpx transport layer?", "TF2"),
    ("httpx-tf4-001", "v2-lane-a-httpx", "v2-proj-httpx-tf4-001.json", "Gotchas in httpx connection pooling?", "TF4"),
    ("express-tf1-001", "v2-lane-a-express", "v2-proj-express-tf1-001.json", "Express middleware architecture?", "TF1"),
    ("express-tf5-001", "v2-lane-a-express", "v2-proj-express-tf5-001.json", "Security in Express request parsing?", "TF5"),
    ("typeorm-tf2-001", "v2-lane-a-typeorm", "v2-proj-typeorm-tf2-001.json", "Impact of TypeORM connection changes?", "TF2"),
    ("typeorm-tf3-001", "v2-lane-a-typeorm", "v2-proj-typeorm-tf3-001.json", "Where to add TypeORM migration support?", "TF3"),
    ("gin-tf1-001", "v2-lane-a-gin", "v2-proj-gin-tf1-001.json", "Gin router architecture?", "TF1"),
    ("gin-tf5-001", "v2-lane-a-gin", "v2-proj-gin-tf5-001.json", "Security in Gin middleware chain?", "TF5"),
]


def _build_prompt(question: str, clue: dict, plan: str) -> str:
    """Build a complete consumer prompt from template + clue."""
    template_path = ROOT / "scaffold" / "prompts" / f"arm-plan-{plan}.md"
    template = template_path.read_text(encoding="utf-8")

    clue_json = json.dumps(clue, indent=2, ensure_ascii=False)

    prompt = template.replace("{{QUESTION}}", question)
    prompt = prompt.replace("{{CLUE_JSON}}", clue_json)
    return prompt


def main() -> None:
    runs_dir = ROOT / "experiments" / "runs"
    out_dir = runs_dir / "consumer-prompts"
    out_dir.mkdir(parents=True, exist_ok=True)
    external_repos = ROOT / "experiments" / "external-repos"

    repo_dirs = {
        "flask": external_repos / "flask",
        "fastapi": external_repos / "fastapi",
        "nest": external_repos / "nest",
        "httpx": external_repos / "httpx",
        "express": external_repos / "express",
        "typeorm": external_repos / "typeorm",
        "gin": external_repos / "gin",
    }

    manifest: list[dict] = []
    skipped: list[str] = []

    for task_id, lane_dir, proj_file, question, family in TASKS:
        proj_path = runs_dir / lane_dir / proj_file
        graph_path = runs_dir / lane_dir / "graph.json"

        if not proj_path.is_file() or not graph_path.is_file():
            skipped.append(task_id)
            continue

        repo_key = lane_dir.replace("v2-lane-a-", "")
        repo_root = repo_dirs.get(repo_key, ROOT)

        with open(proj_path, "r", encoding="utf-8") as f:
            projection = json.load(f)
        graph = load_graph(graph_path)

        for plan_label, renderer in [("a", render_clue_plan_a), ("b", render_clue_plan_b)]:
            clue = renderer(projection, graph, question, str(repo_root))
            prompt = _build_prompt(question, clue, plan_label)

            # Save prompt file
            fname = f"{task_id}_plan-{plan_label}.prompt.md"
            (out_dir / fname).write_text(prompt, encoding="utf-8")

            # Save clue artifact for scoring later
            clue_fname = f"{task_id}_plan-{plan_label}.clue.json"
            (out_dir / clue_fname).write_text(
                json.dumps(clue, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            manifest.append({
                "task_id": task_id,
                "family": family,
                "plan": plan_label,
                "prompt_file": fname,
                "response_file": fname.replace(".prompt.md", ".response.md"),
                "clue_file": clue_fname,
                "question": question,
                "prompt_tokens": count_tokens(prompt),
                "clue_tokens": count_tokens(clue),
            })

    # Save manifest
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(manifest)} prompt files in {out_dir}")
    print(f"Skipped: {len(skipped)} tasks")
    print(f"Manifest: {manifest_path}")
    print()
    print("=== NEXT STEPS ===")
    print("1. Open each .prompt.md file")
    print("2. Paste its content into ChatGPT / Gemini / Claude")
    print("3. Save the response as the matching .response.md file")
    print(f"   e.g., {manifest[0]['prompt_file']} → {manifest[0]['response_file']}")
    print("4. Run: python experiments/runs/score_responses.py")


if __name__ == "__main__":
    main()
