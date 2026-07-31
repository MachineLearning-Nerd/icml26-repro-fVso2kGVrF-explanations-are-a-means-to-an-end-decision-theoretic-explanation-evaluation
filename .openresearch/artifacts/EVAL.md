# EVAL — official evidence run

- Commit: `9561782baf73bb3e261090dc69263306f7f4f7fa` (baseline, frozen by this run)
- Compute: HF Jobs `cpu-upgrade`, job `6a6c745bb36a6516e96a3cba`
  (https://huggingface.co/jobs/DineshAI/6a6c745bb36a6516e96a3cba).
  Estimated need: 1 core, sequential, uncertain runtime → routed to
  cpu-upgrade per policy. Allocated: 64 vCPU x86_64. Runtime: 4m50.7s wall
  (6m49.8s user). Local Apple-silicon runs reproduce identical printed values.
- Command: `bash run.sh` (fixed contract; env `uv sync --frozen`,
  Python 3.12.13, PYTHONHASHSEED=0).

## Results (job stdout, authoritative)

- Claims 1/2/5 (Ames, 100 splits): TVE 25.68% (t-CI [25.04, 26.31], seed range
  [18.27, 30.42]) vs paper 24.2 [22.4, 26.1] — consistent both ways.
  PHCV 8.81% (t-CI [8.13, 9.49]) vs paper 9 [8.1, 9.9] — consistent.
  Figure-1 ordering reproduced. RESULTS_SHA256
  `56947dbd226a6f3d543c730efa52ae0b4d84c5992dd856473c0d91cf4aa1202b`.
- Claim 4 (Prop 4): 64/64 garblings partition identity + symbolic all-(p,u)
  R-equality; 500/500 exact-rational equalities; negative control strict
  increase. RESULTS_SHA256
  `813df8a87b4fb3449c2eb66d6426459e557e8abab570ff48127c2b3ee32fffce`.
- Claim 6: Example 1 exact (rule ⇔ q>9/10; VoI = 9/4); Example 2 German
  Credit recourse gain +0.00253. RESULTS_SHA256
  `9af6871bca759ec01790871972e08c3335cbf287dc22ace811c79224cfabf82c`.
- Claim 3 (Def 8, real study): Δ_behavioral −0.78 MAPE pp CI [−1.65, +0.09]
  (u = APE), −7.17 $k CI [−16.50, +2.16] (u = abs err); placebo CI covers 0.
  RESULTS_SHA256
  `ccf7d3fd7e70c0bfedd498d973bbcca2db9b0c6a617528d46afeb26f06071c82`.
- Independent checker: 19/19 gates PASS (`VERDICT: ALL CLAIM CONTRACTS PASS`).

## Non-circularity note

The relative-improvement reading of "24.2% in MAPE" was fixed from a
feasibility bound before the final runs (see source_audit.md §Interpretation):
no data, sample size, tolerance, or model family was selected from the target
numbers — all pipeline choices are the paper's stated ones or documented
decision-theoretic defaults, and the sensitivity sweep reports the
alternatives. Negative controls fail for the intended reasons (shuffled
features destroy value; a non-garbling explanation restores it).

## Limitations

Recorded per claim on the Space pages; principal ones: Ames variant/split-seed
underspecified (per-seed distribution published); rational-agent regressor
unspecified (sensitivity published); Definition 8 instantiated on the paper's
cited controlled study (the paper itself collected no human data).
