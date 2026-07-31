#!/usr/bin/env bash
# Fixed baseline reproduction command. Runs every claim experiment and the
# independent verifier; writes raw artifacts + logs under .openresearch/artifacts/.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONHASHSEED=0
mkdir -p .openresearch/artifacts/logs
PY=.venv/bin/python
[ -x "$PY" ] || { uv sync --frozen; }

$PY data/fetch.py                 2>&1 | tee .openresearch/artifacts/logs/fetch.log
$PY src/claim156_ames.py          2>&1 | tee .openresearch/artifacts/logs/claim156_ames.log
$PY src/claim4_prop4.py           2>&1 | tee .openresearch/artifacts/logs/claim4_prop4.log
$PY src/claim6_examples.py        2>&1 | tee .openresearch/artifacts/logs/claim6_examples.log
$PY src/claim3_behavioral.py      2>&1 | tee .openresearch/artifacts/logs/claim3_behavioral.log
$PY src/verify_claims.py          2>&1 | tee .openresearch/artifacts/logs/verify.log

# Emit raw artifacts to stdout so remote (HF Jobs) runs return them in the log.
for f in .openresearch/artifacts/*.json .openresearch/artifacts/*.csv; do
  echo "===ARTIFACT $f==="
  cat "$f"
done
echo "===ARTIFACT-END==="
