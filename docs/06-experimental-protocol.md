# Experimental Protocol

## Study Arms

- A: raw-source-first baseline
- B: clue-first full regeneration
- C: clue-first delta update
- D: optional map-plus-retrieval comparator

## Task Matrix

Use task families TF1 through TF5 with easy, medium, and hard strata.

## Primary Outcomes

- Token Reduction Ratio (TRR)
- Fidelity Score (FS)
- Delta Non-Inferiority Gap (DNG)
- Drift Slope (DS)
- CCT metrics (PP, PR, CS, CRR, PDI)

## Statistical Plan

- Bootstrap confidence intervals for TRR and FS.
- Non-inferiority testing for C vs B.
- Mixed-effects model with repository random effects.

## External Benchmark Path

- Minimum 12 repos in 500k to 700k token band.
- At least 30 tasks per repo.
- Commit freeze and preregistration before execution.

## Pre-Registered Replay Set (v1 Seed)

This seed set is a concrete, replayable appendix for Sprint 4 trial runs before
full 12-repository benchmark scale-up.

Selection policy:

1. Public repositories only.
2. Mixed language coverage (Python and TypeScript).
3. PR-level commit freeze via `merge_commit_sha` for merged entries.
4. Include closed-unmerged controls for robustness checks.

Manifest artifact:

- `experiments/reports/pr-replay-set-v1.json`

Seed entries (15 total):

| Repo | PR | Tier | Merge Commit / Head SHA |
| --- | ---: | --- | --- |
| pallets/flask | 5928 | merged-core | c34d6e81fd8e405e6d4178bf24b364918811ef17 |
| pallets/flask | 5917 | merged-core | 12e95c93b488725f80753f34b2e0d24838ca4646 |
| pallets/flask | 5898 | merged-core | 809d5a8869d4ffe8656680b2438b10f7c8845613 |
| pallets/flask | 5964 | closed-control | b00c66248d9c7fa5ac52ecd7d39bc1e8fa589f2a |
| pallets/flask | 5956 | closed-control | 8342e6871214defcc98ca5c27ea66f118be4d60c |
| fastapi/fastapi | 15038 | merged-core | 8a9258b169dce3e321f614c14b1877c18750d6c7 |
| fastapi/fastapi | 15139 | merged-core | aeb9f4bb854d030803e2d13cdb64dd0bc5843f00 |
| fastapi/fastapi | 15151 | merged-core | 6e5e94208eb8f6ef82bc07ac30405b0e57cc5918 |
| fastapi/fastapi | 15246 | closed-control | 0d5ecfae6747bcf2b13ffe1a440eaf860b7930b6 |
| fastapi/fastapi | 15245 | closed-control | a93a92f187a8c985e71870f06624c4d2c01e12c5 |
| nestjs/nest | 16506 | merged-core | 8366143e4086d3a70c286ac59abff073d08464bc |
| nestjs/nest | 16464 | merged-core | 3c181b2c11f47fba4b9c21b9623b828e9259528d |
| nestjs/nest | 16640 | merged-core | 3bd47abc54d7485ee34103525c06e5165b9b2634 |
| nestjs/nest | 16658 | closed-control | 70bfe5bfe4c50c13080df2cb6d28079afb6db126 |
| nestjs/nest | 16656 | closed-control | ac9ca041dd12a92b8c80cf7b8d167f1a9fa90bd0 |

Regeneration protocol:

1. Use GitHub REST `GET /repos/{owner}/{repo}/pulls/{number}` for each entry.
2. Persist: repo, PR number, title, state, merged_at, merge_commit_sha,
   head_sha, base_sha, changed_files, additions, deletions, commits,
   updated_at.
3. Write full manifest to `experiments/reports/pr-replay-set-v1.json`.

Execution note:

- Use `merge_commit_sha` for merged-core replay pinning.
- Use `head_sha` as the frozen reference for closed-control entries.
