"""Shared machinery for the Ames Iowa case study (paper Appendix B / Examples 4-5).

Paper setup (arXiv:2506.22740, Appendix B):
  - Ames Iowa dataset (De Cock 2011), 80/20 train/holdout split.
  - Signals: X = {year built, #bedrooms, exterior covering material};
    Yhat = XGBoost model trained on the dataset predicting the overall
    condition score from the same three features; Z = SHAP values of Yhat.
  - Synthetic human: linear model yH = b0 + b1*X1 + b2*X2 + b3*X3 fit on the
    training set against ground-truth sale prices (Eq. 10).
  - Utility u(a,s) = -|s-a|/s (Example 4), i.e. score = negative APE; expected
    scores are reported as MAPE.
  - Rational Bayesian agent with signal set V: acts to maximize posterior
    expected utility given V.  Empirically approximated by a regressor trained
    on (V -> sale price) on the training split; the prior-only agent plays the
    MAPE-optimal constant action (the 1/s-weighted median of training prices).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy import stats

REPO = Path(__file__).resolve().parents[1]
ART = REPO / ".openresearch" / "artifacts"
sys.path.insert(0, str(REPO / "data"))
from fetch import fetch  # noqa: E402

FEATURES = ["Year Built", "Bedroom AbvGr", "Exterior 1st"]
TARGET = "SalePrice"
CONDITION = "Overall Cond"


def load_ames():
    df = pd.read_csv(fetch("AmesHousing.txt"), sep="\t")
    df = df[FEATURES + [CONDITION, TARGET]].dropna().reset_index(drop=True)
    # Exterior material is categorical; trees need a numeric encoding.
    df["ext_code"] = df["Exterior 1st"].astype("category").cat.codes
    X = df[["Year Built", "Bedroom AbvGr", "ext_code"]].to_numpy(dtype=float)
    price = df[TARGET].to_numpy(dtype=float)
    cond = df[CONDITION].to_numpy(dtype=float)
    return X, price, cond


def mape_optimal_constant(prices):
    """argmin_a E[|s-a|/s]: the median of s under weights 1/s."""
    o = np.argsort(prices)
    w = np.cumsum(1.0 / prices[o])
    return prices[o][np.searchsorted(w, w[-1] / 2.0)]


def ape(pred, s):
    return np.abs(s - pred) / s


def fit_agent(sig_tr, price_tr, seed=0):
    """Rational-agent approximation: posterior-mean regressor on the signals."""
    m = xgb.XGBRegressor(random_state=seed, n_jobs=1)
    m.fit(sig_tr, price_tr)
    return m


def t_ci(values, conf=0.95):
    v = np.asarray(values, dtype=float)
    lo, hi = stats.t.interval(conf, len(v) - 1, loc=v.mean(), scale=stats.sem(v))
    return float(lo), float(hi)


def col(a):
    return np.asarray(a).reshape(-1, 1)


def split(X, price, cond, seed):
    return train_test_split(X, price, cond, test_size=0.2, random_state=seed)


def results_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()
