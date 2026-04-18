const API = 'http://localhost:8000';

async function fetchJson(path) {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${path}`);
  return res.json();
}

async function load() {
  const summary = await fetchJson('/dashboard/summary');
  for (const [k, v] of Object.entries(summary)) {
    const el = document.getElementById(k);
    if (el) el.textContent = v;
  }

  const reviewerLedger = await fetchJson('/dashboard/reviewer-ledger');
  document.getElementById('reviewerLedger').textContent = JSON.stringify(reviewerLedger.items, null, 2);

  const councilSeats = await fetchJson('/dashboard/council-seats');
  document.getElementById('councilSeats').textContent = JSON.stringify(councilSeats.items, null, 2);

  window.__dashboardSnapshot = {
    generatedAt: new Date().toISOString(),
    summary,
    reviewerLedger: reviewerLedger.items,
    councilSeats: councilSeats.items,
  };
}

function exportJson() {
  const blob = new Blob([JSON.stringify(window.__dashboardSnapshot || {}, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'nova-dashboard-snapshot.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

function exportPng() {
  const node = document.getElementById('dashboardSnapshot');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600"><foreignObject width="100%" height="100%">${new XMLSerializer().serializeToString(node)}</foreignObject></svg>`;
  const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(blob);

  const img = new Image();
  img.onload = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 1600;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    canvas.toBlob((png) => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(png);
      a.download = 'nova-dashboard-snapshot.png';
      a.click();
      URL.revokeObjectURL(a.href);
    });
    URL.revokeObjectURL(url);
  };
  img.src = url;
}

document.getElementById('refreshBtn').addEventListener('click', () => load().catch(console.error));
document.getElementById('exportJsonBtn').addEventListener('click', exportJson);
document.getElementById('exportPngBtn').addEventListener('click', exportPng);

load().catch(console.error);
