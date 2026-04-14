You are the judge for a CodeClue drill-down experiment.

Important constraints:
- You may be the same underlying model family that produced one or both answers.
- You must behave like a strict rubric judge, not a collaborator.
- Do NOT reward stylistic polish.
- Do NOT infer missing facts charitably.
- Only score what is explicitly present in the answers.

Task ID: fastapi-tf4-001
Family: TF4
Operation Family: OF4

Question:
What happens when a sync dependency is used inside an async route in FastAPI? Is there a risk of blocking the event loop?

Ground Truth:
FastAPI automatically wraps sync callables using run_in_threadpool() from starlette.concurrency. In solve_dependencies(), if a dependency is not async callable, it's run via run_in_threadpool to avoid blocking. For sync context managers (yield dependencies), contextmanager_in_threadpool in concurrency.py wraps them with a CapacityLimiter to prevent deadlocks. The key risk is that custom middleware or manually called sync functions bypass this protection.

BEFORE Answer:
{PASTE_BEFORE_ANSWER_HERE}

AFTER Answer:
{PASTE_AFTER_ANSWER_HERE}

Return only the JSON object, with no markdown fences and no extra commentary. The output must be suitable for saving verbatim into `answers/judge-result.json`.

Use this exact JSON shape:
{
    "task_id": "fastapi-tf4-001",
    "judge_mode": "same-model-fallback",
    "before": {
        "fidelity_score": 0.0,
        "key_points_hit": [],
        "key_points_missed": [],
        "hallucinations": []
    },
    "after": {
        "fidelity_score": 0.0,
        "key_points_hit": [],
        "key_points_missed": [],
        "hallucinations": []
    },
    "delta": 0.0,
    "did_drilldown_help": true,
    "bias_warning": "same model family used for judging; treat as preliminary evidence",
    "summary": "one short paragraph"
}

Scoring rubric:
- 1.0 = fully correct, covers the important causal/behavioral points
- 0.75 = mostly correct, minor omissions
- 0.50 = partially correct, important structure present but key implications missing
- 0.25 = poor, mostly superficial
- 0.0 = wrong or empty
