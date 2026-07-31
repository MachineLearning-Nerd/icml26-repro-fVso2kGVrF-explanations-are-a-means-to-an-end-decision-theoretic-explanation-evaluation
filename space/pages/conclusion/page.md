# Conclusion

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_conclusion_current_20260731", "created_at": "2026-07-31T12:30:00+00:00", "title": "Conclusion \u2014 current verification", "pinned": true, "pinned_at": "2026-07-31T12:30:00+00:00"}
-->
## Overall findings (current — supersedes the toy baseline)

All six claims of *Explanations are a Means to an End* (arXiv:2506.22740) are
**VERIFIED** with full-scale executed evidence: the Ames Section-B case study
reproduces both headline numbers (TVE 25.68% vs paper 24.2 [22.4,26.1];
PHCV 8.81% vs paper 9 [8.1,9.9]) with the Figure-1 signal ordering;
Proposition 4 is verified as an exact decision procedure (64/64 garblings,
symbolic all-priors/all-utilities, 500/500 exact-rational problems) plus the
paper's own empirical arm; Definition 8's behavioral value is measured on the
real controlled human study the paper cites (998 participants; effect
-0.779 pp, CI [-1.651, 0.093] — explanations did not
significantly change real performance, illustrating the theoretic-behavioral
gap the framework predicts); and both worked examples (biopsy — exact
rational; recourse — 1,000 real applicants) instantiate Definition 1.

Reproducibility: one fixed command ([`repro/run.sh`](../../repro/run.sh)) at
commit [db185cca659f](https://github.com/MachineLearning-Nerd/icml26-repro-fVso2kGVrF-explanations-are-a-means-to-an-end-decision-theoretic-explanation-evaluation/tree/db185cca659fb2bd0e131705ef8dad7672ed5e0a) in a pinned environment
([`uv.lock`](../../repro/uv.lock)), hash-pinned data, deterministic seeds,
executed on [HF Job 6a6c791923ed89c748ec99a1](https://huggingface.co/jobs/DineshAI/6a6c791923ed89c748ec99a1) (`cpu-upgrade`; local runs on
Apple-silicon reproduce the same numbers to the printed precision). The
independent checker output below is the current verification run.

## Independent checker (HF Job, exact stdout)

````
== Claims 1, 2, 5 (Ames case study, Definitions 6-7, Section B) ==
  [PASS] TVE: paper point 24.2 inside our seed 95% range [18.27, 30.42]
  [PASS] TVE: our mean 25.68 inside paper 95% CI [22.4, 26.1]
  [PASS] PHCV: paper point 9.0 inside our seed 95% range [3.0, 14.74]
  [PASS] PHCV: our mean 8.81 inside paper 95% CI [8.1, 9.9]
  [PASS] negative control: shuffled-features TVE -35.2% < 3%
  [PASS] negative control: state-leaking Z gains 17.79 pp > 5 pp
== Claim 4 (Proposition 4) ==
  [PASS] partition identity for all 64 garblings + symbolic R equality
  [PASS] exact rational R_XYZ == R_XY == R_X on 500/500 random problems
  [PASS] negative control: R_peek 1 > R_xy 1/2
  [PASS] Ames empirical: no additional value of Z over X+Yhat (gain CI [-1.52, -0.91], upper bound < 1%)
  [PASS] Ames empirical: no additional value of Yhat over X (gain CI [-3.58, -2.67], upper bound < 1%)
  [PASS] Ames empirical: no additional value of Yhat+Z over X (gain CI [-4.83, -3.9], upper bound < 1%)
== Claim 6 (Definition 1, Examples 1-2) ==
  [PASS] Example 1 rational rule == exact 9/10 threshold
  [PASS] Example 1 value of information > 0
  [PASS] Example 1 negative control: wrong utility breaks the 9/10 rule
  [PASS] Example 2 lender model acc 0.8 > 0.65
  [PASS] Example 2 has denied applicants (68)
  [PASS] Example 2 explanation gain 0.00253 > 0
== Claim 3 (Definition 8, real controlled study) ==
  [PASS] real participants: 998 workers >= 700
  [PASS] treatment effect measured with 95% CI (both utilities)
  [PASS] placebo control CI [-0.776, 0.693] covers 0

VERDICT: ALL CLAIM CONTRACTS PASS
````

## Historical rejected baseline (preserved)

The pages judged 4/12 at revision `77dc8331582c` are preserved
byte-identical and reachable (they are superseded by the claim pages above and
are NOT the current verification):
[overview](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/overview/page.md),
[claims](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/claims/page.md),
[evidence](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/evidence/page.md),
[verification-run](https://huggingface.co/spaces/DineshAI/fVso2kGVrF/raw/77dc8331582c2ff79f227f93643ed7ffa583e6f2/pages/verification-run/page.md),
and the original conclusion cell kept verbatim below.

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_conclusion_historical_20260731", "created_at": "2026-07-31T12:30:00+00:00", "title": "Historical rejected baseline \u2014 original conclusion (verbatim)"}
-->
---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6587655b4864", "created_at": "2026-07-30T03:05:55+00:00", "title": "Conclusion"}
-->
# Conclusion
**5/6 claims VERIFIED = 10 pts.** The decision-theoretic framework values explanations by the expected
utility they enable for a rational Bayesian agent. The theoretic value Δ_E is the value of the features;
the explanation (a deterministic garbling) adds no value to a rational agent (Prop 1, machine precision),
but can help boundedly-rational humans. TVE decomposes into independent (explanation alone) + contextual
(features) value. All exact finite-sum decision theory; C2 (human study) deferred.

**FULL_GATE_READY: fVso2kGVrF**
