from __future__ import annotations
from pathlib import Path
import argparse

from .business import load_parent_business, emit_parent_business_artifact
from .seeds import load_seed_packets, emit_seed_packets
from .fixtures import read_contracts
from .assay import run_mandate_1_competition, run_mandate_2
from .package_builder import build_capability_packages
from .scorecard import build_scorecard
from .sovereign import emit_sovereign_or_ruling
from .utils import reset_dir, write_json, write_text, demo_timestamp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo_output"


def _pct(v: float) -> str:
    return f"{v*100:.1f}%"


def run_demo(assert_mode: bool = False):
    reset_dir(OUT)

    parent = load_parent_business(ROOT / "parent_business" / "protocol_assurance_studio.json")
    seeds = load_seed_packets(ROOT / "nova_seeds")
    emit_parent_business_artifact(parent, OUT / "parent_business")
    emit_seed_packets(seeds, OUT / "nova_seeds")

    mandate_1_contracts = read_contracts(ROOT / "contracts" / "mandate_1")
    mandate_1_summary = run_mandate_1_competition(
        seeds,
        mandate_1_contracts,
        ROOT / "ground_truth" / "mandate_1.json",
        OUT / "mandate_1",
    )
    winner_id = mandate_1_summary["winner"]
    winner_result = next(r for r in mandate_1_summary["results"] if r["seed"] == winner_id)

    governance_pack, protocol_pack = build_capability_packages(winner_result, OUT / "capability_package")

    mandate_2_contracts = read_contracts(ROOT / "contracts" / "mandate_2")
    winner_seed = next(seed for seed in seeds if seed["id"] == winner_id)
    control = run_mandate_2(winner_seed, mandate_2_contracts, ROOT / "ground_truth" / "mandate_2.json", False, OUT / "mandate_2_control")
    treatment = run_mandate_2(winner_seed, mandate_2_contracts, ROOT / "ground_truth" / "mandate_2.json", True, OUT / "mandate_2_treatment")

    scorecard = build_scorecard(control["metrics"], treatment["metrics"], OUT / "scorecard")
    sovereign_or_ruling = emit_sovereign_or_ruling(scorecard, protocol_pack, OUT / "sovereign")
    governance_ruling = {
        "id": "governance_ruling.json",
        "status": "pass" if scorecard["passes"]["adjacent_mandate_proof"] else "fail_closed",
        "decision": "emit_protocol_assurance_sovereign" if scorecard["passes"]["adjacent_mandate_proof"] else "block_protocol_assurance_sovereign",
        "justification": "Threshold scorecard evaluated under deterministic control-vs-treatment adjacent mandate assay.",
        "linked_artifact": sovereign_or_ruling["id"],
        "timestamp": sovereign_or_ruling["timestamp"],
        "disclaimer": "Synthetic governance ruling for local replay; not a real-world governance decision."
    }
    write_json(OUT / "proof_docket" / governance_ruling["id"], governance_ruling)

    now = demo_timestamp()
    release_gate_packet = {
        "id": "release_gate_packet",
        "timestamp": now,
        "status": "pass" if scorecard["passes"]["adjacent_mandate_proof"] else "fail",
        "requirements": protocol_pack["portable_components"]["release_gate_packet"]["required"],
    }
    write_json(OUT / "scorecard" / "release_gate_packet.json", release_gate_packet)

    chronicle = {
        "id": "chronicle_protocol_correctness_first_stepping_stone",
        "sector": "protocol_and_smart_contract_correctness",
        "parent_business": parent["title"],
        "winning_seed": winner_id,
        "frozen_sub_pack": governance_pack["id"],
        "sector_stepping_stone": protocol_pack["id"],
        "adjacent_proof_passed": scorecard["passes"]["adjacent_mandate_proof"],
        "timestamp": now,
    }
    write_json(OUT / "proof_docket" / "chronicle_entry.json", chronicle)

    proof_docket = {
        "claim": "Synthetic flagship claim: frozen protocol assurance capability improved adjacent mandate performance under control-vs-treatment assay.",
        "constitutional_frame": {
            "order": ["identity", "proof", "settlement", "governance"],
            "invariant": [
                "no value without evidence",
                "no autonomy without authority",
                "no settlement without validation"
            ],
        },
        "parent_business": parent,
        "mandate_1_summary": mandate_1_summary,
        "mandate_2_control_summary": control,
        "mandate_2_treatment_summary": treatment,
        "scorecard": scorecard,
        "settlement_release_packet": release_gate_packet,
        "chronicle_entry": chronicle,
        "governance_ruling": governance_ruling,
        "sovereign_or_fail_closed_artifact": sovereign_or_ruling,
        "synthetic_disclaimer": "This docket is synthetic, local, replayable, and falsifiable. It is not a real-world proof pack.",
    }
    write_json(OUT / "proof_docket" / "proof_docket.json", proof_docket)

    md = f"""# Protocol Smart-Contract Correctness Flagship Demo Report

**Synthetic disclaimer:** This report is synthetic, local, replayable, and falsifiable. It is not a real-world proof.

## Sector and parent business
- Sector: protocol and smart-contract correctness
- Parent business: {parent['title']}
- Why first wedge: objective, replayable, fast to review, reusable primitives, commercially legible.

## Nova-Seed assay (Mandate 1)
Winner: **{winner_id}**

| Seed | AUP | First accepted step | Rework | Evidence | Unsupported claim rate | Package quality |
|---|---:|---:|---:|---:|---:|---:|
"""
    for result in mandate_1_summary["results"]:
        m = result["metrics"]
        md += f"| {result['seed']} | {m['accepted_usefulness_points']} | {m['time_to_first_accepted_output']} | {m['repair_rework']:.3f} | {m['evidence_completeness']:.3f} | {m['unsupported_claim_rate']:.3f} | {m['packageable_artifact_quality']:.3f} |\n"

    cmp = scorecard["comparison"]
    md += f"""

## Frozen capability packages
- Sub-pack: `GovernanceValidationPack-v1`
- Sector stepping stone: `ProtocolAssurancePack-v1`

## Adjacent mandate (Mandate 2) control vs treatment
- Control AOY: {control['metrics']['aoy']}
- Treatment AOY: {treatment['metrics']['aoy']}
- AOY uplift: {_pct(cmp['aoy_uplift'])}
- Speed uplift: {_pct(cmp['speed_uplift'])}
- Repair/rework reduction: {_pct(cmp['repair_rework_reduction'])}
- Evidence completeness uplift: {_pct(cmp['evidence_completeness_uplift'])}
- Safety regression: {'YES' if cmp['safety_regression'] else 'NO'}
- Package dependence rate: {_pct(cmp['package_dependence_rate'])}

## Threshold ruling
- Adjacent-mandate proof: **{'PASS' if scorecard['passes']['adjacent_mandate_proof'] else 'FAIL'}**

## Sovereign emission
- Artifact: `{sovereign_or_ruling['id']}`
- Status: `{sovereign_or_ruling['status']}`
"""
    write_text(OUT / "reports" / "report.md", md)

    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Protocol Correctness Flagship Demo</title>
<style>
body{{font-family:Inter,Arial,sans-serif;background:#0b1020;color:#e5e7eb;margin:0;padding:24px;line-height:1.5}}
.wrap{{max-width:1100px;margin:0 auto}}
.card{{background:#111827;border:1px solid #334155;border-radius:14px;padding:18px;margin-bottom:16px}}
h1,h2{{margin:0 0 12px 0}}
small{{color:#94a3b8}}
table{{width:100%;border-collapse:collapse}}th,td{{border-bottom:1px solid #334155;padding:8px;text-align:left}}
.pass{{color:#34d399;font-weight:700}}.fail{{color:#f87171;font-weight:700}}
.kpi{{font-size:1.1rem;font-weight:700}}
.badge{{display:inline-block;padding:4px 10px;border:1px solid #475569;border-radius:999px;background:#1f2937}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
</style></head><body><div class='wrap'>
<div class='card'>
<span class='badge'>Synthetic flagship demo</span>
<h1>Protocol + Smart-Contract Correctness</h1>
<small>Front-door wedge explanation: sector → parent business → seeds → assay → stepping stone → sovereign candidate.</small>
<p><strong>Disclaimer:</strong> synthetic, local, replayable, falsifiable; not a real-world proof pack.</p>
</div>
<div class='card'>
<h2>Parent business: {parent['title']}</h2>
<p>{parent['review_posture']}</p>
<p><strong>Constitutional order:</strong> identity → proof → settlement → governance</p>
<p><strong>Invariant:</strong> no value without evidence; no autonomy without authority; no settlement without validation.</p>
</div>
<div class='card'>
<h2>Mandate 1 Nova-Seed assay winner: {winner_id}</h2>
<table><tr><th>Seed</th><th>AUP</th><th>First accepted</th><th>Rework</th><th>Evidence</th><th>Unsupported rate</th><th>Package quality</th></tr>
"""
    for result in mandate_1_summary["results"]:
        m = result["metrics"]
        html += f"<tr><td>{result['seed']}</td><td>{m['accepted_usefulness_points']}</td><td>{m['time_to_first_accepted_output']}</td><td>{m['repair_rework']}</td><td>{m['evidence_completeness']}</td><td>{m['unsupported_claim_rate']}</td><td>{m['packageable_artifact_quality']}</td></tr>"
    html += f"""
</table>
<p>Frozen sub-pack: <code>GovernanceValidationPack-v1</code> → promoted stepping stone: <code>ProtocolAssurancePack-v1</code>.</p>
</div>
<div class='card grid'>
<div>
<h2>Mandate 2 Control</h2>
<p>AOY: <span class='kpi'>{control['metrics']['aoy']}</span></p>
<p>Time to first accepted: {control['metrics']['time_to_first_accepted_output']}</p>
<p>Repair/rework: {control['metrics']['repair_rework']}</p>
<p>Evidence completeness: {control['metrics']['evidence_completeness']}</p>
</div>
<div>
<h2>Mandate 2 Treatment</h2>
<p>AOY: <span class='kpi'>{treatment['metrics']['aoy']}</span></p>
<p>Time to first accepted: {treatment['metrics']['time_to_first_accepted_output']}</p>
<p>Repair/rework: {treatment['metrics']['repair_rework']}</p>
<p>Evidence completeness: {treatment['metrics']['evidence_completeness']}</p>
<p>Package dependence: {treatment['metrics']['package_dependence_rate']}</p>
</div>
</div>
<div class='card'>
<h2>Adjacent-mandate threshold scorecard</h2>
<ul>
<li>AOY uplift: {_pct(cmp['aoy_uplift'])}</li>
<li>Speed uplift: {_pct(cmp['speed_uplift'])}</li>
<li>Repair/rework reduction: {_pct(cmp['repair_rework_reduction'])}</li>
<li>Evidence completeness uplift: {_pct(cmp['evidence_completeness_uplift'])}</li>
<li>Safety regression: {'YES' if cmp['safety_regression'] else 'NO'}</li>
<li>Package dependence rate: {_pct(cmp['package_dependence_rate'])}</li>
</ul>
<p>Ruling: <span class='{'pass' if scorecard['passes']['adjacent_mandate_proof'] else 'fail'}'>{'PASS' if scorecard['passes']['adjacent_mandate_proof'] else 'FAIL'}</span></p>
<p>Sovereign artifact/ruling emitted: <code>{sovereign_or_ruling['id']}</code></p>
</div>
</div></body></html>"""
    write_text(OUT / "reports" / "report.html", html)

    if assert_mode:
        assert winner_id == "invariant_library", "Expected deterministic winner invariant_library"
        assert (OUT / "capability_package" / "GovernanceValidationPack-v1.json").exists()
        assert (OUT / "capability_package" / "ProtocolAssurancePack-v1.json").exists()
        assert (OUT / "scorecard" / "adjacent_mandate_scorecard.json").exists()
        assert (OUT / "proof_docket" / "governance_ruling.json").exists()

    return {
        "winner": winner_id,
        "adjacent_mandate_proof": scorecard["passes"]["adjacent_mandate_proof"],
        "sovereign_artifact": sovereign_or_ruling["id"],
    }


def run_demo_cli():
    parser = argparse.ArgumentParser(description="Run protocol correctness flagship demo")
    parser.add_argument("--assert", action="store_true", dest="assert_mode", help="Run with deterministic assertions")
    args = parser.parse_args()
    result = run_demo(assert_mode=args.assert_mode)
    print(f"Winner seed: {result['winner']}")
    print(f"Adjacent proof: {'PASS' if result['adjacent_mandate_proof'] else 'FAIL'}")
    print(f"Sovereign artifact: {result['sovereign_artifact']}")
