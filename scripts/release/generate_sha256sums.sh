#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
ARTIFACT_DIR="${ROOT_DIR}/release/artifacts"
OUT_FILE="${ARTIFACT_DIR}/SHA256SUMS"

find "${ARTIFACT_DIR}" -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > "${OUT_FILE}"

echo "Wrote ${OUT_FILE}"
