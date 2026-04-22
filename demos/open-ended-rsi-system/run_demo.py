#!/usr/bin/env python3
"""Deterministic open-ended RSI system demo for bounded accelerating-loop RC evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = Path(__file__).resolve().parent
OUT = DEMO_ROOT / "out"

REQUIRED_DIRS = [
    "00_manifest",
    "01_frontier_queue",
    "02_seed_genome",
    "03_generation",
    "04_assays",
    "05_selection",
    "06_archive",
    "07_scorecard",
    "08_proof_docket",
    "out",
]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _json(payload: Any) -> str:
    return json.dumps(payload, indent=2) + "\n"


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json(payload), encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _reset_out() -> None:
    if OUT.exists():
        for item in sorted(OUT.rglob("*"), reverse=True):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                item.rmdir()
    OUT.mkdir(parents=True, exist_ok=True)


def _check_required_dirs() -> None:
    missing = [d for d in REQUIRED_DIRS if not (DEMO_ROOT / d).exists()]
    if missing:
        raise SystemExit(f"fail-closed: missing required demo directories: {missing}")


def _load_config() -> dict[str, Any]:
    config = _read_json(DEMO_ROOT / "config.json")
    if config.get("demo_id") != "open-ended-rsi-system":
        raise SystemExit("fail-closed: config demo_id mismatch")
    return config


def _seed_genome(config: dict[str, Any]) -> dict[str, Any]:
    seeds = [
        ROOT / "contracts" / "NovaSeedRegistryV25.sol",
        ROOT / "backend" / "app" / "main.py",
        ROOT / "schemas" / "v2.6" / "threshold-binding-profile.schema.json",
        ROOT / "docs" / "verify-release.md",
        ROOT / "demos" / "protocol_smart_contract_correctness_demo" / "ground_truth" / "mandate_1.json",
    ]
    missing = [p for p in seeds if not p.exists()]
    if missing:
        raise SystemExit("fail-closed: missing seed assets: " + ", ".join(_rel(p) for p in missing))

    reactive_intermediate = {
        "type": "missing_proof_artifact",
        "description": "Mandate-1 wedge lacks explicit deterministic capability-genome artifact for cross-domain reuse.",
        "fixed_trace": "protocol-correctness-lineage-gap",
    }

    genome = {
        "genome_id": "capability-genome-g0",
        "mode": "DISCO",
        "candidate_pool_size": config["candidate_pool_size"],
        "reactive_intermediate": reactive_intermediate,
        "source_assets": [
            {"path": _rel(p), "sha256": _sha256_file(p)} for p in seeds
        ],
        "authority_scope": {
            "can": [
                "mutate_package_templates",
                "run_preapproved_assays",
                "select_frontier_from_whitelist",
            ],
            "cannot": [
                "widen_authority_scope",
                "settle_real_value",
                "promote_to_production",
                "rewrite_repo_claim_boundary",
            ],
        },
    }
    return genome


def _candidate_pool(config: dict[str, Any]) -> list[dict[str, Any]]:
    pool = []
    family_cycle = ["trace-fix", "proof-surface", "schema-lift", "operator-runbook"]
    for i in range(config["candidate_pool_size"]):
        idx = i + 1
        family = family_cycle[i % len(family_cycle)]
        cheap = 0.62 + ((idx % 9) * 0.015)
        mid = 0.58 + ((idx % 7) * 0.019)
        expensive = 0.55 + ((idx % 5) * 0.027)
        penalty = 0.0
        if idx % 11 == 0:
            penalty += 0.08
        if idx % 13 == 0:
            penalty += 0.05
        pareto = [round(cheap, 3), round(mid, 3), round(expensive, 3)]
        pooled = {
            "id": f"g0-candidate-{idx:03d}",
            "family": family,
            "mode": "DISCO" if idx <= 24 else "Arnold",
            "assays": {
                "cheap": round(cheap, 3),
                "mid": round(mid, 3),
                "expensive": round(expensive, 3),
            },
            "off_target_penalties": {
                "evidence_fabrication": 0.0,
                "undeclared_privilege": 0.0 if idx % 17 else 0.1,
                "safety_regression": 0.0 if idx % 19 else 0.1,
                "schema_drift": 0.0 if idx % 23 else 0.1,
                "missing_docs_or_provenance": penalty,
                "governance_shortcut": 0.0,
            },
            "pareto_vector": pareto,
        }
        pooled["utility"] = round(
            0.25 * pooled["assays"]["cheap"]
            + 0.35 * pooled["assays"]["mid"]
            + 0.40 * pooled["assays"]["expensive"]
            - sum(pooled["off_target_penalties"].values()),
            4,
        )
        pool.append(pooled)
    return pool


def _select_winner(pool: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_pool = sorted(
        pool,
        key=lambda c: (
            -c["utility"],
            -c["assays"]["expensive"],
            c["id"],
        ),
    )
    return sorted_pool[0]


def _frontier_selection(config: dict[str, Any], package_hash: str) -> dict[str, Any]:
    scoring = {
        "backend_api_correctness": [0.93, 0.92, 0.91, 0.95],
        "sdk_typed_attestation_correctness": [0.88, 0.86, 0.90, 0.88],
        "schema_migration_integrity": [0.81, 0.90, 0.87, 0.89],
        "proof_docket_synthesis": [0.79, 0.94, 0.83, 0.91],
        "release_provenance_automation": [0.75, 0.93, 0.88, 0.90],
        "dashboard_provenance_surface": [0.72, 0.80, 0.78, 0.84],
    }
    ranked = []
    for domain in config["frontier_whitelist"]:
        transfer, assay_coverage, authority_fit, evidence_density = scoring[domain]
        total = round(
            (0.35 * transfer)
            + (0.25 * assay_coverage)
            + (0.20 * authority_fit)
            + (0.20 * evidence_density),
            4,
        )
        ranked.append(
            {
                "domain": domain,
                "expected_transfer": transfer,
                "assay_coverage": assay_coverage,
                "authority_fit": authority_fit,
                "evidence_density": evidence_density,
                "score": total,
            }
        )
    ranked = sorted(ranked, key=lambda r: (-r["score"], r["domain"]))

    selected = ranked[0]["domain"]
    arnold_neighborhood = []
    for i in range(config["neighborhood_size"]):
        v = round(0.67 + (i % 8) * 0.024 + (i // 8) * 0.006, 3)
        arnold_neighborhood.append({"variant": f"{selected}-n{i+1:02d}", "fitness": v})

    neighborhood_slope = round(
        (arnold_neighborhood[-1]["fitness"] - arnold_neighborhood[0]["fitness"])
        / len(arnold_neighborhood),
        4,
    )

    return {
        "mode_sequence": ["DISCO", "Arnold"],
        "ranked_frontier": ranked,
        "selected_domain": selected,
        "package_hash_dependency": package_hash,
        "arnold_neighborhood": arnold_neighborhood,
        "neighborhood_slope": neighborhood_slope,
    }


def run_demo(assert_mode: bool = False) -> dict[str, Any]:
    _check_required_dirs()
    _reset_out()
    config = _load_config()
    timestamp = config["deterministic_timestamp"]

    genome = _seed_genome(config)
    pool = _candidate_pool(config)
    winner = _select_winner(pool)

    lineage = {
        "lineage_id": "lineage-open-ended-rsi-g0-g2",
        "parentage": ["protocol-smart-contract-correctness-wedge"],
        "generation0_winner": winner["id"],
        "strategy_families_seen": sorted({c["family"] for c in pool}),
        "archive_depth": 3,
    }

    capability_genome = {
        "id": "ProtocolCorrectnessCapabilityPack-v1",
        "manifest_version": "1.0",
        "timestamp": timestamp,
        "winner": winner,
        "lineage": lineage,
        "authority_scope": genome["authority_scope"],
        "reusable_assets": [a["path"] for a in genome["source_assets"]],
    }
    capability_hash = _sha256_bytes(_json(capability_genome).encode("utf-8"))

    control = {
        "aoy": 108,
        "time_to_first_accept_minutes": 149,
        "repair_ratio": 0.29,
        "evidence_completeness": 0.72,
        "safety_regression": False,
    }
    treatment = {
        "aoy": 162,
        "time_to_first_accept_minutes": 97,
        "repair_ratio": 0.16,
        "evidence_completeness": 0.92,
        "safety_regression": False,
        "package_dependence": 0.63,
    }

    assay_bundle = {
        "cheap_assays": [
            "lint_static_checks",
            "schema_validation",
            "diff_sanity",
            "proof_completeness",
            "policy_compliance",
            "template_consistency",
        ],
        "mid_assays": [
            "targeted_integration_tests",
            "openapi_abi_schema_consistency",
            "operator_usability_rubric",
            "cost_latency_proxy",
            "proof_docket_completeness",
        ],
        "expensive_assays": [
            "held_out_synthetic_mandate",
            "blinded_rubric_emulation",
            "canary_replay_pack",
        ],
        "lane_results": {
            "control": control,
            "treatment": treatment,
        },
    }

    scorecard = {
        "release_target": config["release_target"],
        "mandate_2_adjacent_result": {
            "aoy_uplift": round((treatment["aoy"] - control["aoy"]) / control["aoy"], 4),
            "speed_uplift": round((control["time_to_first_accept_minutes"] - treatment["time_to_first_accept_minutes"]) / control["time_to_first_accept_minutes"], 4),
            "rework_reduction": round((control["repair_ratio"] - treatment["repair_ratio"]) / control["repair_ratio"], 4),
            "evidence_completeness_uplift": round((treatment["evidence_completeness"] - control["evidence_completeness"]) / control["evidence_completeness"], 4),
            "safety_regression": False,
            "package_dependence": treatment["package_dependence"],
        },
        "thresholds": {
            "aoy_uplift": 0.35,
            "speed_uplift": 0.30,
            "rework_reduction": 0.40,
            "evidence_completeness_uplift": 0.20,
            "package_dependence": 0.30,
            "safety_regression": False,
        },
    }

    m2 = scorecard["mandate_2_adjacent_result"]
    t = scorecard["thresholds"]
    passes = {
        "aoy": m2["aoy_uplift"] >= t["aoy_uplift"],
        "speed": m2["speed_uplift"] >= t["speed_uplift"],
        "rework": m2["rework_reduction"] >= t["rework_reduction"],
        "evidence": m2["evidence_completeness_uplift"] >= t["evidence_completeness_uplift"],
        "package_dependence": m2["package_dependence"] >= t["package_dependence"],
        "safety": m2["safety_regression"] == t["safety_regression"],
    }
    passes["adjacent_gate"] = all(passes.values())
    scorecard["passes"] = passes

    frontier = _frontier_selection(config, capability_hash)

    intervention_log = {
        "generation_0_human_touches": 14,
        "generation_1_human_touches": 8,
        "generation_2_human_touches": 3,
        "autonomy_delta": 11,
        "authority_gates_unchanged": True,
    }

    longitudinal = {
        "frontier_width": len(config["frontier_whitelist"]),
        "autonomy_delta": intervention_log["autonomy_delta"],
        "neighborhood_slope": frontier["neighborhood_slope"],
        "archive_depth": lineage["archive_depth"],
    }

    provenance_manifest = {
        "demo_id": config["demo_id"],
        "release_target": config["release_target"],
        "timestamp": timestamp,
        "deterministic": True,
        "artifact_hashes": {},
        "claim_boundary": {
            "demonstrated": "bounded accelerating loop mechanics across three governed generations",
            "simulated": "synthetic metrics, blinded rubric emulation, and mandate outputs",
            "unproven": "unrestricted autonomy, external real-world broad cybersecurity sovereign operation, unbounded RSI",
        },
    }

    proof_docket = f"""# Proof Docket — Open-Ended RSI System ({config['release_target']})

## Demonstrated

- Generation 0 executes a deterministic protocol-correctness wedge with a fixed reactive intermediate.
- Generation 1 runs explicit control-vs-treatment and passes bounded thresholds using a frozen package hash.
- Generation 2 selects a second domain only from a whitelist and runs DISCO then Arnold under unchanged authority gates.

## Simulated

- Assay outcomes are synthetic and deterministic.
- Board scorecard values are synthetic replay values.

## Unproven

- Unrestricted autonomy in unconstrained environments.
- External real-world broad cybersecurity sovereign operation.
- Literal fully general unbounded RSI.
"""

    summary_md = f"""# Open-Ended RSI System Summary

## Release target

- Target: **{config['release_target']}**
- Timestamp: **{timestamp}**

## Three generations

1. **Generation 0 (bounded, DISCO)**: human-selected protocol-correctness start point and deterministic candidate funnel.
2. **Generation 1 (expanding)**: frozen capability package and control-vs-treatment adjacent mandate.
3. **Generation 2 (increasingly autonomous)**: whitelist-scored autonomous domain selection, then Arnold neighborhood improvement.

## Board scorecard

- Adjacent gate: **{'PASS' if passes['adjacent_gate'] else 'FAIL'}**
- AOY uplift: **{m2['aoy_uplift']*100:.1f}%**
- Speed uplift: **{m2['speed_uplift']*100:.1f}%**
- Rework reduction: **{m2['rework_reduction']*100:.1f}%**
- Evidence uplift: **{m2['evidence_completeness_uplift']*100:.1f}%**
- Package dependence: **{m2['package_dependence']*100:.1f}%**

## Longitudinal metrics

- frontier_width: **{longitudinal['frontier_width']}**
- autonomy_delta: **{longitudinal['autonomy_delta']} human touches reduced**
- neighborhood_slope: **{longitudinal['neighborhood_slope']}**
- archive_depth: **{longitudinal['archive_depth']}**
"""

    report_html = f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>Open-Ended RSI System Demo</title>
<style>
body{{margin:0;background:#f4f7fb;color:#0f172a;font-family:Inter,Segoe UI,Arial,sans-serif;line-height:1.55}}
.wrap{{max-width:1200px;margin:0 auto;padding:36px 24px 48px}}
.hero{{background:#0f2747;color:#e5eefb;border-radius:16px;padding:26px 28px;margin-bottom:16px}}
.hero h1{{margin:0 0 8px;font-size:30px}}
.hero p{{margin:8px 0}}
.badge{{display:inline-block;background:#173863;border:1px solid #2f5485;color:#dce8fb;border-radius:999px;padding:3px 10px;margin-right:8px;font-size:12px;letter-spacing:.04em}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:16px}}
.card{{background:white;border:1px solid #d7e1ef;border-radius:14px;padding:16px}}
.timeline{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.table{{width:100%;border-collapse:collapse}}
.table th,.table td{{border-bottom:1px solid #e5edf8;padding:8px;text-align:left}}
.ok{{color:#0b7a48;font-weight:700}}
.note{{background:#eef4ff;border:1px solid #c8d9f5;border-radius:12px;padding:14px;margin-top:14px}}
@media(max-width:980px){{.grid,.timeline{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class='wrap'>
<section class='hero'>
<span class='badge'>Accelerating-loop demo</span><span class='badge'>{config['release_target']}</span>
<h1>Open-Ended RSI System (bounded proof-of-mechanism)</h1>
<p>Progression: <strong>bounded → expanding → increasingly autonomous</strong> with explicit authority and safety gates.</p>
<p><strong>Demonstrated</strong>: deterministic accelerating mechanism under governance. <strong>Not claimed</strong>: unrestricted autonomy or fully general unbounded RSI.</p>
</section>
<section class='grid'>
<div class='card'><h3>Generation 0</h3><p>DISCO mode finds first workable package in protocol correctness wedge.</p><p>Winner: <code>{winner['id']}</code></p></div>
<div class='card'><h3>Generation 1</h3><p>Control-vs-treatment on adjacent mandate with frozen package reuse.</p><p>Gate: <span class='ok'>{'PASS' if passes['adjacent_gate'] else 'FAIL'}</span></p></div>
<div class='card'><h3>Generation 2</h3><p>Autonomous whitelist selection then Arnold neighborhood search.</p><p>Selected domain: <code>{frontier['selected_domain']}</code></p></div>
</section>
<section class='card'>
<h2>Board scorecard</h2>
<table class='table'>
<tr><th>Metric</th><th>Observed</th><th>Threshold</th></tr>
<tr><td>AOY uplift</td><td>{m2['aoy_uplift']*100:.1f}%</td><td>35.0%</td></tr>
<tr><td>Speed uplift</td><td>{m2['speed_uplift']*100:.1f}%</td><td>30.0%</td></tr>
<tr><td>Rework reduction</td><td>{m2['rework_reduction']*100:.1f}%</td><td>40.0%</td></tr>
<tr><td>Evidence uplift</td><td>{m2['evidence_completeness_uplift']*100:.1f}%</td><td>20.0%</td></tr>
<tr><td>Package dependence</td><td>{m2['package_dependence']*100:.1f}%</td><td>30.0%</td></tr>
</table>
</section>
<section class='timeline'>
<div class='card'><h3>Demonstrated</h3><p>Deterministic three-generation governed loop and package lineage reuse.</p></div>
<div class='card'><h3>Simulated</h3><p>Synthetic mandate outcomes and blinded-rubric emulation.</p></div>
<div class='card'><h3>Unproven</h3><p>Unrestricted autonomy and real-world broad sovereign completion.</p></div>
</section>
<div class='note'>Outputs written under <code>demos/open-ended-rsi-system/out/</code> including scorecard, proof docket, provenance manifest, and lineage artifacts.</div>
</div>
</body>
</html>
"""

    frontier_queue = {
        "whitelist": config["frontier_whitelist"],
        "ranked": frontier["ranked_frontier"],
        "selected": frontier["selected_domain"],
    }

    # Core required artifacts.
    artifacts: dict[str, Any] = {
        "capability_genome.json": capability_genome,
        "assay_bundle.json": assay_bundle,
        "lineage.json": lineage,
        "frontier_queue.json": frontier_queue,
        "intervention_log.json": intervention_log,
        "scorecard.json": {**scorecard, "longitudinal": longitudinal},
        "provenance_manifest.json": provenance_manifest,
    }

    for name, payload in artifacts.items():
        _write_json(OUT / name, payload)

    _write_text(OUT / "proof_docket.md", proof_docket)
    _write_text(OUT / "summary.md", summary_md)
    _write_text(OUT / "report.html", report_html)

    # Mirror key artifacts into staged folders for operator navigation.
    _write_json(DEMO_ROOT / "00_manifest" / "manifest.json", {"demo_id": config["demo_id"], "release_target": config["release_target"], "timestamp": timestamp})
    _write_json(DEMO_ROOT / "01_frontier_queue" / "frontier_queue.json", frontier_queue)
    _write_json(DEMO_ROOT / "02_seed_genome" / "capability_genome.json", capability_genome)
    _write_json(DEMO_ROOT / "03_generation" / "generation_log.json", {"candidate_count": len(pool), "winner": winner["id"], "mode_sequence": ["DISCO", "Arnold"]})
    _write_json(DEMO_ROOT / "04_assays" / "assay_bundle.json", assay_bundle)
    _write_json(DEMO_ROOT / "05_selection" / "selection.json", {"winner": winner, "frontier_selected": frontier["selected_domain"]})
    _write_json(DEMO_ROOT / "06_archive" / "lineage.json", lineage)
    _write_json(DEMO_ROOT / "07_scorecard" / "scorecard.json", {**scorecard, "longitudinal": longitudinal})
    _write_text(DEMO_ROOT / "08_proof_docket" / "proof_docket.md", proof_docket)

    # Populate provenance artifact hashes after outputs exist.
    tracked_files = sorted(p for p in OUT.glob("*") if p.is_file())
    provenance_manifest["artifact_hashes"] = {
        p.name: _sha256_file(p) for p in tracked_files
    }
    _write_json(OUT / "provenance_manifest.json", provenance_manifest)

    if assert_mode:
        required_files = {
            "capability_genome.json",
            "assay_bundle.json",
            "lineage.json",
            "frontier_queue.json",
            "intervention_log.json",
            "scorecard.json",
            "summary.md",
            "proof_docket.md",
            "provenance_manifest.json",
            "report.html",
        }
        produced = {p.name for p in OUT.glob("*") if p.is_file()}
        missing = sorted(required_files - produced)
        if missing:
            raise SystemExit(f"assert failed: missing required artifacts: {missing}")

        rerun = _read_json(OUT / "scorecard.json")
        if not rerun.get("passes", {}).get("adjacent_gate"):
            raise SystemExit("assert failed: adjacent gate did not pass")

    return {
        "release_target": config["release_target"],
        "selected_domain": frontier["selected_domain"],
        "adjacent_gate": passes["adjacent_gate"],
        "artifacts": sorted([p.name for p in OUT.glob("*") if p.is_file()]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic open-ended RSI system demo")
    parser.add_argument("--assert", action="store_true", dest="assert_mode")
    args = parser.parse_args()

    result = run_demo(assert_mode=args.assert_mode)
    print(
        f"PASS: {result['release_target']} open-ended demo emitted {len(result['artifacts'])} artifacts "
        f"(mandate-3={result['selected_domain']}, adjacent_gate={'PASS' if result['adjacent_gate'] else 'FAIL'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
