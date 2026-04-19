import { expect } from "chai";
import hre from "hardhat";

describe("ThresholdNetworkAdapterV25 fail-closed transitions", function () {
  it("rejects invalid profiles and blocks completion with untrusted signatures", async function () {
    const [owner, requester] = await hre.ethers.getSigners();
    const verifier = await hre.ethers.deployContract("SignedAttestationVerifierV25", [owner.address]);
    const adapter = await hre.ethers.deployContract("ThresholdNetworkAdapterV25", [owner.address, await verifier.getAddress()]);

    const badProfile = {
      profileId: hre.ethers.id("bad"),
      provider: "lit",
      networkName: "datil",
      committeeRoot: hre.ethers.ZeroHash,
      relayerRoot: hre.ethers.ZeroHash,
      committeeSize: 2,
      threshold: 3,
      timeoutSeconds: 60,
      policyHash: hre.ethers.ZeroHash,
      active: true
    };

    await expect(adapter.connect(owner).setBindingProfile(badProfile)).to.be.revertedWith("BAD_THRESHOLD");

    const profile = { ...badProfile, profileId: hre.ethers.id("good"), threshold: 2 };
    await adapter.connect(owner).setBindingProfile(profile);

    const requestTx = await adapter
      .connect(requester)
      .openRequest(hre.ethers.id("seed"), profile.profileId, hre.ethers.id("cipher"), hre.ethers.id("manifest"));
    const requestRcpt = await requestTx.wait();
    const event = requestRcpt?.logs
      .map((l) => {
        try {
          return adapter.interface.parseLog(l);
        } catch {
          return null;
        }
      })
      .find((e) => e?.name === "DecryptionRequested");

    const requestId = event?.args.requestId as string;
    const deadline = (await hre.ethers.provider.getBlock("latest"))!.timestamp + 60;
    const digest = await verifier.hashDecryptAttestation(
      requestId,
      hre.ethers.id("seed"),
      hre.ethers.id("plain"),
      hre.ethers.id("completion"),
      1,
      deadline
    );
    const untrustedSigner = hre.ethers.Wallet.createRandom();
    const sig = untrustedSigner.signingKey.sign(digest).serialized;

    await expect(
      adapter.connect(requester).completeRequest(requestId, hre.ethers.id("plain"), hre.ethers.id("completion"), 1, deadline, sig)
    ).to.be.revertedWith("BAD_SIGNATURE");

    await verifier.connect(owner).setTrustedSigner(untrustedSigner.address, true);
    await adapter.connect(requester).completeRequest(requestId, hre.ethers.id("plain"), hre.ethers.id("completion"), 1, deadline, sig);
    const request = await adapter.requests(requestId);
    expect(request.status).to.equal(2n);

    await expect(adapter.connect(owner).cancelRequest(requestId)).to.be.revertedWith("BAD_STATE");
  });
});
