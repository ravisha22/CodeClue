# Instructions for GPT 5.4 — Benchmark Consumer (Arm B and Arm A)
# Role: CONSUMER
# You are a BLIND benchmark participant. You answer code comprehension questions.

## Critical Rules — READ FIRST

1. You must NOT read `ground_truth_summary` from any task YAML file.
2. For Arm B: read ONLY the projection file. Do NOT read source files.
3. For Arm A: read ONLY the source files listed. Do NOT reference the projection.
4. Be honest. If you cannot answer from the clue, say what's missing.
5. Do NOT read any files in `experiments/reports/` — those contain prior scores.

## Your Task

Execute 23 benchmark tasks across 7 repositories. For each task, do two rounds.

## Task Definitions

Read the task list from these three files (read questions and relevant_files ONLY,
skip ground_truth_summary):

- `tests/fixtures/lane_a_flask_tasks.yaml` — 5 tasks
- `tests/fixtures/lane_a_extended_tasks.yaml` — 10 tasks  
- `tests/fixtures/lane_a_newrepo_tasks.yaml` — 8 tasks

## For Each Task

### Round 1: Arm B (Clue-First)

Read the projection file:
`experiments/runs/v2-lane-a-{repo_dir}/v2-proj-{task_id}.json`

Where `repo_dir` is:
- flask tasks → `flask`
- fastapi tasks → `fastapi`
- nest tasks → `nest`
- httpx tasks → `httpx`
- express tasks → `express`
- typeorm tasks → `typeorm`
- gin tasks → `gin`

From the projection, read the `projected_nodes`, `projected_edges`, and `confidence` sections.

Answer the `question` from the task YAML using ONLY what you see in the projection.
Then state:
- Was the clue sufficient to fully answer? (yes/no)
- What specific information was missing?

### Round 2: Arm A (Raw Source)

Read the files listed in `relevant_files` from the task YAML.
The source files are at: `experiments/external-repos/{repo_dir}/{file_path}`

Answer the same question using the source code.

## Output

For each task, write a JSON file to:
`experiments/cross-model-eval/results/gpt54-{task_id}.json`

Format:
```json
{
  "task_id": "flask-tf1-001",
  "model": "gpt-5.4",
  "timestamp": "ISO 8601",
  "arm_b": {
    "answer": "Your Arm B answer text",
    "clue_sufficient": false,
    "gaps_identified": ["specific gap 1", "specific gap 2"],
    "confidence_from_projection": 0.95,
    "lookup_hint_from_projection": "clue_only"
  },
  "arm_a": {
    "answer": "Your Arm A answer text"
  }
}
```

## Processing Order

Process all 23 tasks in this order:
1. flask-tf1-001 through flask-tf5-001 (5 tasks)
2. flask-tf1-002, flask-tf2-002 (2 tasks)
3. fastapi-tf1-001, fastapi-tf3-001, fastapi-tf4-001, fastapi-tf5-001 (4 tasks)
4. nest-tf1-001, nest-tf2-001, nest-tf4-001, nest-tf5-001 (4 tasks)
5. httpx-tf2-001, httpx-tf4-001 (2 tasks)
6. express-tf1-001, express-tf5-001 (2 tasks)
7. typeorm-tf3-001, typeorm-tf2-001 (2 tasks)
8. gin-tf1-001, gin-tf5-001 (2 tasks)

After ALL 23 tasks are done, write a completion marker:
`experiments/cross-model-eval/results/gpt54-COMPLETE.json`
```json
{
  "model": "gpt-5.4",
  "tasks_completed": 23,
  "timestamp": "ISO 8601"
}
```
