import { expect } from "chai";
import hre from "hardhat";

describe("AlphaNovaSeedV25 identity controls", function () {
  it("enforces owner/registry authority and URI mutation guards", async function () {
    const [owner, registry, outsider, recipient] = await hre.ethers.getSigners();
    const nft = await hre.ethers.deployContract("AlphaNovaSeedV25", [owner.address]);

    await expect(nft.connect(outsider).setRegistry(registry.address)).to.be.revertedWithCustomError(nft, "OwnableUnauthorizedAccount");

    await nft.connect(owner).setRegistry(registry.address);
    await expect(nft.connect(outsider).mint(recipient.address, "ipfs://seed-1")).to.be.revertedWith("NOT_REGISTRY");

    await expect(nft.connect(registry).mint(recipient.address, "ipfs://seed-1"))
      .to.emit(nft, "Transfer")
      .withArgs(hre.ethers.ZeroAddress, recipient.address, 1n);

    expect(await nft.ownerOf(1n)).to.equal(recipient.address);
    expect(await nft.tokenURI(1n)).to.equal("ipfs://seed-1");

    await expect(nft.connect(outsider).setTokenURI(1n, "ipfs://mutated")).to.be.revertedWith("NOT_REGISTRY");
    await nft.connect(registry).setTokenURI(1n, "ipfs://mutated");
    expect(await nft.tokenURI(1n)).to.equal("ipfs://mutated");

    await expect(nft.tokenURI(999n)).to.be.revertedWith("NO_TOKEN");
    await expect(nft.connect(registry).setTokenURI(999n, "ipfs://nope")).to.be.revertedWith("NO_TOKEN");
  });
});
