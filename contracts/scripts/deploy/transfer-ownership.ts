import hre from "hardhat";
import { assertSafetyFlag, getEnv } from "../lib/env";

async function transfer(name: string, contractAddress: string, newOwner: string): Promise<void> {
  const contract = await hre.ethers.getContractAt("Ownable", contractAddress);
  const currentOwner = await contract.owner();
  if (currentOwner.toLowerCase() === newOwner.toLowerCase()) {
    console.log(`${name}: already owned by ${newOwner}`);
    return;
  }
  const tx = await contract.transferOwnership(newOwner);
  await tx.wait();
  console.log(`${name}: ownership transferred to ${newOwner}. tx=${tx.hash}`);
}

async function main(): Promise<void> {
  assertSafetyFlag("ALLOW_OWNERSHIP_TRANSFER", "Ownership transfer");
  const env = getEnv();

  const addresses = {
    AlphaNovaSeedV25: process.env.ALPHA_NOVA_SEED_ADDRESS,
    SignedAttestationVerifierV25: process.env.SIGNED_ATTESTATION_VERIFIER_ADDRESS,
    ThresholdNetworkAdapterV25: process.env.THRESHOLD_NETWORK_ADAPTER_ADDRESS,
    ReviewerRewardTreasuryV25: process.env.REVIEWER_REWARD_TREASURY_ADDRESS,
    CouncilGovernanceV25: process.env.COUNCIL_GOVERNANCE_ADDRESS,
    ChallengePolicyModuleV25: process.env.CHALLENGE_POLICY_MODULE_ADDRESS,
    NovaSeedRegistryV25: process.env.NOVA_SEED_REGISTRY_ADDRESS,
    NovaSeedWorkflowAdapterV25: process.env.NOVA_SEED_WORKFLOW_ADAPTER_ADDRESS
  };

  for (const [name, address] of Object.entries(addresses)) {
    if (!address) {
      throw new Error(`Missing ${name} address in environment for transfer script.`);
    }
    await transfer(name, address, env.ADMIN_OWNER_ADDRESS);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
