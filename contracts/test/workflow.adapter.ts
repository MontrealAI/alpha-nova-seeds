import { expect } from "chai";
import hre from "hardhat";

describe("NovaSeedWorkflowAdapterV25 workflow controls", function () {
  it("fail-closes invalid transitions and preserves owner-only workflow execution", async function () {
    const [owner, outsider] = await hre.ethers.getSigners();
    const registryView = await hre.ethers.deployContract("MockRegistryViewV25");
    const workflowEngine = await hre.ethers.deployContract("MockAGIJobManagerWorkflowV25");
    const mark = await hre.ethers.deployContract("MockMARKV25");
    const adapter = await hre.ethers.deployContract("NovaSeedWorkflowAdapterV25", [
      owner.address,
      await registryView.getAddress(),
      await workflowEngine.getAddress()
    ]);

    const seedId = hre.ethers.id("seed-workflow");
    const assayHash = hre.ethers.id("assay");

    await expect(adapter.connect(outsider).setMARK(await mark.getAddress())).to.be.revertedWithCustomError(
      adapter,
      "OwnableUnauthorizedAccount"
    );
    await adapter.connect(owner).setMARK(await mark.getAddress());
    expect(await adapter.mark()).to.equal(await mark.getAddress());

    await registryView.setState(seedId, 2n);
    await expect(adapter.connect(owner).createAssay(seedId, assayHash, 100n)).to.be.revertedWith("NOT_GREENLIT_OR_BLOOMING");

    await registryView.setState(seedId, 4n);
    const createTx = await adapter.connect(owner).createAssay(seedId, assayHash, 100n);
    const receipt = await createTx.wait();
    const parsed = receipt?.logs
      .map((l) => {
        try {
          return adapter.interface.parseLog(l);
        } catch {
          return null;
        }
      })
      .find((e) => e?.name === "AssayJobCreated");

    const jobId = parsed?.args.jobId as bigint;
    expect(jobId).to.equal(1n);

    await expect(adapter.connect(outsider).finalizeAssay(seedId, jobId)).to.be.revertedWithCustomError(
      adapter,
      "OwnableUnauthorizedAccount"
    );

    await adapter.connect(owner).finalizeAssay(seedId, jobId);
    const job = await workflowEngine.jobs(jobId);
    expect(job.finalized).to.equal(true);
  });

  it("propagates downstream workflow failures and fails closed", async function () {
    const [owner] = await hre.ethers.getSigners();
    const registryView = await hre.ethers.deployContract("MockRegistryViewV25");
    const failingEngine = await hre.ethers.deployContract("MockFailingAGIJobManagerWorkflowV25");
    const adapter = await hre.ethers.deployContract("NovaSeedWorkflowAdapterV25", [
      owner.address,
      await registryView.getAddress(),
      await failingEngine.getAddress()
    ]);

    const seedId = hre.ethers.id("seed-failing");
    await registryView.setState(seedId, 4n);

    await expect(adapter.connect(owner).createAssay(seedId, hre.ethers.id("x"), 1n)).to.be.revertedWith("CREATE_BLOCKED");
    await expect(adapter.connect(owner).finalizeAssay(seedId, 999n)).to.be.revertedWith("FINALIZE_BLOCKED");
  });
});
