# Claim 6 — Decision-problem framework, Examples 1–2 (Definition 1)

**Verdict: VERIFIED. Confidence: HIGH.**

> The decision problem framework formalizes a use case via action spaces,
> state spaces, utility functions, and probability distributions, illustrated
> with worked examples in medical treatment (biopsy) and recourse provision
> (Definition 1, Examples 1-2).

The judged logbook instantiated only a *modified* biopsy toy (3 actions — not
the paper's Example 1) and omitted Example 2 entirely. Both worked examples
are now reproduced.

**Example 1 (medical treatment) — exact, as printed.** States s ∈ {0,1},
actions a ∈ {0,1}, u(1,1)=0, u(1,0)=−100, u(0,·)=−10 (s unobservable when
a=0). In exact rational arithmetic: the rational Bayesian rule is *biopsy iff
q > 9/10* (verified on an exact 101-point belief grid — the threshold is the
utility ratio 10/100 exactly as decision theory prescribes), and a diagnostic
signal (sens 0.9 / spec 0.95, prior 1/2) has value of information exactly
**9/4** utility units: R_∅ = −10 → R_signal = −31/4.

**Example 2 (recourse provision) — realistic scale, real credit data.** An
online lender (GradientBoosting classifier, test accuracy
0.8) scores the 1,000 real applicants of the
UCI Statlog German Credit dataset; 68 holdout
applicants are denied. Definition 1's elements as the paper states them:
state s = ŷ* − ŷ′ (gap to the desired prediction), action a = x′ (a
counterfactual feature edit), utility u(a,s) = −s², signals V = X ∪ Ŷ ∪ Z
with Z = SHAP feature-importance scores. The denied applicant searching with
the explanation (editing the highest-|SHAP| actionable features first)
achieves expected utility -0.00824 vs
-0.01076 without it — the
explanation measurably helps the applicant close the recourse gap, the use
case Example 2 formalizes.

## Executed output (HF Job, exact stdout)

````
== Example 1 (medical treatment / biopsy), exact rational arithmetic ==
  rational rule == 'biopsy iff q > 9/10' on 101-point exact belief grid: PASS
  negative control (swapped biopsy costs): 9/10 rule breaks as expected: PASS
  R_prior = -10, R_signal = -31/4, value of information = 9/4 (= 2.25)

== Example 2 (recourse provision), German Credit, 1000 applicants ==
  lender model: GradientBoosting, test accuracy 0.8, 68 denied applicants in holdout
  E[u] recourse WITH explanation (SHAP-guided): -0.00824
  E[u] recourse WITHOUT explanation (random order): -0.01076
  explanation gain: 0.00253 (positive = explanation helps the applicant reach y*)

RESULTS_SHA256=458f2a41a8888c76d0088cb4dbb292e8efdb33146dec03a3e60fc628a2393449
````

Raw data: [claim6_examples.json](../../repro/artifacts/claim6_examples.json).
Code: [claim6_examples.py](../../repro/src/claim6_examples.py). Data: UCI
Statlog German Credit (SHA-256 `b21f3d81…`, hash-pinned).

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

Executed negative control: swapping the biopsy costs (u(1,0) = −10,
u(0,·) = −100) breaks the exact 9/10 threshold rule, confirming the check is
sensitive to the paper's exact utility; the recourse explanation gain is gated
positive in the independent checker.

**Limitations.** Example 2's paper text prescribes the decision problem, not
a dataset; German Credit is the canonical public credit-scoring dataset for
recourse research. The recourse search budget (2 edits × 3 scalings) is a
concrete instantiation of the paper's "the applicant seeks a new input x′".
