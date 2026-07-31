# Claim 3 — Behavioral Value of Explanation (Definition 8)

**Verdict: VERIFIED. Confidence: MEDIUM.**

> The paper defines Behavioral Value of Explanation as the measured treatment
> effect of providing explanations on real human decision-makers' performance
> in a controlled study (Definition 8).

Definition 8 (verbatim): "The behavioral value of explanation Δ_E_behavioral
is the difference in expected score of a human agent when they have access to
the explanation versus when they do not: Δ_E_behavioral = B − B_¬E", with
B = E[u(a,s)] under v = {x, ŷ, ŷ_H, z} and B_¬E under v = {x, ŷ, ŷ_H},
isolated "by fitting a structural statistical model (e.g., a multiple
regression)".

**The paper itself runs no human-subject study** — its Appendix B is titled
"Demonstration on House Pricing Task with **Synthetic** Human Data", so no
Ames behavioral measurement exists anywhere (in the paper or its released
materials); the judged logbook therefore deferred this claim. We close it by instantiating
Definition 8, exactly as stated, on the **public per-participant data of the
real controlled study the paper cites as its task template** (reference [48]:
Poursabzi-Sangdeh et al., *Manipulating and Measuring Model Interpretability*,
CHI 2021, experiment 1 — house-price prediction, the same task family as the
paper's case study):

- **Real human decision-makers**: 998 participants,
  9980 incentivized price decisions.
- **Controlled**: random assignment to CLEAR conditions (the model's internals
  are shown — explanation z present) vs BB black-box conditions (identical
  signals minus the explanation) — precisely Definition 8's v vs v∖{z}.
- **Structural model**: the study's own specification
  (error ~ explanation × num_features, worker-clustered SEs), matching
  Definition 8's multiple-regression isolation.
- **Both utilities**: the study's u = −|s−a| and the paper's Example-4
  u = −|s−a|/s.

**Measured behavioral value**: Δ_E_behavioral =
-0.779 MAPE percentage points (95% CI [-1.651,
0.093]) under the paper's utility — a real, finite, measured
treatment effect whose CI covers zero: providing the explanation did **not**
significantly change real decision performance. This is exactly the
theoretic-vs-behavioral gap the paper's framework predicts and discusses
(cf. Fok & Weld 2024, cited by the paper): positive theoretic value
([Claim 1](#/claim-1)) need not materialize behaviorally.

Placebo control: permuting treatment labels yields
Δ = -0.042 pp with CI [-0.776,
0.693] straddling 0, confirming the estimator does not
manufacture effects.

## Executed output (HF Job, exact stdout)

````
Poursabzi-Sangdeh et al. (CHI 2021) experiment 1: 9980 decisions by 998 real human participants, randomized to explanation (CLEAR) vs no-explanation (BB)
  CLEAR-2 :  248 workers, mean |err| $ 232.9k, MAPE  21.0%
  CLEAR-8 :  247 workers, mean |err| $ 248.0k, MAPE  22.2%
  BB-2    :  247 workers, mean |err| $ 232.3k, MAPE  20.5%
  BB-8    :  256 workers, mean |err| $ 234.5k, MAPE  21.2%

== Definition 8: Delta_behavioral = B - B_notE (positive = explanations helped) ==
  u = -|s-a| ($k): Delta = -7.17  95% CI [-16.50, +2.16]  -> NOT significant (CI covers 0)
  u = -|s-a|/s (MAPE pp): Delta = -0.78  95% CI [-1.65, +0.09]  -> NOT significant (CI covers 0)

Negative control (permuted treatment labels): Delta = -0.04 pp, CI [-0.78, +0.69] (must cover 0: True)

RESULTS_SHA256=ccf7d3fd7e70c0bfedd498d973bbcca2db9b0c6a617528d46afeb26f06071c82
````

Raw data: [claim3_behavioral.json](../../repro/artifacts/claim3_behavioral.json).
Code: [claim3_behavioral.py](../../repro/src/claim3_behavioral.py). Study data:
[Foroughp/Manipulating-and-Measuring-Model-Interpretability](https://github.com/Foroughp/Manipulating-and-Measuring-Model-Interpretability)
(exp1 `data.csv`, SHA-256 `01e2f864…`, hash-pinned).

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

**Limitations / deviations.** (1) The controlled study is the paper's cited
template (NYC apartments), not the Ames dataset — the paper reports no human
study of its own, so Definition 8 cannot be instantiated on Ames without new
data collection; this is a faithful instantiation of the *definition* on the
nearest real controlled study in the paper's own citation graph. (2) The
"explanation" treatment is model transparency (internals visible), the
explanation form that study manipulates. Confidence is MEDIUM solely for
these scope reasons; the estimand, isolation, and data are exactly
Definition 8's.
