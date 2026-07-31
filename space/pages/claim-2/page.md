# Claim 2 — Potential Human-Complementary Value (Definition 7)

**Verdict: VERIFIED. Confidence: HIGH.**

> The paper defines Potential Human-Complementary Value as the expected
> improvement when a rational agent has both human predictions and features
> versus human predictions alone (Definition 7).

Definition 7 (verbatim): "Δ_E_compl is the expected improvement in the
performance of the rational Bayesian agent when they have access to the human
prediction Ŷ_H and features X for each instance versus when they lack access
to X: Δ_E_compl = R_{Ŷ_H ∪ X} − R_{Ŷ_H}."

Verified at the paper's case-study scale (Ames, Example 5 / Appendix B) with
the paper's own synthetic-human model (Eq. 10: OLS on the three features fit
to training sale prices). R_{Ŷ_H} is the score of the rational agent given
only the human prediction; R_{Ŷ_H ∪ X} adds the three features.

Across 100 independent 80/20 splits: **Δ_E_compl = 8.81% relative
MAPE improvement** (95% t-CI [8.13, 9.49]; seed 95%
range [3.0, 14.74]). The paper's
Example-5 value **9% [8.1, 9.9] is consistent**: paper point inside our seed
range, our mean inside the paper CI — and our t-CI is nearly nested in the
paper's interval.

As the paper argues, Δ_E_compl (8.81%) is far below Δ_E
(25.68%): the human predictions already carry most of the feature
information, so the *complementary* room for explanations is much smaller
than the unconditioned theoretic value.

## Executed output (HF Job, exact stdout excerpt)

````
Ames Iowa dataset (De Cock 2011): 2930 rows after dropna; features = year built, bedrooms, exterior material

== Main configuration (100 independent 80/20 splits, XGBoost agent, MAPE-optimal prior constant) ==
TVE  (Def 6): mean 25.68%  95% t-CI of mean [25.04, 26.31]  seed 95% range [18.27, 30.42]
       paper 24.2% CI [22.4, 26.1]  | paper point in seed range: True  | our mean in paper CI: True
PHCV (Def 7): mean  8.81%  95% t-CI of mean [ 8.13,  9.49]  seed 95% range [ 3.00, 14.74]
       paper 9.0% CI [8.1, 9.9]  | paper point in seed range: True  | our mean in paper CI: True
````

(The full block including Figure-1 values appears on [Claim 5](#/claim-5).)

Raw data: [claim156_ames.json](../../repro/artifacts/claim156_ames.json),
[per-seed CSV](../../repro/artifacts/claim156_per_seed.csv). Code:
[claim156_ames.py](../../repro/src/claim156_ames.py).

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

**Limitations.** Same operationalization sensitivity as Claim 1, quantified on
[Claim 5](#/claim-5); with linear or k-NN agents Δ_E_compl shrinks toward 0
because those agents cannot extract nonlinear feature information beyond the
linear human signal — the paper's XGBoost family is the faithful choice.
