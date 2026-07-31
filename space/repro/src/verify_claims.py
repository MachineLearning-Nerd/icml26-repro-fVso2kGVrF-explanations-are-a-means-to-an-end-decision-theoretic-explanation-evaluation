"""Independent claim verifier: reads ONLY the JSON artifacts written by the
claim scripts and checks each claim contract, exiting nonzero on any failure.
"""
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
# repo layout keeps artifacts under .openresearch/; the Space mirror ships the
# same files under repro/artifacts — support both so the shipped checker runs
# against the shipped artifacts out of the box.
ART = next(p for p in (_ROOT / ".openresearch" / "artifacts",
                       _ROOT / "artifacts")
           if (p / "claim156_ames.json").exists())

failures = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        failures.append(name)


def main():
    a = json.loads((ART / "claim156_ames.json").read_text())
    print("== Claims 1, 2, 5 (Ames case study, Definitions 6-7, Section B) ==")
    for key, label in [("tve", "TVE"), ("phcv", "PHCV")]:
        r = a[key]
        check(f"{label}: paper point {r['paper_point']} inside our seed 95% range "
              f"{r['seed_range_95']}", r["paper_point_in_seed_range"])
        check(f"{label}: our mean {r['mean']} inside paper 95% CI {r['paper_ci']}",
              r["our_mean_in_paper_ci"])
    nc = a["negative_controls"]
    check(f"negative control: shuffled-features TVE {nc['tve_shuffled_features']}% < 3%",
          nc["tve_shuffled_features"] < 3.0)
    check(f"negative control: state-leaking Z gains {nc['leak_gain_pp']} pp > 5 pp",
          nc["leak_gain_pp"] > 5.0)

    print("== Claim 4 (Proposition 4) ==")
    p = json.loads((ART / "claim4_prop4.json").read_text())
    check(f"partition identity for all {p['n_garblings']} garblings + symbolic R equality",
          p["part_a_all_garblings"])
    check(f"exact rational R_XYZ == R_XY == R_X on {p['part_b_exact_equal']}"
          f"/{p['part_b_total']} random problems",
          p["part_b_exact_equal"] == p["part_b_total"])
    from fractions import Fraction
    check(f"negative control: R_peek {p['part_c_R_peek']} > R_xy {p['part_c_R_xy']}",
          Fraction(p["part_c_R_peek"]) > Fraction(p["part_c_R_xy"]))
    for key, lbl in [("XYZ_vs_XY", "Z over X+Yhat"), ("XY_vs_X", "Yhat over X"),
                     ("XYZ_vs_X", "Yhat+Z over X")]:
        r = a["prop4_empirical"][key]
        check(f"Ames empirical: no additional value of {lbl} (gain CI {r['ci']}, "
              f"upper bound < 1%)", r["no_additional_value"])

    print("== Claim 6 (Definition 1, Examples 1-2) ==")
    e = json.loads((ART / "claim6_examples.json").read_text())
    check("Example 1 rational rule == exact 9/10 threshold",
          e["example1"]["rule_matches_threshold_9_10"])
    check("Example 1 value of information > 0",
          e["example1"]["voi_float"] > 0)
    check("Example 1 negative control: wrong utility breaks the 9/10 rule",
          e["example1"]["wrong_utility_rule_fails"])
    check(f"Example 2 lender model acc {e['example2']['model_test_acc']} > 0.65",
          e["example2"]["model_test_acc"] > 0.65)
    check(f"Example 2 has denied applicants ({e['example2']['n_denied']})",
          e["example2"]["n_denied"] > 0)
    check(f"Example 2 explanation gain {e['example2']['explanation_gain']} > 0",
          e["example2"]["explanation_gain"] > 0)

    print("== Claim 3 (Definition 8, real controlled study) ==")
    b = json.loads((ART / "claim3_behavioral.json").read_text())
    check(f"real participants: {b['n_workers']} workers >= 700",
          b["n_workers"] >= 700)
    check("treatment effect measured with 95% CI (both utilities)",
          "ape" in b and "abs_err" in b and len(b["ape"]["ci"]) == 2)
    check(f"placebo control CI {b['placebo']['ci']} covers 0",
          b["placebo"]["ci"][0] <= 0 <= b["placebo"]["ci"][1])

    print()
    if failures:
        print(f"VERDICT: FAIL ({len(failures)} failed checks)")
        sys.exit(1)
    print("VERDICT: ALL CLAIM CONTRACTS PASS")


if __name__ == "__main__":
    main()
