## Corrections Applied to CodeClue Paper

### From GPT 5.4 Review (CONFIRMED)
1. Abstract: Updated cross-model evaluation phrasing to reflect that the mean fidelity delta of 0.12 applies specifically to Arm B, not Arm A (source: experiments/cross-model-eval/results/gemini-judge-SUMMARY.json).
2. Abstract & Section 3.1 & 8: Corrected language attribution for the Express framework from TypeScript to JavaScript, updating language counts to 4 languages (source: experiments/external-repos/express/package.json).
3. Abstract & 4.3: Clarified the zero hallucination claim applies to the two consumer models (Claude and GPT 5.4) and that Gemini served exclusively as the judge (source: experiments/cross-model-eval/results/gemini-judge-SUMMARY.json).
4. Section 4.4: Corrected `clue_only` hint task counts from 13/23 to 15/23 and Mean Arm B FS to 0.61 (source: experiments/reports/v2-benchmark-all-23.json).
5. Section 4.4: Corrected `targeted_lookup` hint FS to 0.51 (source: experiments/reports/v2-benchmark-all-23.json).
6. Section 4.4: Corrected `expanded_lookup` hint task counts to 4/23 and Mean Arm B FS to 0.26 (source: experiments/reports/v2-benchmark-all-23.json).
7. Abstract & Section 8 & 4.6: Re-worded claims that cross-model evaluation blanket "confirms" findings to state it "provides partial external validation", given mixed evidence on Arm A delta and TF3 suffix replication.
8. Section 4.5: Tempered the claim that ecological validity is fully established, noting that KL divergence still requires remediation for full Sillito callback alignment.
9. Section 5/8: Reduced hyperbolic claim regarding trust validation for Tier 1 structural clues, noting this applies under the current benchmark rather than universally obviating verification.
10. Section 4.7: Explicitly scoped the Tier 2 contract evaluation, stating it was observed in a preliminary 8-file sample rather than an aggregated benchmark finding.
11. Abstract: Re-worded open-source release text so the repository URL is framed as forthcoming for camera-ready, dropping unverifiable assertions of instantaneous release.

### From Gemini Meta-Review (additional)
None. All factual and logical errors were properly scoped by the GPT 5.4 review, and its corrections comprehensively resolved the issues found in the draft.

### DISPUTED (not applied)
None. All of GPT 5.4's findings were empirically validated by analyzing the underlying JSON/results logs.

### Summary
- Total corrections from GPT: 11 confirmed, 0 disputed, 0 partial
- Additional corrections from Gemini: 0
- Paper version: final (ready for arXiv)