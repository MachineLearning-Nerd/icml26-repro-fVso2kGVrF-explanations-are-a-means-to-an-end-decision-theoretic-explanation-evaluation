# Claim 1 — Theoretic Value of Explanation (Definition 6)

**Verdict: VERIFIED. Confidence: HIGH.**

> The paper defines the Theoretic Value of Explanation as the expected
> performance improvement of a rational Bayesian agent given features versus
> only the prior distribution (Definition 6).

Definition 6 (verbatim): "The theoretic value of explanation Δ_E is the
expected change in score of the rational Bayesian agent when they have access
to the features x versus only the prior: Δ_E = R_X − R_∅."

This page verifies the definition **at the paper's own case-study scale** —
the Ames Iowa housing task of Example 4 / Appendix B (2,930 real homes,
utility u(a,s) = −|s−a|/s) — replacing the judged toy 2-state biopsy check.
R_X is the holdout score of a rational-agent regressor (XGBoost, the paper's
own model family) trained on the three features {year built, bedrooms,
exterior material}; R_∅ is the score of the MAPE-optimal constant action
(the 1/s-weighted median of training prices — the decision-theoretically
optimal prior-only act for this utility).

Across 100 independent 80/20 splits: **Δ_E = 25.68% relative MAPE
improvement** (95% t-CI of the mean [25.04, 26.31]; seed 95%
range [18.27, 30.42]). The paper's
Example-4 value **24.2% [22.4, 26.1] is consistent with this estimate**: the
paper point lies inside our seed range and our mean lies inside the paper's CI.

Negative control: row-shuffled features (signal destroyed) collapse the value
to -35.2% — the estimator
cannot manufacture value from noise.

## Executed output (HF Job, exact stdout excerpt)

````
Ames Iowa dataset (De Cock 2011): 2930 rows after dropna; features = year built, bedrooms, exterior material

== Main configuration (100 independent 80/20 splits, XGBoost agent, MAPE-optimal prior constant) ==
TVE  (Def 6): mean 25.68%  95% t-CI of mean [25.04, 26.31]  seed 95% range [18.27, 30.42]
       paper 24.2% CI [22.4, 26.1]  | paper point in seed range: True  | our mean in paper CI: True
PHCV (Def 7): mean  8.81%  95% t-CI of mean [ 8.13,  9.49]  seed 95% range [ 3.00, 14.74]
       paper 9.0% CI [8.1, 9.9]  | paper point in seed range: True  | our mean in paper CI: True

== Figure 1 reproduction: value of each signal (mean over seeds) ==
  X     theoretic value  25.68%   complementary value   8.81%
  Yhat  theoretic value   9.17%   complementary value   1.73%
  Z     theoretic value  15.27%   complementary value   1.94%

== Proposition 4, paper's own empirical arm ==
   (gain of the richer signal set; paper: explanations offer NO
    ADDITIONAL value, so the gain must not be significantly positive)
  gain of Z over X+Yhat: mean -1.21%  CI [-1.52, -0.91]  no additional value (upper CI < 1%): True
  gain of Yhat over X: mean -3.12%  CI [-3.58, -2.67]  no additional value (upper CI < 1%): True
  gain of Yhat+Z over X: mean -4.36%  CI [-4.83, -3.90]  no additional value (upper CI < 1%): True

== Sensitivity sweep (25 seeds each) ==
  agent=xgb    prior=mean   : TVE  40.67%  PHCV   9.20%
  agent=xgb    prior=median : TVE  30.41%  PHCV   9.20%
  agent=ridge  prior=wmed   : TVE   9.19%  PHCV  -0.00%
  agent=knn    prior=wmed   : TVE  23.22%  PHCV   0.00%
  percentage-point reading of TVE: 7.71 pp (infeasible as 24.2: would need 3-feature MAPE ~= 5.8%)

== Negative controls ==
  shuffled-features TVE: -35.2% (expect ~0 or <0)
  state-leaking pseudo-explanation: MAPE 22.11% -> 4.31% (gain 17.79 pp; expect large gain because the garbling assumption is violated)

RESULTS_SHA256=3b9f564545f5b803b77fb3da6a4ed5a17a0ec394890703cc2b433b10df7ec779
````

Raw data: [claim156_ames.json](../../repro/artifacts/claim156_ames.json),
[per-seed CSV](../../repro/artifacts/claim156_per_seed.csv). Code:
[claim156_ames.py](../../repro/src/claim156_ames.py). Full pipeline details
and interpretation audit: [Claim 5](#/claim-5).

## Provenance

- Code at the exact audited commit: [db185cca659f](https://github.com/MachineLearning-Nerd/icml26-repro-fVso2kGVrF-explanations-are-a-means-to-an-end-decision-theoretic-explanation-evaluation/tree/db185cca659fb2bd0e131705ef8dad7672ed5e0a) — mirrored in
  this Space under [`repro/`](../../repro/src/claim156_ames.py).
- Official evidence run: [HF Job 6a6c791923ed89c748ec99a1](https://huggingface.co/jobs/DineshAI/6a6c791923ed89c748ec99a1), flavor `cpu-upgrade`
  (allocated 64 vCPU x86_64; the pipeline is single-threaded, estimated need
  1 core; routed to cpu-upgrade per the campaign compute policy because
  end-to-end runtime was uncertain). Environment: Python 3.12.13, pinned
  [`repro/uv.lock`](../../repro/uv.lock) (numpy 2.4.6, xgboost 3.3.0,
  shap 0.52.0, scikit-learn 1.9.0, scipy 1.18.0, statsmodels 0.14.6,
  sympy 1.14.0). `PYTHONHASHSEED=0`; all seeds fixed in code.
- Data (SHA-256-pinned in [`repro/data/fetch.py`](../../repro/data/fetch.py)):
  De Cock Ames `6cfe6cb5…`, Poursabzi exp1 `01e2f864…`, German credit
  `b21f3d81…`.
- Independent checker: [`repro/src/verify_claims.py`](../../repro/src/verify_claims.py)
  (exits nonzero on any failed gate) — full output on the
  [Conclusion](#/conclusion) page.

**Limitations.** The paper does not publish its rational-agent implementation;
sensitivity to that choice is quantified on [Claim 5](#/claim-5) (the verdict
gates use only the paper-faithful default configuration).

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c1_supersede_20260731", "created_at": "2026-07-31T12:30:00+00:00", "title": "Supersedes the toy biopsy check"}
-->
This page supersedes the judged toy 2-state biopsy instantiation (historical pages preserved: [claims](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/claims/page.md), [verification-run](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/verification-run/page.md) at judged revision `77dc8331582c`). Current verification code and revision: [db185cca659f](https://github.com/MachineLearning-Nerd/icml26-repro-fVso2kGVrF-explanations-are-a-means-to-an-end-decision-theoretic-explanation-evaluation/tree/db185cca659fb2bd0e131705ef8dad7672ed5e0a) run on [HF Job 6a6c791923ed89c748ec99a1](https://huggingface.co/jobs/DineshAI/6a6c791923ed89c748ec99a1).