import hre from "hardhat";
import { assertSafetyFlag, getEnv } from "./env";
import { assertOwnership, deployComposite, getAddressMap, type CoreContracts, roleStateSummary } from "./contracts";
import { artifactHint, deployedBytecodeHash, deploymentOutputDir, newBaseManifest, writeDeploymentArtifacts } from "./deployment";
import { postcheckMarkdown } from "./report";

export async function runDeployment(networkName: "mainnet" | "sepolia" | "mainnet-fork", options?: { enforceGate?: boolean; outputNetworkName?: string; }): Promise<{ outDir: string; addresses: Record<string, string>; contracts: CoreContracts; }> {
  const env = getEnv();
  const [deployer] = await hre.ethers.getSigners();
  const chain = await hre.ethers.provider.getNetwork();

  if (options?.enforceGate !== false) {
    if (networkName === "mainnet") {
      assertSafetyFlag("ALLOW_DEPLOY_TO_MAINNET", "Mainnet deployment");
    }
    if (networkName === "sepolia") {
      assertSafetyFlag("ALLOW_DEPLOY_TO_SEPOLIA", "Sepolia deployment");
    }
  }

  const contracts = await deployComposite({
    initialOwner: env.ADMIN_OWNER_ADDRESS,
    rewardToken: env.AGI_TOKEN_ADDRESS,
    agiJobManager: env.AGIJOBMANAGER_ADDRESS
  });

  await assertOwnership(contracts, env.ADMIN_OWNER_ADDRESS);

  const addresses = getAddressMap(contracts);

  const constructorArgsByName: Record<string, unknown[]> = {
    AlphaNovaSeedV25: [env.ADMIN_OWNER_ADDRESS],
    SignedAttestationVerifierV25: [env.ADMIN_OWNER_ADDRESS],
    ThresholdNetworkAdapterV25: [env.ADMIN_OWNER_ADDRESS, addresses.SignedAttestationVerifierV25],
    ReviewerRewardTreasuryV25: [env.ADMIN_OWNER_ADDRESS, env.AGI_TOKEN_ADDRESS],
    CouncilGovernanceV25: [env.ADMIN_OWNER_ADDRESS],
    ChallengePolicyModuleV25: [env.ADMIN_OWNER_ADDRESS],
    NovaSeedRegistryV25: [
      env.ADMIN_OWNER_ADDRESS,
      addresses.AlphaNovaSeedV25,
      addresses.ThresholdNetworkAdapterV25,
      addresses.ReviewerRewardTreasuryV25,
      addresses.CouncilGovernanceV25,
      addresses.ChallengePolicyModuleV25
    ],
    NovaSeedWorkflowAdapterV25: [env.ADMIN_OWNER_ADDRESS, addresses.NovaSeedRegistryV25, env.AGIJOBMANAGER_ADDRESS]
  };

  const manifest = newBaseManifest({
    network: options?.outputNetworkName ?? networkName,
    chainId: Number(chain.chainId),
    deployer: deployer.address,
    adminOwner: env.ADMIN_OWNER_ADDRESS,
    pauserAddress: env.PAUSER_ADDRESS,
    treasuryAddress: env.TREASURY_ADDRESS,
    agiTokenAddress: env.AGI_TOKEN_ADDRESS,
    agiJobManagerAddress: env.AGIJOBMANAGER_ADDRESS
  });

  for (const [name, address] of Object.entries(addresses)) {
    const bytecodeHash = await deployedBytecodeHash(hre, address);
    const hint = artifactHint(name);
    manifest.contracts.push({
      name,
      address,
      constructorArgs: constructorArgsByName[name] ?? [],
      deployedBytecodeHash: bytecodeHash,
      artifactPath: hint.artifactPath,
      buildInfoHint: hint.buildInfoHint,
      verificationStatus: "pending"
    });
  }

  const roleSummary = await roleStateSummary(contracts, env.ADMIN_OWNER_ADDRESS);
  const postcheck = await postcheckMarkdown({
    networkName: options?.outputNetworkName ?? networkName,
    chainId: chain.chainId,
    contracts,
    expectedOwner: env.ADMIN_OWNER_ADDRESS,
    rewardToken: env.AGI_TOKEN_ADDRESS,
    agiJobManager: env.AGIJOBMANAGER_ADDRESS
  });

  const handoff = `# Ownership and role handoff status\n\n${roleSummary}\n\n` +
    `## Transfer status\n` +
    `- Initial owner set at deployment: ${env.ADMIN_OWNER_ADDRESS}\n` +
    `- Additional transfer required: only if temporary owner deployment path was used.\n`;

  const outDir = deploymentOutputDir(options?.outputNetworkName ?? networkName);
  writeDeploymentArtifacts(outDir, manifest, addresses, postcheck, handoff);

  return { outDir, addresses, contracts };
}
