import { expect } from "chai";
import hre from "hardhat";

async function deployRegistryGraph() {
  const [owner, creator, reviewer] = await hre.ethers.getSigners();
  const rewardToken = await hre.ethers.deployContract("MockERC20", ["AGI", "AGI", hre.ethers.parseEther("1000000")]);
  const nft = await hre.ethers.deployContract("AlphaNovaSeedV25", [owner.address]);
  const verifier = await hre.ethers.deployContract("SignedAttestationVerifierV25", [owner.address]);
  const adapter = await hre.ethers.deployContract("ThresholdNetworkAdapterV25", [owner.address, await verifier.getAddress()]);
  const treasury = await hre.ethers.deployContract("ReviewerRewardTreasuryV25", [owner.address, await rewardToken.getAddress()]);
  const council = await hre.ethers.deployContract("CouncilGovernanceV25", [owner.address]);
  const challenge = await hre.ethers.deployContract("ChallengePolicyModuleV25", [owner.address]);
  const registry = await hre.ethers.deployContract("NovaSeedRegistryV25", [
    owner.address,
    await nft.getAddress(),
    await adapter.getAddress(),
    await treasury.getAddress(),
    await council.getAddress(),
    await challenge.getAddress()
  ]);

  await nft.connect(owner).setRegistry(await registry.getAddress());
  await treasury.connect(owner).setDistributor(await registry.getAddress(), true);
  await registry.connect(owner).setCreator(creator.address, true);

  return { owner, creator, reviewer, rewardToken, registry, council, treasury };
}

describe("NovaSeedRegistryV25 lifecycle", function () {
  it("rejects non-creator draft and enforces lifecycle ordering", async function () {
    const { creator, reviewer, registry } = await deployRegistryGraph();
    const seedId = hre.ethers.id("seed-1");
    const hash = hre.ethers.id("h");

    await expect(
      registry.connect(reviewer).draftSeed(seedId, hash, hash, hash, hash, hash, hash, hash, hash, hash, hash, "p", "s", "f", "t")
    ).to.be.revertedWith("NOT_CREATOR");

    await registry.connect(creator).draftSeed(seedId, hash, hash, hash, hash, hash, hash, hash, hash, hash, hash, "p", "s", "f", "t");
    await expect(registry.connect(creator).openReview(seedId)).to.be.revertedWith("BAD_STATE");

    await registry.connect(creator).sealSeed(seedId);
    await registry.connect(creator).openReview(seedId);
    await expect(registry.connect(creator).sealSeed(seedId)).to.be.revertedWith("BAD_STATE");
  });

  it("prevents duplicate reviews and accrues reward once per reviewer", async function () {
    const { owner, creator, reviewer, registry, council, treasury } = await deployRegistryGraph();
    const seedId = hre.ethers.id("seed-2");
    const hash = hre.ethers.id("h2");

    await registry.connect(creator).draftSeed(seedId, hash, hash, hash, hash, hash, hash, hash, hash, hash, hash, "p", "s", "f", "t");
    await registry.connect(creator).sealSeed(seedId);
    await registry.connect(creator).openReview(seedId);
    await council.connect(owner).openTerm();

    await registry.connect(reviewer).submitReview(seedId, 3, 1, hre.ethers.id("r1"));
    await expect(registry.connect(reviewer).submitReview(seedId, 3, 1, hre.ethers.id("r2"))).to.be.revertedWith("ALREADY_REVIEWED");
    expect(await treasury.accrued(reviewer.address)).to.equal(hre.ethers.parseEther("1"));
  });
});
