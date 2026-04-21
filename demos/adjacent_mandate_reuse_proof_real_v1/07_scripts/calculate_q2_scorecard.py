#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "04_scorecard"
RUN_COSTS = BASE / "run_costs.template.csv"
OUTPUTS = BASE / "output_scoring.template.csv"
OUTDIR = BASE / "out"
OUTDIR.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def to_float(v):
    try:
        return float(v)
    except Exception:
        return 0.0

def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return 0

cost_rows = read_csv(RUN_COSTS)
output_rows = read_csv(OUTPUTS)

lanes = {"control": {}, "treatment": {}}

for row in cost_rows:
    lane = row["lane"].strip().lower()
    if lane not in lanes:
        continue
    lanes[lane]["cost_units"] = to_float(row.get("cost_units", 0))

for lane in lanes:
    accepted = [r for r in output_rows if r["lane"].strip().lower() == lane and to_int(r.get("accepted", 0)) == 1]
    lanes[lane]["accepted_count"] = len(accepted)
    lanes[lane]["usefulness_points"] = sum(to_float(r.get("usefulness_points", 0)) for r in accepted)
    cost = lanes[lane].get("cost_units", 0.0)
    lanes[lane]["aoy"] = (lanes[lane]["usefulness_points"] / cost) if cost > 0 else 0.0
    times = [to_float(r.get("time_to_accept_hours", 0)) for r in accepted if to_float(r.get("time_to_accept_hours", 0)) > 0]
    lanes[lane]["time_to_first_accepted_output"] = min(times) if times else 0.0
    reworks = [to_float(r.get("rework_rounds", 0)) for r in accepted]
    lanes[lane]["avg_rework"] = (sum(reworks) / len(reworks)) if reworks else 0.0
    fractions = []
    for r in accepted:
        fields = [
            to_int(r.get("evidence_code_pointer", 0)),
            to_int(r.get("evidence_broken_condition", 0)),
            to_int(r.get("evidence_repro", 0)),
            to_int(r.get("evidence_severity_rationale", 0)),
            to_int(r.get("evidence_fix", 0)),
            to_int(r.get("evidence_replay_artifact", 0)),
        ]
        fractions.append(sum(fields) / 6.0)
    lanes[lane]["evidence_completeness"] = (sum(fractions) / len(fractions)) if fractions else 0.0
    lanes[lane]["safety_incidents"] = sum(to_int(r.get("safety_incident", 0)) for r in output_rows if r["lane"].strip().lower() == lane)
    lanes[lane]["unsupported_claims"] = sum(to_int(r.get("unsupported_claim_count", 0)) for r in output_rows if r["lane"].strip().lower() == lane)
    lanes[lane]["hallucinated_references"] = sum(to_int(r.get("hallucinated_reference_count", 0)) for r in output_rows if r["lane"].strip().lower() == lane)
    dep_num = sum(to_int(r.get("package_dependency", 0)) for r in accepted)
    dep_den = len(accepted)
    lanes[lane]["package_dependence"] = (dep_num / dep_den) if dep_den else 0.0

control = lanes["control"]
treatment = lanes["treatment"]

def rel_improve(base, new, higher_is_better=True):
    if base == 0:
        return 0.0
    if higher_is_better:
        return (new - base) / base
    return (base - new) / base

results = {
    "control": control,
    "treatment": treatment,
    "comparisons": {
        "aoy_uplift": rel_improve(control["aoy"], treatment["aoy"], True),
        "speed_uplift": rel_improve(control["time_to_first_accepted_output"], treatment["time_to_first_accepted_output"], False),
        "rework_reduction": rel_improve(control["avg_rework"], treatment["avg_rework"], False),
        "evidence_completeness_uplift": rel_improve(control["evidence_completeness"], treatment["evidence_completeness"], True),
        "package_dependence": treatment["package_dependence"],
        "safety_regression": not (
            treatment["safety_incidents"] > control["safety_incidents"] or
            treatment["unsupported_claims"] > control["unsupported_claims"] or
            treatment["hallucinated_references"] > control["hallucinated_references"]
        ),
    }
}

comparisons = results["comparisons"]
thresholds = {
    "aoy_uplift": 0.35,
    "speed_uplift": 0.30,
    "rework_reduction": 0.40,
    "evidence_completeness_uplift": 0.20,
    "package_dependence": 0.30,
    "safety_regression": True,
}

pass_flags = {
    "aoy_uplift": comparisons["aoy_uplift"] >= thresholds["aoy_uplift"],
    "speed_uplift": comparisons["speed_uplift"] >= thresholds["speed_uplift"],
    "rework_reduction": comparisons["rework_reduction"] >= thresholds["rework_reduction"],
    "evidence_completeness_uplift": comparisons["evidence_completeness_uplift"] >= thresholds["evidence_completeness_uplift"],
    "package_dependence": comparisons["package_dependence"] >= thresholds["package_dependence"],
    "safety_regression": comparisons["safety_regression"] is True,
}
results["pass_flags"] = pass_flags
results["adjacent_mandate_pass"] = all(pass_flags.values())

(OUTDIR / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

md = []
md.append("# Q2 scorecard summary")
md.append("")
md.append("## Control")
for k, v in control.items():
    md.append(f"- **{k}**: {v}")
md.append("")
md.append("## Treatment")
for k, v in treatment.items():
    md.append(f"- **{k}**: {v}")
md.append("")
md.append("## Comparisons")
for k, v in comparisons.items():
    md.append(f"- **{k}**: {v}")
md.append("")
md.append("## Pass flags")
for k, v in pass_flags.items():
    md.append(f"- **{k}**: {'PASS' if v else 'FAIL'}")
md.append("")
md.append(f"## Overall adjacent-mandate result")
md.append(f"**{'PASS' if results['adjacent_mandate_pass'] else 'FAIL'}**")
(OUTDIR / "summary.md").write_text("\n".join(md), encoding="utf-8")

print("Wrote:")
print(OUTDIR / "summary.json")
print(OUTDIR / "summary.md")
