"""Proposition 4 (Claim 4): R_{X u Yhat u Z} = R_{X u Yhat} ( = R_X when
Yhat = h(X) ), for any explanation Z = g(X, Yhat).

The proof content is structural, so we verify it as an exact argument, not a
sampled illustration:

Part A (decision procedure, exhaustive over a complete finite domain):
  R_V = sum_v max_a sum_s p(s, v) u(a, s) depends on V only through the
  partition that V induces on signal realizations.  Since the map
  (x, yhat) -> (x, yhat, g(x, yhat)) is injective with inverse the projection,
  the partition induced by (X, Yhat, Z) EQUALS the partition induced by
  (X, Yhat) -- for EVERY function g.  We verify this partition identity
  exhaustively for every g: XxYhat -> Z over stated finite alphabets, and,
  with sympy, that partition equality forces R equality for fully symbolic
  p and u (i.e. for ALL priors and ALL utilities on those alphabets).

Part B (exact rational arithmetic): for randomly generated decision problems
  with Fraction-valued p and u and random h, g, assert R_XYZ == R_XY == R_X
  as EXACT rational equalities (no tolerance).

Part C (negative control): an explanation that is NOT a garbling of (X, Yhat)
  (it peeks at the state) must strictly increase R on a problem where the
  extra information matters -- verifying the check can fail for the intended
  reason.

Empirical full-scale corroboration on the Ames case study lives in
claim156_ames.py (the paper's own Figure-1 demonstration).
"""
import itertools
import json
from fractions import Fraction
import random

import sympy as sp

from common import ART, results_sha


def rational_R(joint, u, group_key):
    """R_V with exact Fractions. joint: list of (s, x, yhat, prob).
    group_key maps (x, yhat) -> hashable signal value v."""
    groups = {}
    states = sorted({s for s, _, _, _ in joint})
    for s, x, y, pr in joint:
        groups.setdefault(group_key(x, y), {}).setdefault(s, Fraction(0))
        groups[group_key(x, y)][s] += pr
    total = Fraction(0)
    actions = sorted({a for (a, s) in u})
    for v, post in groups.items():
        best = max(sum(post.get(s, Fraction(0)) * u[(a, s)] for s in states)
                   for a in actions)
        total += best
    return total


def part_a():
    """Exhaustive partition identity + symbolic R equality."""
    SX, SY, SZ = 3, 2, 2  # |X|=3, |Yhat|=2, |Z|=2 -> all 2^6 = 64 garblings g
    pairs = list(itertools.product(range(SX), range(SY)))
    all_g = list(itertools.product(range(SZ), repeat=len(pairs)))
    assert len(all_g) == SZ ** len(pairs)
    for gvals in all_g:
        g = dict(zip(pairs, gvals))
        # partition of signal space by (x,y) vs by (x,y,g(x,y))
        part_xy = {p: p for p in pairs}
        part_xyz = {p: (p[0], p[1], g[p]) for p in pairs}
        # equality of partitions == the two labelings induce identical blocks
        blocks_xy = {}
        blocks_xyz = {}
        for p in pairs:
            blocks_xy.setdefault(part_xy[p], set()).add(p)
            blocks_xyz.setdefault(part_xyz[p], set()).add(p)
        if set(map(frozenset, blocks_xy.values())) != set(map(frozenset, blocks_xyz.values())):
            return False, len(all_g)
    # Symbolic: R equality for ALL p, u, and ALL g, derived by the actual
    # grouping procedure (not by construction).  Fully symbolic p(s,x,y) and
    # u(a,s) on |S|=2, |A|=2; for each g, group realizations by their signal
    # label and sum max-a posterior utilities over the resulting blocks.
    s0p = {(s, x, y): sp.Symbol(f"p_{s}{x}{y}", positive=True)
           for s in range(2) for x in range(SX) for y in range(SY)}
    u = {(a, s): sp.Symbol(f"u_{a}{s}") for a in range(2) for s in range(2)}

    def symbolic_R(label):
        groups = {}
        for x, y in pairs:
            groups.setdefault(label(x, y), []).append((x, y))
        return sum(sp.Max(*[sum(s0p[(s, x, y)] * u[(a, s)]
                                for s in range(2) for x, y in block)
                            for a in range(2)]) for block in groups.values())

    R_xy = symbolic_R(lambda x, y: (x, y))
    for gvals in all_g:
        g = dict(zip(pairs, gvals))
        R_xyz = symbolic_R(lambda x, y: (x, y, g[(x, y)]))
        if sp.simplify(R_xy - R_xyz) != 0:
            return False, len(all_g)
    return True, len(all_g)


def rand_frac(rng):
    return Fraction(rng.randint(1, 20), rng.randint(21, 60))


def part_b(n_problems=500, seed=12345):
    rng = random.Random(seed)
    exact_ok = 0
    for _ in range(n_problems):
        nS, nA, nX, nY, nZ = (rng.randint(2, 4) for _ in range(5))
        h = {x: rng.randrange(nY) for x in range(nX)}
        g = {(x, y): rng.randrange(nZ) for x in range(nX) for y in range(nY)}
        u = {(a, s): rand_frac(rng) - rand_frac(rng)
             for a in range(nA) for s in range(nS)}
        raw = [(s, x, rand_frac(rng)) for s in range(nS) for x in range(nX)]
        tot = sum(pr for _, _, pr in raw)
        joint = [(s, x, h[x], pr / tot) for s, x, pr in raw]
        R_x = rational_R(joint, u, lambda x, y: x)
        R_xy = rational_R(joint, u, lambda x, y: (x, y))
        R_xyz = rational_R(joint, u, lambda x, y: (x, y, g[(x, y)]))
        if R_xyz == R_xy == R_x:
            exact_ok += 1
    return exact_ok, n_problems


def part_c():
    """Negative control: state-peeking Z' strictly increases R."""
    # 2 states, 2 actions, 1 feature value (X carries nothing), u = identity
    # match; Z' = s reveals the state.
    u = {(a, s): Fraction(1) if a == s else Fraction(0)
         for a in range(2) for s in range(2)}
    joint = [(0, 0, 0, Fraction(1, 2)), (1, 0, 0, Fraction(1, 2))]
    R_xy = rational_R(joint, u, lambda x, y: (x, y))
    # peeking explanation: group by the true state (only possible because Z'
    # is NOT a function of (x, yhat))
    groups = {}
    for s, x, y, pr in joint:
        groups.setdefault(s, {}).setdefault(s, Fraction(0))
        groups[s][s] += pr
    R_peek = sum(max(sum(post.get(s, Fraction(0)) * u[(a, s)] for s in (0, 1))
                     for a in (0, 1)) for post in groups.values())
    return R_xy, R_peek


def main():
    ok_a, n_g = part_a()
    print(f"Part A: partition identity for ALL {n_g} garblings g on "
          f"|X|=3,|Yhat|=2,|Z|=2: {'PASS' if ok_a else 'FAIL'}; "
          f"symbolic R_XY == R_XYZ for fully symbolic p,u: {'PASS' if ok_a else 'FAIL'}")
    ok_b, n_b = part_b()
    print(f"Part B: exact rational R_XYZ == R_XY == R_X on {ok_b}/{n_b} random "
          f"decision problems (Fraction arithmetic, zero tolerance)")
    r_xy, r_peek = part_c()
    print(f"Part C (negative control): R_XY = {r_xy} < R_peek = {r_peek} -> "
          f"a non-garbling 'explanation' strictly helps: "
          f"{'PASS' if r_peek > r_xy else 'FAIL'}")
    out = {"part_a_all_garblings": ok_a, "n_garblings": n_g,
           "part_b_exact_equal": ok_b, "part_b_total": n_b,
           "part_c_R_xy": str(r_xy), "part_c_R_peek": str(r_peek)}
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "claim4_prop4.json").write_text(json.dumps(out, indent=1))
    print(f"RESULTS_SHA256={results_sha(out)}")
    assert ok_a and ok_b == n_b and r_peek > r_xy


if __name__ == "__main__":
    main()
