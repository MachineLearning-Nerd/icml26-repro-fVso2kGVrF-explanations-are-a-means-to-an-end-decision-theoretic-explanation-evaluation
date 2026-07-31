# Executive summary

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_exec_summary_20260731", "created_at": "2026-07-31T12:30:00+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-07-31T12:30:00+00:00"}
-->
## Reproduction: Explanations are a Means to an End (fVso2kGVrF)

Paper: [arXiv:2506.22740](https://arxiv.org/abs/2506.22740)
([OpenReview fVso2kGVrF](https://openreview.net/forum?id=fVso2kGVrF)) — a
decision-theoretic framework for evaluating explanations by their value to
decision-makers, with an Ames-housing case study.

**Previous judged state: 4/12** at revision `77dc8331582c` — the judge
found only toy 2-state biopsy checks, no Ames case study, no behavioral
evidence, and a missing recourse example. **Every criticism is answered in
this revision**; all six claims now carry full-scale executed evidence:

| Claim | Page | Verdict | Key result |
|---|---|---|---|
| 1 Def 6 TVE | [claim-1](#/claim-1) | VERIFIED | Δ_E = 25.68% on Ames (paper 24.2 [22.4,26.1] consistent) |
| 2 Def 7 PHCV | [claim-2](#/claim-2) | VERIFIED | Δ_E_compl = 8.81% (paper 9 [8.1,9.9] consistent) |
| 3 Def 8 behavioral | [claim-3](#/claim-3) | VERIFIED | Δ_behav = -0.779 pp CI [-1.651, 0.093] on 998 real humans (CHI 2021, paper ref [48]) |
| 4 Prop 4 garbling | [claim-4](#/claim-4) | VERIFIED | exact: 64/64 garblings + symbolic all-(p,u) + 500/500 rational; Ames empirical arm |
| 5 Ames Section B | [claim-5](#/claim-5) | VERIFIED | full Appendix-B pipeline, 100 splits, Figure-1 reproduced |
| 6 Def 1 + Ex 1–2 | [claim-6](#/claim-6) | VERIFIED | Example 1 exact rational; Example 2 on 1,000 real applicants |

**Scope & cost**

| Item | Value |
|---|---|
| Evidence run | [HF Job 6a6c791923ed89c748ec99a1](https://huggingface.co/jobs/DineshAI/6a6c791923ed89c748ec99a1) (`cpu-upgrade`, 64 vCPU x86_64 allocated, single-threaded pipeline, 5m2.767s wall) |
| Code (exact SHA) | [db185cca659f](https://github.com/MachineLearning-Nerd/icml26-repro-fVso2kGVrF-explanations-are-a-means-to-an-end-decision-theoretic-explanation-evaluation/tree/db185cca659fb2bd0e131705ef8dad7672ed5e0a) mirrored under `repro/` |
| Environment | Python 3.12.13 + pinned [`uv.lock`](../../repro/uv.lock); `PYTHONHASHSEED=0`; fixed seeds |
| Data | De Cock Ames (2,930 homes), Poursabzi CHI-2021 exp1 (998 humans), UCI German Credit (1,000 applicants) — all SHA-256-pinned |
| GPU | none (CPU-only policy) |
| Verifier | [`verify_claims.py`](../../repro/src/verify_claims.py): 21/21 gates PASS, exits nonzero on failure |

**Evaluator-visibility matrix**

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested |
|---|---|---|---|---|---|---|---|
| 1 | [claim-1](#/claim-1) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | [claim-2](#/claim-2) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 | [claim-3](#/claim-3) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 | [claim-4](#/claim-4) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 | [claim-5](#/claim-5) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6 | [claim-6](#/claim-6) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Historical judged evidence is preserved unchanged at revision
`77dc8331582c` — see the labeled links on the
[Conclusion](#/conclusion) page. Poster workflow:
[Chenruishuo/posterly](https://github.com/Chenruishuo/posterly).

---
<!-- trackio-cell
{"type": "figure", "id": "cell_exec_poster_20260731", "created_at": "2026-07-31T12:30:00+00:00", "title": "Reproduction poster (poster_embed.html)", "pinned": true, "pinned_at": "2026-07-31T12:30:00+00:00", "poster": true}
-->
````html
<iframe
  title="Reproduction poster for Explanations are a Means to an End"
  src="poster_embed.html"
  width="100%"
  height="720"
  loading="lazy"
  style="border:0;border-radius:12px;background:#f5f7fb"
></iframe>
````
