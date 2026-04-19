import { expect } from "chai";
import hre from "hardhat";

describe("SignedAttestationVerifierV25 signature verification", function () {
  it("accepts trusted signer signatures and rejects malformed/untrusted payloads", async function () {
    const [owner, outsider] = await hre.ethers.getSigners();
    const verifier = await hre.ethers.deployContract("SignedAttestationVerifierV25", [owner.address]);

    const trustedWallet = hre.ethers.Wallet.createRandom();
    const digest = await verifier.hashManifestAttestation(
      hre.ethers.id("seed"),
      hre.ethers.id("manifest"),
      hre.ethers.id("ciphertext"),
      1,
      999_999_999
    );

    const trustedSignature = trustedWallet.signingKey.sign(digest).serialized;
    const [recoveredUntrusted, isTrustedBefore] = await verifier.verify(digest, trustedSignature);
    expect(recoveredUntrusted).to.equal(trustedWallet.address);
    expect(isTrustedBefore).to.equal(false);

    await expect(verifier.connect(outsider).setTrustedSigner(trustedWallet.address, true)).to.be.revertedWithCustomError(
      verifier,
      "OwnableUnauthorizedAccount"
    );

    await verifier.connect(owner).setTrustedSigner(trustedWallet.address, true);
    const [recoveredTrusted, isTrustedAfter] = await verifier.verify(digest, trustedSignature);
    expect(recoveredTrusted).to.equal(trustedWallet.address);
    expect(isTrustedAfter).to.equal(true);

    const domainSeparatedDigest = await verifier.hashChallengeEvidence(
      hre.ethers.id("challenge"),
      hre.ethers.id("seed"),
      hre.ethers.id("evidence"),
      1,
      999_999_999
    );
    expect(domainSeparatedDigest).to.not.equal(digest);

    const [wrongDomainSigner, wrongDomainTrusted] = await verifier.verify(domainSeparatedDigest, trustedSignature);
    expect(wrongDomainSigner).to.not.equal(trustedWallet.address);
    expect(wrongDomainTrusted).to.equal(false);

    await expect(verifier.verify(digest, "0x0102")).to.be.reverted;
  });
});
