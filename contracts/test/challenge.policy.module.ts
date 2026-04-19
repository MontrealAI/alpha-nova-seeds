import { expect } from "chai";
import hre from "hardhat";

describe("ChallengePolicyModuleV25 adjudication paths", function () {
  it("enforces policy/adjudicator controls and deterministic outcomes", async function () {
    const [owner, adjudicator, outsider] = await hre.ethers.getSigners();
    const module = await hre.ethers.deployContract("ChallengePolicyModuleV25", [owner.address]);

    const policyId = hre.ethers.id("policy:upheld");
    await expect(module.connect(outsider).setPolicy(policyId, 2, 5, 1, true)).to.be.revertedWithCustomError(
      module,
      "OwnableUnauthorizedAccount"
    );

    await module.connect(owner).setAdjudicator(adjudicator.address, true);
    await module.connect(owner).setPolicy(policyId, 2, 5, 1, true);

    const challengeId = hre.ethers.id("challenge:upheld");
    await expect(module.connect(outsider).recordVote(challengeId, policyId, true, 3, false)).to.be.revertedWith("NOT_ADJUDICATOR");

    await module.connect(adjudicator).recordVote(challengeId, policyId, true, 2, false);
    await module.connect(adjudicator).recordVote(challengeId, policyId, true, 3, false);
    await expect(module.connect(adjudicator).finalize(challengeId))
      .to.emit(module, "ChallengeAdjudicated")
      .withArgs(challengeId, 1n);

    const adjudication = await module.adjudications(challengeId);
    expect(adjudication.finalized).to.equal(true);
    expect(adjudication.outcome).to.equal(1n);

    await expect(module.connect(adjudicator).finalize(challengeId)).to.be.revertedWith("FINALIZED");

    const inactivePolicy = hre.ethers.id("policy:inactive");
    await module.connect(owner).setPolicy(inactivePolicy, 1, 1, 0, false);
    await expect(module.connect(adjudicator).recordVote(hre.ethers.id("challenge:inactive"), inactivePolicy, true, 1, false)).to.be
      .revertedWith("POLICY_INACTIVE");

    const warningPolicy = hre.ethers.id("policy:warn");
    const warningChallenge = hre.ethers.id("challenge:warn");
    await module.connect(owner).setPolicy(warningPolicy, 3, 10, 2, true);
    await module.connect(adjudicator).recordVote(warningChallenge, warningPolicy, false, 0, true);
    await module.connect(adjudicator).recordVote(warningChallenge, warningPolicy, false, 0, true);
    const warningOutcome = await module.connect(adjudicator).finalize.staticCall(warningChallenge);
    expect(warningOutcome).to.equal(3n);
    await module.connect(adjudicator).finalize(warningChallenge);
  });
});
