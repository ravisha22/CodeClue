You are the independent judge for a CodeClue drill-down experiment.

Score the BEFORE answer and AFTER answer against the ground truth.
The goal is to determine whether MCP drill-down materially improved the answer.

Task ID: flask-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the `push` method in RequestContext (ctx.py) to be async, what other components would be impacted?

Ground Truth:
RequestContext.push() is called by Flask.wsgi_app() via RequestContext's __enter__. It sets up _cv_tokens, calls session_interface.open_session(), and triggers appcontext_pushed signal. Making it async would require Flask.wsgi_app(), Flask.full_dispatch_request(), and all before_request/after_request handlers to be async-aware. The testing client (testing.py) also calls push() directly.

BEFORE Answer:
{PASTE_BEFORE_ANSWER_HERE}

AFTER Answer:
{PASTE_AFTER_ANSWER_HERE}

Return valid JSON with this shape:
{
  "task_id": "flask-tf2-001",
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
  "summary": "one short paragraph"
}

Scoring rubric:
- 1.0 = fully correct, covers the important causal/behavioral points
- 0.75 = mostly correct, minor omissions
- 0.50 = partially correct, important structure present but key implications missing
- 0.25 = poor, mostly superficial
- 0.0 = wrong or empty
