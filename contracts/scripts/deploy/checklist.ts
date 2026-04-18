import { getEnv } from "../lib/env";

const validateOnly = process.argv.includes("--validate-only");

async function main(): Promise<void> {
  const env = getEnv();

  const checklist = [
    ["ADMIN_OWNER_ADDRESS configured", Boolean(env.ADMIN_OWNER_ADDRESS)],
    ["AGI_TOKEN_ADDRESS configured", Boolean(env.AGI_TOKEN_ADDRESS)],
    ["AGIJOBMANAGER_ADDRESS configured", Boolean(env.AGIJOBMANAGER_ADDRESS)],
    ["Mainnet RPC configured", Boolean(env.MAINNET_RPC_URL)],
    ["Sepolia RPC configured", Boolean(env.SEPOLIA_RPC_URL)],
    ["Mainnet deploy gate", env.ALLOW_DEPLOY_TO_MAINNET === "true"],
    ["Sepolia deploy gate", env.ALLOW_DEPLOY_TO_SEPOLIA === "true"],
    ["Ownership transfer gate", env.ALLOW_OWNERSHIP_TRANSFER === "true"]
  ] as const;

  console.log("# Nova-Seeds deployment checklist");
  for (const [item, ok] of checklist) {
    console.log(`- [${ok ? "x" : " "}] ${item}`);
  }

  if (validateOnly) {
    console.log("\nValidation-only mode complete.");
    return;
  }

  console.log("\nFail-closed policy reminders:");
  console.log("- Contracts deploy with owner control only; no creator/signer/profile auto-activation.");
  console.log("- No script auto-unpauses or opens permissive policy flags.");
  console.log("- Review docs/mainnet-deployment.md before broadcast.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
