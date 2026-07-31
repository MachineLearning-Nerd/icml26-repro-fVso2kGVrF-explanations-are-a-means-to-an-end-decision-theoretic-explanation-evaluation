"""Full-scale Ames Iowa case study: Definitions 6-7 (Claims 1-2), Section B
numbers (Claim 5), and the paper's own empirical Proposition-4 demonstration
(Figure 1 / Claim 4 empirical arm).

Reproduces, for N_SEEDS independent 80/20 splits:
  MAPE of the rational agent under signal sets
    prior-only, X, Yhat, Z, X+Yhat, X+Yhat+Z, yH, yH+X, yH+Yhat, yH+Z
  Theoretic value (Def 6):        TVE  = relative MAPE improvement of X over prior
  Potential complementary value (Def 7): PHCV = relative improvement of yH+X over yH
  Figure-1 bars: theoretic + complementary value of X, Yhat, Z
  Prop 4 empirical: X+Yhat+Z vs X+Yhat vs X (differences ~ 0)

Paper targets (Section B / Examples 4-5):
  TVE  = 24.2% MAPE improvement, 95% CI [22.4, 26.1]
  PHCV =  9.0% MAPE improvement, 95% CI [8.1, 9.9]

Also runs a sensitivity sweep over the ambiguous implementation choices and two
negative controls.  Deterministic: fixed seeds, single-thread XGBoost.
"""
import json

import numpy as np
import shap
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor

from common import (ART, ape, col, fit_agent, load_ames, mape_optimal_constant,
                    results_sha, split, t_ci)

N_SEEDS = 100
N_SEEDS_SENS = 25

PAPER = {"tve": (24.2, 22.4, 26.1), "phcv": (9.0, 8.1, 9.9)}


def one_seed(X, price, cond, seed, agent="xgb", prior="wmed"):
    Xtr, Xte, ptr, pte, ctr, cte = split(X, price, cond, seed)

    # AI model: XGBoost predicting the overall-condition score (Appendix B).
    m_cond = fit_agent(Xtr, ctr, seed=0)
    yhat_tr, yhat_te = m_cond.predict(Xtr), m_cond.predict(Xte)
    ex = shap.TreeExplainer(m_cond)
    Ztr, Zte = ex.shap_values(Xtr), ex.shap_values(Xte)

    # Synthetic human (Eq. 10): OLS on the three features vs sale price.
    hum = LinearRegression().fit(Xtr, ptr)
    h_tr, h_te = hum.predict(Xtr), hum.predict(Xte)

    def agent_mape(sig_tr, sig_te):
        if agent == "xgb":
            m = fit_agent(sig_tr, ptr, seed=0)
        elif agent == "ridge":
            m = Ridge().fit(sig_tr, ptr)
        elif agent == "knn":
            m = KNeighborsRegressor(n_neighbors=25).fit(sig_tr, ptr)
        return float(ape(m.predict(sig_te), pte).mean())

    if prior == "wmed":
        a0 = mape_optimal_constant(ptr)
    elif prior == "mean":
        a0 = ptr.mean()
    elif prior == "median":
        a0 = np.median(ptr)
    m0 = float(ape(np.full_like(pte, a0), pte).mean())

    sigs = {
        "X": (Xtr, Xte),
        "Yhat": (col(yhat_tr), col(yhat_te)),
        "Z": (Ztr, Zte),
        "XY": (np.hstack([Xtr, col(yhat_tr)]), np.hstack([Xte, col(yhat_te)])),
        "XYZ": (np.hstack([Xtr, col(yhat_tr), Ztr]),
                np.hstack([Xte, col(yhat_te), Zte])),
        "H": (col(h_tr), col(h_te)),
        "HX": (np.hstack([col(h_tr), Xtr]), np.hstack([col(h_te), Xte])),
        "HY": (np.hstack([col(h_tr), col(yhat_tr)]),
               np.hstack([col(h_te), col(yhat_te)])),
        "HZ": (np.hstack([col(h_tr), Ztr]), np.hstack([col(h_te), Zte])),
    }
    m = {k: agent_mape(tr, te) for k, (tr, te) in sigs.items()}
    m["prior"] = m0
    return m


def rel(m, sig, base):
    return 100.0 * (m[base] - m[sig]) / m[base]


def negative_controls(X, price, cond, seed=0):
    rng = np.random.default_rng(seed)
    Xtr, Xte, ptr, pte, ctr, cte = split(X, price, cond, seed)
    a0 = mape_optimal_constant(ptr)
    m0 = float(ape(np.full_like(pte, a0), pte).mean())

    # Control 1: destroyed signal. Row-shuffled features carry no information
    # about the state, so TVE must collapse to ~0.
    Xtr_sh = Xtr[rng.permutation(len(Xtr))]
    Xte_sh = Xte[rng.permutation(len(Xte))]
    m_sh = float(ape(fit_agent(Xtr_sh, ptr, seed=0).predict(Xte_sh), pte).mean())
    tve_shuffled = 100.0 * (m0 - m_sh) / m0

    # Control 2: a state-leaking pseudo-explanation (NOT a garbling of X,Yhat).
    # Prop 4's assumption is violated, so it must add large value over X.
    m_cond = fit_agent(Xtr, ctr, seed=0)
    yhat_tr, yhat_te = m_cond.predict(Xtr), m_cond.predict(Xte)
    leak_tr = col(ptr * (1 + rng.normal(0, 0.05, len(ptr))))
    leak_te = col(pte * (1 + rng.normal(0, 0.05, len(pte))))
    mX = float(ape(fit_agent(Xtr, ptr, seed=0).predict(Xte), pte).mean())
    Xl_tr = np.hstack([Xtr, col(yhat_tr), leak_tr])
    Xl_te = np.hstack([Xte, col(yhat_te), leak_te])
    m_leak = float(ape(fit_agent(Xl_tr, ptr, seed=0).predict(Xl_te), pte).mean())
    return {
        "tve_shuffled_features": round(tve_shuffled, 2),
        "mape_X": round(100 * mX, 2),
        "mape_X_plus_leaky_Z": round(100 * m_leak, 2),
        "leak_gain_pp": round(100 * (mX - m_leak), 2),
    }


def main():
    X, price, cond = load_ames()
    print(f"Ames Iowa dataset (De Cock 2011): {len(price)} rows after dropna; "
          f"features = year built, bedrooms, exterior material")

    runs = [one_seed(X, price, cond, s) for s in range(N_SEEDS)]

    def series(f):
        return [f(m) for m in runs]

    tve = series(lambda m: rel(m, "X", "prior"))
    phcv = series(lambda m: rel(m, "HX", "H"))

    out = {"n_seeds": N_SEEDS, "paper": PAPER}
    print(f"\n== Main configuration ({N_SEEDS} independent 80/20 splits, "
          f"XGBoost agent, MAPE-optimal prior constant) ==")
    for name, vals, (pt, lo, hi) in [("TVE  (Def 6)", tve, PAPER["tve"]),
                                     ("PHCV (Def 7)", phcv, PAPER["phcv"])]:
        clo, chi = t_ci(vals)
        mean = float(np.mean(vals))
        # The paper's estimate is one draw from the split distribution, so the
        # consistency question is predictive: is the paper point inside the
        # 95% range of faithful reruns?  (The CI of our mean answers a
        # different, much narrower question and is reported alongside.)
        plo, phi = np.percentile(vals, [2.5, 97.5])
        key = name.split()[0].lower()
        out[key] = {"mean": round(mean, 2), "ci": [round(clo, 2), round(chi, 2)],
                    "seed_range_95": [round(float(plo), 2), round(float(phi), 2)],
                    "paper_point": pt, "paper_ci": [lo, hi],
                    "paper_point_in_seed_range": bool(plo <= pt <= phi),
                    "our_mean_in_paper_ci": bool(lo <= mean <= hi)}
        print(f"{name}: mean {mean:5.2f}%  95% t-CI of mean [{clo:5.2f}, {chi:5.2f}]  "
              f"seed 95% range [{plo:5.2f}, {phi:5.2f}]")
        print(f"       paper {pt}% CI [{lo}, {hi}]  "
              f"| paper point in seed range: {plo <= pt <= phi}  "
              f"| our mean in paper CI: {lo <= mean <= hi}")

    print("\n== Figure 1 reproduction: value of each signal (mean over seeds) ==")
    fig1 = {}
    comp_key = {"X": "HX", "Yhat": "HY", "Z": "HZ"}
    for sig in ["X", "Yhat", "Z"]:
        tv = float(np.mean(series(lambda m: rel(m, sig, "prior"))))
        cv = float(np.mean(series(lambda m: rel(m, comp_key[sig], "H"))))
        fig1[sig] = {"theoretic": round(tv, 2), "complementary": round(cv, 2)}
        print(f"  {sig:5s} theoretic value {tv:6.2f}%   complementary value {cv:6.2f}%")
    out["figure1"] = fig1

    print("\n== Proposition 4, paper's own empirical arm ==")
    print("   (gain of the richer signal set; paper: explanations offer NO")
    print("    ADDITIONAL value, so the gain must not be significantly positive)")
    prop4 = {}
    for a, b, label in [("XYZ", "XY", "gain of Z over X+Yhat"),
                        ("XY", "X", "gain of Yhat over X"),
                        ("XYZ", "X", "gain of Yhat+Z over X")]:
        d = [100.0 * (m[b] - m[a]) / m[b] for m in runs]
        clo, chi = t_ci(d)
        mean = float(np.mean(d))
        no_gain = bool(chi < 1.0)  # upper CI bound: no material improvement
        prop4[f"{a}_vs_{b}"] = {"mean": round(mean, 2),
                                "ci": [round(clo, 2), round(chi, 2)],
                                "no_additional_value": no_gain,
                                "per_seed": [round(v, 4) for v in d]}
        print(f"  {label}: mean {mean:5.2f}%  CI [{clo:5.2f}, {chi:5.2f}]  "
              f"no additional value (upper CI < 1%): {no_gain}")
    out["prop4_empirical"] = prop4

    print(f"\n== Sensitivity sweep ({N_SEEDS_SENS} seeds each) ==")
    sens = {}
    for agent, prior in [("xgb", "mean"), ("xgb", "median"),
                         ("ridge", "wmed"), ("knn", "wmed")]:
        rs = [one_seed(X, price, cond, s, agent=agent, prior=prior)
              for s in range(N_SEEDS_SENS)]
        tvs = [rel(m, "X", "prior") for m in rs]
        pvs = [rel(m, "HX", "H") for m in rs]
        tv, pv = float(np.mean(tvs)), float(np.mean(pvs))
        sens[f"{agent}/{prior}"] = {"tve": round(tv, 2), "phcv": round(pv, 2),
                                    "tve_per_seed": [round(v, 4) for v in tvs],
                                    "phcv_per_seed": [round(v, 4) for v in pvs]}
        print(f"  agent={agent:6s} prior={prior:7s}: TVE {tv:6.2f}%  PHCV {pv:6.2f}%")
    # absolute percentage-point reading, for the interpretation audit
    tv_pp = float(np.mean([100 * (m["prior"] - m["X"]) for m in runs]))
    sens["pp_reading"] = {"tve_pp": round(tv_pp, 2)}
    print(f"  percentage-point reading of TVE: {tv_pp:.2f} pp "
          f"(infeasible as 24.2: would need 3-feature MAPE ~= "
          f"{100 * np.mean([m['prior'] for m in runs]) - 24.2:.1f}%)")
    out["sensitivity"] = sens

    print("\n== Negative controls ==")
    nc = negative_controls(X, price, cond)
    print(f"  shuffled-features TVE: {nc['tve_shuffled_features']}% (expect ~0 or <0)")
    print(f"  state-leaking pseudo-explanation: MAPE {nc['mape_X']}% -> "
          f"{nc['mape_X_plus_leaky_Z']}% (gain {nc['leak_gain_pp']} pp; "
          f"expect large gain because the garbling assumption is violated)")
    out["negative_controls"] = nc

    out["per_seed"] = {"tve": [round(v, 4) for v in tve],
                       "phcv": [round(v, 4) for v in phcv]}
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "claim156_ames.json").write_text(json.dumps(out, indent=1))
    with open(ART / "claim156_per_seed.csv", "w") as f:
        f.write("seed,tve_pct,phcv_pct\n")
        for i, (a, b) in enumerate(zip(tve, phcv)):
            f.write(f"{i},{a:.4f},{b:.4f}\n")
    print(f"\nRESULTS_SHA256={results_sha(out)}")


if __name__ == "__main__":
    main()
