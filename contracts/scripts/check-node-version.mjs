#!/usr/bin/env node
const [major, minor] = process.versions.node.split('.').map(Number);
const ok = major > 22 || (major === 22 && minor >= 10);

if (!ok) {
  console.error(`Node.js ${process.versions.node} detected. contracts workspace requires Node.js >=22.10.0 for Hardhat 3.`);
  process.exit(1);
}
