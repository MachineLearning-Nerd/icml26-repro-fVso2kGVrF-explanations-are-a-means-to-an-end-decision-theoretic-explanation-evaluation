# Reproduction: Explanations are a Means to an End (fVso2kGVrF)

Reproduction campaign for arXiv:2506.22740 (ICML 2026 agent-repro challenge,
OpenReview `fVso2kGVrF`). Evaluator-visible evidence lives in the Hugging Face
Space [DineshAI/fVso2kGVrF](https://huggingface.co/spaces/DineshAI/fVso2kGVrF);
this repository is the mirrored source of the pipeline that generated it.

## Layout

- `run.sh` — fixed reproduction command: fetches hash-pinned data, runs every
  claim experiment, then the independent verifier (nonzero exit on any failed
  claim contract).
- `data/fetch.py` — SHA-256-pinned downloads (Ames/De Cock, Poursabzi-Sangdeh
  CHI 2021 exp1, UCI German Credit).
- `src/claim156_ames.py` — Ames case study (Definitions 6–7, Section B
  numbers, Figure 1, Prop-4 empirical arm, sensitivity, negative controls).
- `src/claim4_prop4.py` — Proposition 4: exhaustive partition decision
  procedure + fully symbolic R-equality + exact-rational checks + negative
  control.
- `src/claim3_behavioral.py` — Definition 8 on the real controlled study the
  paper cites (ref [48]), 998 human participants.
- `src/claim6_examples.py` — Example 1 (exact rational) + Example 2 (recourse
  on German Credit).
- `src/verify_claims.py` — independent checker over the JSON artifacts.
- `.openresearch/artifacts/` — claim contracts, source audit, method, raw
  outputs, logs.

## Environment

`uv sync --frozen` (Python 3.12, pinned `uv.lock`), then `bash run.sh`.
Official evidence runs execute on Hugging Face Jobs (`cpu-upgrade` flavor) at a
pinned commit of this repository.
