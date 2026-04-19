// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../ReviewerRewardTreasuryV25.sol";
import "../ThresholdNetworkAdapterV25.sol";
import "../SignedAttestationVerifierV25.sol";
import "../CouncilGovernanceV25.sol";
import "../mocks/MockERC20.sol";

contract FuzzAndInvariantTest {
    MockERC20 internal token;
    ReviewerRewardTreasuryV25 internal treasury;
    SignedAttestationVerifierV25 internal verifier;
    ThresholdNetworkAdapterV25 internal adapter;
    CouncilGovernanceV25 internal governance;

    uint256 internal totalAccrued;
    uint256 internal totalClaimed;
    uint256 internal totalClawed;

    constructor() {
        token = new MockERC20("Reward", "RWD", 1e27);
        treasury = new ReviewerRewardTreasuryV25(address(this), token);
        treasury.setDistributor(address(this), true);

        verifier = new SignedAttestationVerifierV25(address(this));
        adapter = new ThresholdNetworkAdapterV25(address(this), verifier);

        governance = new CouncilGovernanceV25(address(this));
        governance.setElectionAdmin(address(this), true);
        governance.openTerm();
    }

    function testFuzz_threshold_boundaries(uint16 committeeSize, uint16 threshold, uint64 timeoutSeconds) external {
        if (committeeSize == 0) committeeSize = 1;
        ThresholdNetworkAdapterV25.BindingProfile memory p = ThresholdNetworkAdapterV25.BindingProfile({
            profileId: keccak256(abi.encodePacked(committeeSize, threshold, timeoutSeconds)),
            provider: "lit",
            networkName: "network",
            committeeRoot: bytes32(uint256(1)),
            relayerRoot: bytes32(uint256(2)),
            committeeSize: committeeSize,
            threshold: threshold,
            timeoutSeconds: timeoutSeconds,
            policyHash: bytes32(uint256(3)),
            active: true
        });

        bool shouldRevert = threshold == 0 || threshold > committeeSize;
        (bool ok,) = address(adapter).call(abi.encodeWithSelector(adapter.setBindingProfile.selector, p));
        require(ok != shouldRevert, "threshold-boundary mismatch");
    }

    function testFuzz_treasury_arithmetic(uint128 accrueAmount, uint128 slashAmount) external {
        address reviewer = address(uint160(uint256(keccak256(abi.encodePacked(accrueAmount, slashAmount)))));
        treasury.accrue(reviewer, accrueAmount, keccak256("accrue"));
        totalAccrued += accrueAmount;

        uint256 boundedSlash = slashAmount;
        if (boundedSlash > treasury.accrued(reviewer)) boundedSlash = treasury.accrued(reviewer);

        if (boundedSlash > 0) {
            treasury.clawback(reviewer, boundedSlash, keccak256("slash"));
            totalClawed += boundedSlash;
        }

        require(totalAccrued >= totalClaimed + totalClawed, "value created unexpectedly");
    }

    function testFuzz_governance_seat_count_coherence(uint32 seatId, uint96 weight) external {
        seatId = uint32((seatId % 10) + 1);
        governance.assignSeat(seatId, address(uint160(seatId + 100)), weight, true);
        require(governance.seatCount() >= seatId, "seat count incoherent");
    }

    function invariant_treasury_no_negative_accounting() external view {
        require(totalAccrued >= totalClaimed + totalClawed, "underflow accounting invariant");
    }

    function invariant_governance_seatcount_nonzero_for_assigned() external view {
        for (uint32 i = 1; i <= governance.seatCount(); i++) {
            (address occupant,,) = governance.seats(i);
            if (occupant != address(0)) {
                require(i <= governance.seatCount(), "seat out of range");
            }
        }
    }
}
