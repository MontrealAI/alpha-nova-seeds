async function load() {
  const res = await fetch('http://localhost:8000/dashboard/summary');
  const data = await res.json();
  for (const [k,v] of Object.entries(data)) {
    const el = document.getElementById(k);
    if (el) el.textContent = v;
  }
}
load().catch(console.error);
