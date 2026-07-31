# Method

One pinned environment (uv, Python 3.12, `uv.lock` committed) and one fixed
run command (`bash run.sh`) for every experiment node. All variants live in
committed code; no env-var switches.

## Claims 1, 2, 5 — Ames case study (`src/claim156_ames.py`)

Pipeline per seed (100 independent 80/20 splits, exactly Appendix B):
1. De Cock Ames (2930 rows; 2929 after dropna on the five used columns).
2. XGBoost (defaults, `random_state=0`, `n_jobs=1`) predicting the
   overall-condition score from {year built, bedrooms, exterior material};
   SHAP `TreeExplainer` values = Z.
3. Synthetic human ŷ_H: OLS on the three features vs sale price (Eq. 10).
4. Rational agent for signal set V: XGBoost regressor (V → sale price) on the
   training split; prior-only agent plays the MAPE-optimal constant
   (1/s-weighted median). Utility u(a,s) = −|s−a|/s.
5. TVE = 100·(MAPE_prior − MAPE_X)/MAPE_prior; PHCV = 100·(MAPE_yH −
   MAPE_yH∪X)/MAPE_yH; t-distribution CIs across seeds (as in the paper's
   "t distribution" CI statement).
6. Figure-1 bars for X, Ŷ, Z (theoretic + complementary); Prop-4 empirical
   differences; sensitivity sweep (agent ∈ {xgb, ridge, knn}, prior ∈
   {weighted-median, mean, median}, pp-vs-relative reading); negative controls
   (shuffled features; state-leaking pseudo-explanation).

## Claim 4 — Proposition 4 (`src/claim4_prop4.py`)

Part A: exhaustive decision procedure — for every garbling g on |X|=3,
|Ŷ|=2, |Z|=2 (all 64), the partition of signal realizations induced by
(X,Ŷ,g(X,Ŷ)) equals that of (X,Ŷ); with sympy, the grouping procedure applied
to fully symbolic p(s,x,ŷ) and u(a,s) yields R_XYZ ≡ R_XY for every g (i.e.
for ALL priors and utilities on those alphabets). Part B: 500 random decision
problems with Fraction-valued p, u and random h, g — R_XYZ == R_XY == R_X as
exact rational equalities. Part C: negative control (state-peeking Z strictly
increases R). Empirical full-scale arm: claim156 outputs on Ames.

Derivation being verified: for deterministic Ŷ=h(X), Z=g(X,Ŷ), the map
(x,ŷ) ↦ (x,ŷ,g(x,ŷ)) is injective with the projection as inverse, so both
signal structures generate the same partition (σ-algebra); R_V depends on V
only through that partition, hence R_{X∪Ŷ∪Z} = R_{X∪Ŷ} (= R_X when Ŷ=h(X)).
This mirrors the paper's two-sided Blackwell-garbling argument.

## Claim 3 — Definition 8 (`src/claim3_behavioral.py`)

Public per-participant data of the controlled study the paper cites as its
task template (ref [48]: Poursabzi-Sangdeh et al., CHI 2021, experiment 1):
998 real participants randomized to CLEAR (model internals shown = explanation
present) vs BB (black-box) conditions on the apartment-price prediction task.
Δ_behavioral = B − B_¬E estimated with the study's own structural model
(outcome ~ explanation × num_features, worker-clustered SEs), under both the
study's u = −|s−a| and the paper's Example-4 u = −|s−a|/s. Placebo control:
permuted treatment labels.

## Claim 6 — Definition 1 + Examples 1–2 (`src/claim6_examples.py`)

Example 1 exactly as printed (exact rational arithmetic): rule threshold,
R_prior, R_signal, value of information. Example 2 at realistic scale:
GradientBoosting lender model on UCI German Credit (1000 applicants), denied
holdout applicants perform recourse search; state s = ŷ* − ŷ′, utility −s²,
explanation = SHAP importances; expected utility with vs without the
explanation.

## Compute

- Local: only short single-core interactive checks (each < 5 min).
- Official evidence run: HF Jobs `cpu-upgrade` executing `bash run.sh` at the
  pinned commit; estimated need ~1 core sequential, 5–15 min (uncertain →
  routed to cpu-upgrade per policy). Flavor, allocation and runtime recorded in
  EVAL.md.
