const API = 'http://localhost:8000';
let snapshotState = {};

function showPage(id) {
  document.querySelectorAll('.page').forEach((p) => p.classList.add('hidden'));
  document.getElementById(id)?.classList.remove('hidden');
}

async function loadJSON(path, targetId) {
  const res = await fetch(`${API}${path}`);
  const data = await res.json();
  snapshotState[path] = data;
  const el = document.getElementById(targetId);
  if (el) el.textContent = JSON.stringify(data, null, 2);
  return data;
}

async function loadSummary() {
  const data = await loadJSON('/dashboard/summary', 'rounds_json');
  for (const [k, v] of Object.entries(data)) {
    const el = document.getElementById(k);
    if (el) el.textContent = v;
  }
}

async function loadAll() {
  await loadSummary();
  await loadJSON('/governance/reviewer-ledger', 'ledger_json');
  await loadJSON('/governance/council-seats', 'seats_json');
  await loadJSON('/metrics', 'alerts_json');
  await loadJSON('/ready', 'lineage_json');
  const provenance = {
    checksums: 'release/artifacts/SHA256SUMS',
    verifyDoc: 'docs/verify-release.md',
    version: '2.6.0-rc.0',
  };
  snapshotState['/release/provenance'] = provenance;
  document.getElementById('provenance_json').textContent = JSON.stringify(provenance, null, 2);
}

function exportSnapshotJSON() {
  const blob = new Blob([JSON.stringify(snapshotState, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'nova-seeds-dashboard-snapshot.json';
  a.click();
}

async function exportSnapshotPNG() {
  const root = document.getElementById('snapshot-root');
  const canvas = await html2canvas(root);
  const url = canvas.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = url;
  a.download = 'nova-seeds-dashboard-snapshot.png';
  a.click();
}

loadAll().catch((err) => console.error('Dashboard load failed', err));
