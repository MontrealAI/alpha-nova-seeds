#!/usr/bin/env python3
"""Validate demo ladder links and role labels."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "README.md",
    ROOT / "demos" / "README.md",
    ROOT / "demos" / "protocol_smart_contract_correctness_demo" / "README.md",
    ROOT / "demos" / "adjacent_mandate_reuse_proof_demo" / "README.md",
    ROOT / "demos" / "adjacent_mandate_reuse_proof_real_v1" / "README.md",
]

REQUIRED_PATHS = [
    "demos/protocol_smart_contract_correctness_demo/",
    "demos/adjacent_mandate_reuse_proof_demo/",
    "demos/adjacent_mandate_reuse_proof_real_v1/",
    "demos/unbounded-rsi-system/",
]

REQUIRED_PHRASES = [
    "Flagship synthetic wedge demo",
    "Adjacent synthetic proof demo",
    "Real-world proof pack",
    "Accelerating-loop demo",
]


def main() -> int:
    errors: list[str] = []

    for file in FILES:
        if not file.exists():
            errors.append(f"missing file: {file.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for path in REQUIRED_PATHS:
        if path not in readme:
            errors.append(f"README missing demo path: {path}")
        if not (ROOT / path).exists():
            errors.append(f"README path target missing: {path}")

    demos_readme = (ROOT / "demos" / "README.md").read_text(encoding="utf-8")
    for phrase in REQUIRED_PHRASES:
        if phrase not in demos_readme:
            errors.append(f"demos/README.md missing phrase: {phrase}")

    for path in (ROOT / "demos").glob("*/README.md"):
        text = path.read_text(encoding="utf-8")
        if "../README.md" not in text:
            errors.append(f"missing ladder index link in {path.relative_to(ROOT)}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: demo ladder links and labels are coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
