"""Claim 6: the decision-problem framework (Definition 1) with BOTH worked
examples: Example 1 (medical treatment / biopsy) and Example 2 (recourse
provision).

Example 1 is reproduced EXACTLY as stated (2 states, 2 actions, utilities
0 / -100 / -10, s unobservable when a = 0) in exact rational arithmetic:
the rational decision rule, its threshold, and the value of information of a
diagnostic signal.

Example 2 is instantiated at realistic scale on the UCI Statlog German Credit
dataset (1000 real credit applicants): an online lender's classifier denies
applicants; a denied applicant seeks a counterfactual x' with the desired
prediction, with state s = yhat* - yhat', utility u(a, s) = -s^2, and signals
V = X u Yhat u Z with Z = feature-importance scores.  We measure the expected
utility of recourse search guided by the explanation versus without it.
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ART, REPO, results_sha  # noqa: E402

sys.path.insert(0, str(REPO / "data"))
from fetch import fetch  # noqa: E402


def example1():
    """Exact instantiation of Example 1 (Definition 1 elements + rational rule).

    u(1, s=1) = 0, u(1, s=0) = -100, u(0, .) = -10  (s unobservable when a=0,
    so E[u(0)] = -10 for every belief).  Rational rule: biopsy iff
    -100 (1 - q) > -10  <=>  q > 9/10, q = posterior P(s=1).
    """
    u = {(1, 1): Fraction(0), (1, 0): Fraction(-100),
         (0, 1): Fraction(-10), (0, 0): Fraction(-10)}
    threshold = Fraction(9, 10)

    def best_action(q):
        eu1 = q * u[(1, 1)] + (1 - q) * u[(1, 0)]
        eu0 = Fraction(-10)
        return (1, eu1) if eu1 > eu0 else (0, eu0)

    # decision rule check on an exact grid of beliefs
    grid = [Fraction(k, 100) for k in range(101)]
    rule_ok = all((best_action(q)[0] == 1) == (q > threshold) for q in grid)

    # negative control: with the wrong utility (biopsy costs swapped:
    # u(1,0) = -10, u(0,.) = -100) the 9/10 threshold must NOT hold.
    def best_action_wrong(q):
        eu1 = q * Fraction(0) + (1 - q) * Fraction(-10)
        return 1 if eu1 > Fraction(-100) else 0

    wrong_fails = not all((best_action_wrong(q) == 1) == (q > threshold)
                          for q in grid)

    # value of information of a diagnostic signal (sensitivity 0.9,
    # specificity 0.95) at prior pi = 1/2, exact rational arithmetic
    pi = Fraction(1, 2)
    sens, spec = Fraction(9, 10), Fraction(19, 20)
    R_prior = best_action(pi)[1]
    R_signal = Fraction(0)
    for t in (0, 1):  # test outcome
        p_t_s1 = sens if t == 1 else 1 - sens
        p_t_s0 = (1 - spec) if t == 1 else spec
        p_t = pi * p_t_s1 + (1 - pi) * p_t_s0
        q = pi * p_t_s1 / p_t
        R_signal += p_t * best_action(q)[1]
    voi = R_signal - R_prior
    return {"rule_matches_threshold_9_10": rule_ok,
            "wrong_utility_rule_fails": wrong_fails,
            "R_prior": str(R_prior), "R_signal": str(R_signal),
            "value_of_information": str(voi),
            "voi_float": round(float(voi), 4)}


GERMAN_COLS = [
    "status", "duration", "credit_history", "purpose", "amount", "savings",
    "employment", "installment_rate", "personal_status", "debtors",
    "residence", "property", "age", "other_plans", "housing", "existing",
    "job", "liable", "telephone", "foreign", "target",
]
NUMERIC = ["duration", "amount", "installment_rate", "residence", "age",
           "existing", "liable"]
# features an applicant can actually change (actionable recourse dimensions)
ACTIONABLE = ["duration", "amount", "savings_code"]


def example2(seed=0):
    df = pd.read_csv(fetch("german.data"), sep=" ", header=None,
                     names=GERMAN_COLS)
    df["target"] = (df["target"] == 1).astype(int)  # 1 = good credit
    for c in GERMAN_COLS:
        if c not in NUMERIC and c != "target":
            df[c + "_code"] = df[c].astype("category").cat.codes
    feats = NUMERIC + [c for c in df.columns if c.endswith("_code")]
    X = df[feats].to_numpy(dtype=float)
    y = df["target"].to_numpy()

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3,
                                          random_state=seed, stratify=y)
    clf = GradientBoostingClassifier(random_state=seed).fit(Xtr, ytr)
    acc = float(clf.score(Xte, yte))

    proba_te = clf.predict_proba(Xte)[:, 1]
    thresh = 0.5
    denied = np.where(proba_te < thresh)[0]

    import shap
    explainer = shap.TreeExplainer(clf)
    shap_vals = explainer.shap_values(Xte)

    idx = {f: i for i, f in enumerate(feats)}
    act_idx = [idx[f] for f in ACTIONABLE]
    y_star = thresh  # desired prediction: cross the approval threshold
    rng = np.random.default_rng(seed)

    def recourse_utility(i, guided):
        """One denied applicant tries K single-feature edits; state
        s = y* - yhat', utility -s^2 (0 once approved).  Guided = edit the
        actionable feature with the largest |SHAP| first."""
        x = Xte[i].copy()
        if guided:
            order = sorted(act_idx, key=lambda j: -abs(shap_vals[i][j]))
        else:
            order = list(rng.permutation(act_idx))
        best_u = None
        for j in order[:2]:  # budget: 2 feature edits
            for scale in (0.5, 1.5, 2.0):
                x2 = x.copy()
                x2[j] = x[j] * scale if x[j] != 0 else scale
                p2 = clf.predict_proba(x2.reshape(1, -1))[0, 1]
                s = max(0.0, y_star - p2)
                uu = -s ** 2
                best_u = uu if best_u is None else max(best_u, uu)
        return best_u

    u_guided = float(np.mean([recourse_utility(i, True) for i in denied]))
    u_blind = float(np.mean([recourse_utility(i, False) for i in denied]))
    return {"n_applicants": int(len(df)), "model_test_acc": round(acc, 3),
            "n_denied": int(len(denied)),
            "E_utility_with_explanation": round(u_guided, 5),
            "E_utility_without_explanation": round(u_blind, 5),
            "explanation_gain": round(u_guided - u_blind, 5)}


def main():
    e1 = example1()
    print("== Example 1 (medical treatment / biopsy), exact rational arithmetic ==")
    print(f"  rational rule == 'biopsy iff q > 9/10' on 101-point exact belief grid: "
          f"{'PASS' if e1['rule_matches_threshold_9_10'] else 'FAIL'}")
    print(f"  negative control (swapped biopsy costs): 9/10 rule breaks as expected: "
          f"{'PASS' if e1['wrong_utility_rule_fails'] else 'FAIL'}")
    print(f"  R_prior = {e1['R_prior']}, R_signal = {e1['R_signal']}, "
          f"value of information = {e1['value_of_information']} "
          f"(= {e1['voi_float']})")

    e2 = example2()
    print("\n== Example 2 (recourse provision), German Credit, 1000 applicants ==")
    print(f"  lender model: GradientBoosting, test accuracy {e2['model_test_acc']}, "
          f"{e2['n_denied']} denied applicants in holdout")
    print(f"  E[u] recourse WITH explanation (SHAP-guided): "
          f"{e2['E_utility_with_explanation']}")
    print(f"  E[u] recourse WITHOUT explanation (random order): "
          f"{e2['E_utility_without_explanation']}")
    print(f"  explanation gain: {e2['explanation_gain']} "
          f"(positive = explanation helps the applicant reach y*)")

    out = {"example1": e1, "example2": e2}
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "claim6_examples.json").write_text(json.dumps(out, indent=1))
    print(f"\nRESULTS_SHA256={results_sha(out)}")
    assert e1["rule_matches_threshold_9_10"]


if __name__ == "__main__":
    main()
