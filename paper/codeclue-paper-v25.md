# CodeClue: Compressed Code Comprehension Artifacts for LLM Consumption

**Ravi Nandagopalan**

## Abstract
Large language models can assist with software engineering only when they receive enough repository context to answer code comprehension questions. In practice, full-source prompting is often too expensive, while retrieval-heavy or agentic browsing pipelines incur repeated latency and token costs. This paper presents **CodeClue**, an open-source system for generating persistent, versioned code comprehension artifacts for LLM consumption. CodeClue's **MRLF** (Multi-Resolution Lattice Format) uses a deterministic two-tier design: **File 1** is a \<=4K-token clue optimized for direct prompting, and **File 2** is a JSONL detail store for targeted drill-down. Across 10 open-source repositories in Python, Go, and TypeScript, with 208 gold facts (40 development, 168 blind), MRLF achieved **97% compression** while retaining useful comprehension on the blind set: **51.8% structural**, **60.7% relational**, and **41.1% mechanistic**. Repo-level bootstrap gave a blind overall interval of **[37.5%, 65.5%]**. A reasoning scaffold materially improved weaker models without changing the format, raising Sonnet 4.6 from **50.0%** to **81.3%** on a shared 8-task subset.

## 1. Introduction
LLM-based programming assistants face a basic scaling problem: repositories are much larger than the context that can be economically sent on every turn. Even when a model can technically accept long inputs, long-context use remains expensive and often brittle, with quality degrading when relevant evidence is diluted across large prompts [1]. For code tasks, the default alternatives are usually (i) retrieval-augmented prompting, which repeatedly fetches raw files or snippets [2,3], or (ii) agentic browsing, where the model spends multiple tool calls rediscovering structure that has not changed since the previous session. Both approaches are useful, but both pay comprehension cost repeatedly.

CodeClue targets a different operating point: generate a **persistent, versioned, deterministic artifact** that captures a compressed view of repository structure and behavior, then let models drill down only when needed. The design goal is not to replace source code, but to provide a stable intermediate representation for LLM consumption that is small enough to fit in a prompt, rich enough to answer many questions directly, and explicit about what it cannot answer.

This paper focuses on **MRLF**, CodeClue's open-source clue format. MRLF is motivated by three observations. First, many code comprehension questions are structural or relational rather than fully mechanistic. Second, deterministic extraction is valuable because it reduces hallucination risk in the artifact itself. Third, models differ not only in parsing ability, but in how well they reason over compressed evidence; this suggests that the format and the reasoning protocol should be evaluated separately.

We make four contributions:

1. **MRLF**, a two-file, two-tier code comprehension artifact with deterministic \<=4K-token clue files and explicit drill-down semantics.
2. An **open-source implementation** with deterministic extractors for Python, Go, and TypeScript plus an MCP server for tool-based consumption.
3. A concise evaluation on **10 open-source repositories** and **208 gold facts**, including a blind protocol and repo-level uncertainty reporting.
4. A **reasoning scaffold** contribution showing that cross-model performance gaps narrow substantially without changing the underlying format.

## 2. MRLF Format Design
MRLF uses a **two-file architecture**. **File 1** is the primary clue and is constrained to roughly \<=4K tokens. **File 2** is a JSONL detail store keyed by stable identifiers for selective drill-down. The first file is designed for low-latency prompting; the second preserves detail without forcing every interaction to pay full context cost.

File 1 is organized into five ordered resolution levels:

- **TREE**: coarse repository and directory structure.
- **INDEX**: module inventory and top exports.
- **SYM**: repository-wide symbol table.
- **FOCUS**: question-conditioned symbol detail.
- **GAPS**: explicit self-report of insufficiency, uncovered evidence, and recommended drill-down.

The design intentionally separates *coverage* from *confidence*. TREE/INDEX/SYM provide broad deterministic coverage, while FOCUS concentrates budget on symbols most relevant to a question. GAPS then states whether the clue is likely sufficient. This section is central to MRLF's contract with the consuming model: instead of implying completeness, MRLF explicitly says when the model should stop, answer, or drill down.

A second design element is **behavioral pattern extraction**. FOCUS entries can include compact, deterministic summaries such as **GUARD**, **BRANCH**, **PRECEDENCE**, **DELEGATE**, **ACCUMULATE**, **TRANSFORM**, **UNWIND**, and **DISPATCH**. These patterns are intended to preserve the gist of method-body logic at much lower cost than raw code. They are lossy by design: enough to support many mechanistic inferences, but not a claim of full semantic equivalence.

Finally, MRLF includes a **reasoning scaffold**. The scaffold is not part of the extracted repository artifact; rather, it is a model-facing prompt protocol that encourages stepwise evidence use: inspect clue sections first, classify the question type, consult GAPS, and only then request File 2 details. This separates artifact quality from reasoning quality and supports model-agnostic consumption.

## 3. Implementation
CodeClue is implemented as an **open-source** pipeline with deterministic extraction for **Python, Go, and TypeScript**. The extractor builds repository-level symbol and relation data from language-specific AST passes. File 1 rendering is deterministic given a repository snapshot and question; repeated runs over unchanged inputs produce the same clue structure.

FOCUS selection uses a **graph-structural ranking** rather than raw lexical matching alone. The current implementation combines semantic anchoring from available symbol descriptions with structural signals such as containment expansion and blended graph ranking. This is intended to generalize across repositories whose naming conventions differ substantially.

A lightweight **question classifier** routes queries into clue-only or drill-down-first protocols. Structural and many relational tasks are usually answerable from File 1, whereas deeper mechanistic questions more often require File 2. The **GAPS** section exposes this estimate directly to the consumer.

For interactive use, CodeClue exposes an **MCP server** with typed drill-down tools. In effect, MRLF becomes a small persistent front-end to repository understanding, while MCP tools provide on-demand expansion. This keeps the base interaction cheap while preserving a controlled path to higher fidelity.

## 4. Evaluation
We evaluated CodeClue on **10 open-source repositories** across **3 languages** (Python, Go, TypeScript) using **208 gold facts**: **40 development** facts and **168 blind** facts. The blind protocol was intended to reduce tuning bias: blind-set questions and scoring targets were frozen before answer generation, and blind-set analysis was separated from implementation iteration. Gold facts for blind evaluation were created under a source-independent protocol rather than by inspecting clue outputs.

Evaluation used a standardized **GPT-5.4 scoring rubric** with fact-level binary judgments. To estimate scorer stability, we obtained a second set of judgments from **Sonnet 4.6** on an 8-task stratified sample, obtaining **81.2% agreement** and **Cohen's kappa = 0.607**, which indicates moderate agreement.

Gold difficulty was intentionally reported because the benchmark is not uniform. In the mechanistic subset, the development facts were much harder (**75.0% DEEP**) than the blind facts (**12.5% DEEP**), so dev-blind comparisons should be interpreted cautiously.

### 4.1 Results by Task Family
Table 1 reports the **blind-set** results by task family. These are reported **separately**, not pooled across families, because structural, relational, and mechanistic questions stress different parts of the format.

| Family | Covered / Total | Coverage | 95% CI |
| --- | ---: | ---: | --- |
| Structural | 29 / 56 | 51.8% | [39.0%, 64.3%] |
| Relational | 34 / 56 | 60.7% | [47.6%, 72.4%] |
| Mechanistic | 23 / 56 | 41.1% | [29.2%, 54.1%] |

A cluster-aware bootstrap at the repository level gave **blind overall = 51.2%** with **95% CI [37.5%, 65.5%]**.

### 4.2 Results by Repository
Blind-set performance varied widely across repositories:

| Repository | Language | Score |
| --- | --- | ---: |
| zod | TypeScript | 83.3% |
| requests | Python | 70.8% |
| echo | Go | 58.3% |
| express | TypeScript/JavaScript ecosystem | 45.8% |
| gin | Go | 41.7% |
| httpx | Python | 33.3% |
| fastapi | Python | 25.0% |

The spread suggests that MRLF is not uniformly effective across architectures. It worked well on some API-centric libraries (e.g., zod, requests) but struggled on frameworks with more dispersed behavioral logic (e.g., FastAPI).

### 4.3 Baselines
We compared MRLF against two cheap baselines under approximately the same **~6K token** budget on a matched subset:

| Method | Score |
| --- | ---: |
| Summary (filenames only) | 0 / 24 = 0.0% |
| Raw top-*k* source | 2 / 24 = 8.3% |
| MRLF | substantially higher on all task families |

The filename summary baseline failed completely, and shallow raw-source retrieval was only marginally better. This suggests that the value is not merely compression, but the structure of the compressed artifact.

### 4.4 Ablation
Mechanistic tasks benefited from the two-tier design:

| Configuration | Mechanistic score |
| --- | ---: |
| File 1 only | 22.9% |
| File 1 + File 2 | 47.9% |

The **drill-down lift was +25 percentage points**, supporting the main architectural claim that a small clue file should be paired with targeted detail retrieval rather than forced to carry all semantics directly.

### 4.5 Cross-Model Validation
On the same **8-task / 32-fact** subset, six models were evaluated with the same MRLF inputs:

| Model | Score |
| --- | ---: |
| GPT-5.4 | 75.0% |
| Sonnet 4.6 | 50.0% |
| Haiku | 50.0% |
| Goldeneye | 43.8% |
| Sonnet 4 | 43.8% |
| GPT-5.4-mini | 34.4% |

With the **reasoning scaffold**, **Sonnet 4.6** improved from **50.0%** to **81.3%** (**+31.3 percentage points**). This is an important finding: the format itself appears largely model-agnostic, while a substantial share of the gap is attributable to reasoning protocol rather than parsing failure.

### 4.6 Success Factors
We summarize the study against four predefined success factors:

| Factor | Criterion | Result |
| --- | --- | --- |
| SF1 | Compression ratio \>= 85% | **97%** — PASS |
| SF2 | Clue-only accuracy \>= 60% | **Relational 60.7%** — at threshold |
| SF3 | Drill-down dependency ratio \<= 40% | **~35%** of tasks required drill-down — PASS |
| SF4 | Post-drill improvement \>= +10pp | **+25pp** — PASS |

## 5. Discussion
The evaluation gives a mixed but useful picture. First, the **dev-blind gap was only 3.8 percentage points** (**55.0% vs. 51.2%**), which argues against severe overfitting despite iterative development. Second, the format clearly preserves some kinds of knowledge better than others: structural and relational facts survive compression better than mechanistic ones.

At the same time, the repository-level spread is a real limitation. The four expansion repositories (**fastapi, gin, express, httpx**) averaged **36.5%**, well below the original trio's **70.8%** average. This suggests that MRLF's current extraction and ranking strategy works better on some architectures than others, especially where public API behavior is more explicitly surfaced.

The reasoning scaffold result is also consequential. If Sonnet 4.6 can move from **50.0%** to **81.3%** without changing MRLF, then part of the challenge is not compression quality per se, but getting models to reason carefully over compressed evidence. That makes scaffolding a first-class systems contribution rather than a prompt-engineering footnote.

Limitations remain. **(1)** Some repositories scored poorly, especially **FastAPI at 25.0%**, so the current format should not be presented as uniformly effective. **(2)** Gold facts were created with LLM assistance, which may bias benchmark construction even under a blind protocol. **(3)** GPT-5.4 was the primary scorer, so although inter-rater agreement is encouraging, the evaluation is not scorer-independent. **(4)** Per-repository sample sizes remain small.

## 6. Related Work
MRLF sits between retrieval-based and summarization-based approaches. **Retrieval-augmented generation (RAG)** retrieves evidence on demand but typically does not preserve a durable repository-level comprehension state [2]. Recent repository-scale coding systems such as **RepoCoder** apply iterative retrieval and generation to code tasks [3], but still reassemble task context dynamically rather than relying on a versioned intermediate artifact.

MRLF also relates to **code summarization**. Prior work has shown that source code can be compacted into natural-language summaries or learned representations [4,5], but those approaches usually optimize for human readability or function-level summaries rather than a deterministic, hierarchical artifact for tool-mediated LLM use.

A third connection is **long-context management**. Long context helps only up to a point; models frequently underuse relevant evidence when it is buried in large prompts [1]. MRLF can be viewed as an attempt to restructure code context before prompting rather than merely extending the window.

Finally, MRLF is informed by **developer cognition** research. Sillito et al. showed that developers ask recurrent question types during change tasks, and that these questions vary in the depth of comprehension they require [6,7]. Our task-family separation follows this intuition: structural and relational questions differ materially from mechanistic ones and should not be conflated.

## 7. Conclusion
CodeClue shows that an **open-source**, deterministic, model-agnostic code comprehension artifact can preserve useful repository understanding at large compression ratios. In our study, MRLF achieved **97% compression** while retaining meaningful blind-set performance, especially for **structural (51.8%)** and **relational (60.7%)** questions. The **two-tier architecture** was validated by a **+25pp** drill-down lift on mechanistic tasks. The reasoning scaffold further showed that weaker models can close much of the gap without changing the artifact itself.

The main next steps are clearer behavioral summaries, broader benchmarks, more balanced blind sets, and human evaluation. The broader lesson is that compressed context for code should be treated not just as summarization, but as a first-class systems artifact with explicit sufficiency boundaries.

## References
[1] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. *Lost in the Middle: How Language Models Use Long Contexts*. Transactions of the Association for Computational Linguistics, 2024.

[2] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, and Douwe Kiela. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS, 2020.

[3] Zecheng Zhang, Hong Jin, Zhe Wang, Quanming Yao, Yong Jiang, and Yangqiu Song. *RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation*. arXiv, 2023.

[4] Sonia Haiduc, Jairo Aponte, Laura Moreno, and Andrian Marcus. *On the Use of Automated Text Summarization Techniques for Summarizing Source Code*. WCRE, 2010.

[5] Xing Hu, Ge Li, Xin Xia, David Lo, and Zhi Jin. *Summarizing Source Code using a Neural Attention Model*. ACL, 2016.

[6] Jonathan Sillito, Gail C. Murphy, and Kris De Volder. *Questions Programmers Ask During Software Evolution Tasks*. FSE, 2006.

[7] Jonathan Sillito, Gail C. Murphy, and Kris De Volder. *Asking and Answering Questions During a Programming Change Task*. IEEE Transactions on Software Engineering, 2008.
