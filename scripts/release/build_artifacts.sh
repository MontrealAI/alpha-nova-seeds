#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/release/artifacts"
SRC_DIR="${OUT_DIR}/source"
CANON_DIR="${OUT_DIR}/canonical"

rm -rf "${SRC_DIR}" "${CANON_DIR}"
mkdir -p "${SRC_DIR}" "${CANON_DIR}"

# Source archive for reproducibility
GIT_SHA="$(git -C "${ROOT_DIR}" rev-parse HEAD)"
ARCHIVE="${SRC_DIR}/alpha-nova-seeds-${GIT_SHA}.tar.gz"
git -C "${ROOT_DIR}" archive --format=tar.gz --output="${ARCHIVE}" HEAD

# Canonical release payloads (ABI + schema + migrations + docs)
cp -f "${ROOT_DIR}/contracts/abi/NovaSeedRegistryV26RC.abi.json" "${CANON_DIR}/"
cp -f "${ROOT_DIR}/schemas/threshold/v2.6/decryption-attestation.schema.json" "${CANON_DIR}/"
cp -f "${ROOT_DIR}/schemas/threshold/v2.6/threshold-binding-profile.schema.json" "${CANON_DIR}/"
cp -f "${ROOT_DIR}/backend/migrations/001_init.sql" "${CANON_DIR}/"
cp -f "${ROOT_DIR}/backend/migrations/002_v26_hardening.sql" "${CANON_DIR}/"
cp -f "${ROOT_DIR}/docs/verify-release.md" "${CANON_DIR}/"
