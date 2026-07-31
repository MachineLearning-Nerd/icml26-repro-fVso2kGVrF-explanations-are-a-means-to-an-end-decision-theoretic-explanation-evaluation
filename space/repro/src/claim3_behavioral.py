"""Claim 3 / Definition 8: the Behavioral Value of Explanation as the MEASURED
treatment effect of explanation access on REAL human decision-makers in a
controlled study.

The paper itself runs no human-subject study (its Appendix B uses synthetic
humans), so we instantiate Definition 8 exactly on the public per-participant
data of the controlled house-pricing experiment the paper cites as its task
template: Poursabzi-Sangdeh et al., "Manipulating and Measuring Model
Interpretability", CHI 2021 (paper's reference [48]), experiment 1.

Mapping onto Definition 8:
  - Decision problem: predict an apartment's sale price (action a in $M),
    state s = actual price, utility u(a, s) = -|s - a| (their measure) and
    u(a, s) = -|s - a|/s (the paper's Example-4 APE utility).
  - v with explanation      = {x, yhat, z}: CLEAR conditions, where the model's
    internals (coefficients) are shown -> explanation z present.
  - v without explanation   = {x, yhat}: BB (black-box) conditions, identical
    except no model internals.
  - Random assignment of workers to conditions -> controlled comparison.
  - Delta_behavioral = B - B_notE, isolated per Definition 8 with a structural
    multiple regression (transparency * num_features, worker-clustered SEs),
    matching the study's own lmer specification.

Filters follow the study's analysis code: first 10 questions, primary four
conditions (CLEAR-2, CLEAR-8, BB-2, BB-8), synthetic apartment (actual = -1)
excluded.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ART, REPO, results_sha  # noqa: E402

sys.path.insert(0, str(REPO / "data"))
from fetch import fetch  # noqa: E402

COND = {"C1": "CLEAR-2", "C3": "CLEAR-8", "C0": "BB-2", "C2": "BB-8",
        "C4": "NO-MODEL"}


def load():
    df = pd.read_csv(fetch("poursabzi_exp1.csv"))
    df["condition"] = df["condition"].map(COND)
    df = df[df["q_id"] < 10]
    df = df[df["condition"] != "NO-MODEL"]
    df = df[df["actual_price"] > 0]  # drop the synthetic apartment (-1)
    df["explanation"] = (df["condition"].str.startswith("CLEAR")).astype(int)
    df["num_features"] = np.where(df["condition"].str.endswith("8"), 8, 2)
    df["abs_err"] = (df["final_pred"] - df["actual_price"]).abs()
    df["ape"] = df["abs_err"] / df["actual_price"]
    return df


def treatment_effect(df, outcome):
    """Delta_behavioral = B - B_notE = E[u | explanation] - E[u | no expl.];
    with u = -outcome, this equals mean(outcome | no expl) - mean(outcome | expl).
    Isolated with the study's structural model, worker-clustered SEs."""
    m = smf.ols(f"{outcome} ~ explanation * C(num_features)", data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df["worker_id"]})
    # marginal effect of explanation averaged over the feature-count factor
    w8 = (df["num_features"] == 8).mean()
    eff = m.params["explanation"] + w8 * m.params["explanation:C(num_features)[T.8]"]
    cov = m.cov_params()
    var = (cov.loc["explanation", "explanation"]
           + w8 ** 2 * cov.loc["explanation:C(num_features)[T.8]",
                               "explanation:C(num_features)[T.8]"]
           + 2 * w8 * cov.loc["explanation", "explanation:C(num_features)[T.8]"])
    se = float(np.sqrt(var))
    delta = -float(eff)  # utility = -error, so improvement = -effect on error
    return delta, 1.96 * se, m


def main():
    df = load()
    n_workers = df["worker_id"].nunique()
    print(f"Poursabzi-Sangdeh et al. (CHI 2021) experiment 1: "
          f"{len(df)} decisions by {n_workers} real human participants, "
          f"randomized to explanation (CLEAR) vs no-explanation (BB)")
    for c in ["CLEAR-2", "CLEAR-8", "BB-2", "BB-8"]:
        sub = df[df["condition"] == c]
        print(f"  {c:8s}: {sub['worker_id'].nunique():4d} workers, "
              f"mean |err| ${1e3 * sub['abs_err'].mean():6.1f}k, "
              f"MAPE {100 * sub['ape'].mean():5.1f}%")

    out = {"n_decisions": int(len(df)), "n_workers": int(n_workers)}
    print("\n== Definition 8: Delta_behavioral = B - B_notE "
          "(positive = explanations helped) ==")
    for outcome, label, scale in [("abs_err", "u = -|s-a| ($k)", 1e3),
                                  ("ape", "u = -|s-a|/s (MAPE pp)", 100)]:
        delta, half, m = treatment_effect(df, outcome)
        lo, hi = scale * (delta - half), scale * (delta + half)
        sig = not (lo <= 0 <= hi)
        print(f"  {label}: Delta = {scale * delta:+.2f}  95% CI [{lo:+.2f}, {hi:+.2f}]"
              f"  -> {'significant' if sig else 'NOT significant (CI covers 0)'}")
        out[outcome] = {"delta": round(scale * delta, 3),
                        "ci": [round(lo, 3), round(hi, 3)],
                        "significant": bool(sig)}

    # Negative control: a placebo "treatment" that permutes the explanation
    # label within condition-pairs must show ~0 effect.
    rng = np.random.default_rng(0)
    dfp = df.copy()
    dfp["explanation"] = rng.permutation(dfp["explanation"].values)
    delta, half, _ = treatment_effect(dfp, "ape")
    print(f"\nNegative control (permuted treatment labels): "
          f"Delta = {100 * delta:+.2f} pp, CI [{100 * (delta - half):+.2f}, "
          f"{100 * (delta + half):+.2f}] (must cover 0: "
          f"{bool(100 * (delta - half) <= 0 <= 100 * (delta + half))})")
    out["placebo"] = {"delta": round(100 * delta, 3),
                      "ci": [round(100 * (delta - half), 3),
                             round(100 * (delta + half), 3)]}

    ART.mkdir(parents=True, exist_ok=True)
    (ART / "claim3_behavioral.json").write_text(json.dumps(out, indent=1))
    print(f"\nRESULTS_SHA256={results_sha(out)}")


if __name__ == "__main__":
    main()
