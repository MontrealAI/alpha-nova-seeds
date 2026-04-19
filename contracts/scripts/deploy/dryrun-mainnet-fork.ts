import hre from "hardhat";
import { runDeployment } from "../lib/run-deployment";

async function main(): Promise<void> {
  if (hre.network.name !== "hardhat") {
    throw new Error(`dryrun-mainnet-fork must run on hardhat network, got ${hre.network.name}`);
  }

  if (!process.env.MAINNET_RPC_URL) {
    throw new Error("MAINNET_RPC_URL is required to run fork dry-run.");
  }

  const result = await runDeployment("mainnet-fork", { enforceGate: false, outputNetworkName: "mainnet-fork" });
  console.log(`Mainnet fork dry-run complete. Artifacts: ${result.outDir}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
