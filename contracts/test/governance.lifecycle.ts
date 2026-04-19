import { expect } from "chai";
import hre from "hardhat";

describe("CouncilGovernanceV25 lifecycle", function () {
  it("enforces election-admin controls and keeps seat count coherent", async function () {
    const [owner, outsider, seat1, seat2, challenger] = await hre.ethers.getSigners();
    const governance = await hre.ethers.deployContract("CouncilGovernanceV25", [owner.address]);

    await expect(governance.connect(outsider).openTerm()).to.be.revertedWith("NOT_ELECTION_ADMIN");

    await governance.connect(owner).setElectionAdmin(outsider.address, true);
    await governance.connect(outsider).openTerm();
    expect(await governance.currentTermId()).to.equal(1n);

    await governance.connect(outsider).assignSeat(0, seat1.address, 5, true);
    await governance.connect(outsider).assignSeat(0, seat2.address, 3, true);
    expect(await governance.seatCount()).to.equal(2n);

    const seatOne = await governance.seats(1);
    const seatTwo = await governance.seats(2);
    expect(seatOne.occupant).to.equal(seat1.address);
    expect(seatTwo.occupant).to.equal(seat2.address);

    await expect(governance.connect(challenger).openSeatChallenge(2, hre.ethers.id("bad"), { value: 0 })).to.be.revertedWith(
      "BOND_REQUIRED"
    );

    const bond = hre.ethers.parseEther("0.1");
    const tx = await governance.connect(challenger).openSeatChallenge(2, hre.ethers.id("bad-seat"), { value: bond });
    const rcpt = await tx.wait();
    const event = rcpt?.logs
      .map((l) => {
        try {
          return governance.interface.parseLog(l);
        } catch {
          return null;
        }
      })
      .find((e) => e?.name === "ChallengeOpened");

    const challengeId = event?.args.challengeId as string;
    const before = await hre.ethers.provider.getBalance(challenger.address);
    const resolveTx = await governance.connect(outsider).resolveSeatChallenge(challengeId, true);
    const resolveRcpt = await resolveTx.wait();
    const gas = (resolveRcpt?.gasUsed ?? 0n) * (resolveTx.gasPrice ?? 0n);
    const after = await hre.ethers.provider.getBalance(challenger.address);
    expect(after + gas).to.be.greaterThanOrEqual(before + bond);

    const challengedSeat = await governance.seats(2);
    expect(challengedSeat.active).to.equal(false);

    await expect(governance.connect(outsider).resolveSeatChallenge(challengeId, false)).to.be.revertedWith("ALREADY_RESOLVED");
  });
});
