import { expect } from "chai";
import hre from "hardhat";

describe("SignedAttestationVerifierV25 verification behavior", function () {
  it("accepts trusted signer signatures and rejects malformed or untrusted signatures", async function () {
    const [owner] = await hre.ethers.getSigners();
    const verifier = await hre.ethers.deployContract("SignedAttestationVerifierV25", [owner.address]);

    const signer = hre.ethers.Wallet.createRandom();
    const seedId = hre.ethers.id("seed/verify");
    const manifestHash = hre.ethers.id("manifest");
    const ciphertextHash = hre.ethers.id("cipher");
    const termId = 7;
    const deadline = 9_999_999_999;

    const digest = await verifier.hashManifestAttestation(seedId, manifestHash, ciphertextHash, termId, deadline);
    const signature = signer.signingKey.sign(digest).serialized;

    const before = await verifier.verify(digest, signature);
    expect(before.trusted).to.equal(false);
    expect(before.signer).to.equal(signer.address);

    await verifier.connect(owner).setTrustedSigner(signer.address, true);
    const after = await verifier.verify(digest, signature);
    expect(after.trusted).to.equal(true);
    expect(after.signer).to.equal(signer.address);

    await expect(verifier.verify(digest, "0x1234")).to.be.reverted;

    const otherDigest = await verifier.hashManifestAttestation(seedId, manifestHash, hre.ethers.id("other-cipher"), termId, deadline);
    const mismatch = await verifier.verify(otherDigest, signature);
    expect(mismatch.signer).to.not.equal(signer.address);
    expect(mismatch.trusted).to.equal(false);
  });

  it("enforces owner-only signer trust updates", async function () {
    const [owner, outsider] = await hre.ethers.getSigners();
    const verifier = await hre.ethers.deployContract("SignedAttestationVerifierV25", [owner.address]);

    await expect(verifier.connect(outsider).setTrustedSigner(outsider.address, true))
      .to.be.revertedWithCustomError(verifier, "OwnableUnauthorizedAccount")
      .withArgs(outsider.address);
  });
});
