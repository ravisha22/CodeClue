You are the judge for a CodeClue drill-down experiment.

Important constraints:
- You may be the same underlying model family that produced one or both answers.
- You must behave like a strict rubric judge, not a collaborator.
- Do NOT reward stylistic polish.
- Do NOT infer missing facts charitably.
- Only score what is explicitly present in the answers.

Task ID: httpx-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the Timeout class in _config.py to make all timeouts optional (default None), what components would break?

Ground Truth:
Timeout is used by Client and AsyncClient in _client.py as DEFAULT_TIMEOUT_CONFIG. It's passed to HTTPTransport/AsyncHTTPTransport in _transports/. The transport layers use timeout values for connection pools. Making all None would cause httpcore to use no timeout, potentially hanging on unresponsive servers. The _api.py convenience functions (get, post, etc.) pass timeout through. Test timeouts would also change behavior.

BEFORE Answer:
{PASTE_BEFORE_ANSWER_HERE}

AFTER Answer:
{PASTE_AFTER_ANSWER_HERE}

Return only the JSON object, with no markdown fences and no extra commentary. The output must be suitable for saving verbatim into `answers/judge-result.json`.

Use this exact JSON shape:
{
    "task_id": "httpx-tf2-001",
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
