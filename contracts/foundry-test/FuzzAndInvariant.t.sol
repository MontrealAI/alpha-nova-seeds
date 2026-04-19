// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../ReviewerRewardTreasuryV25.sol";
import "../ThresholdNetworkAdapterV25.sol";
import "../SignedAttestationVerifierV25.sol";
import "../CouncilGovernanceV25.sol";
import "../AlphaNovaSeedV25.sol";
import "../NovaSeedRegistryV25.sol";
import "../ChallengePolicyModuleV25.sol";
import "../mocks/MockERC20.sol";

contract RegistryOutsider {
    function attemptDraft(
        NovaSeedRegistryV25 registry,
        bytes32 seedId,
        bytes32 h,
        string calldata payload,
        string calldata summary,
        string calldata fusion,
        string calldata tokenURI
    ) external {
        registry.draftSeed(seedId, h, h, h, h, h, h, h, h, h, h, payload, summary, fusion, tokenURI);
    }
}

contract FuzzAndInvariantTest {
    MockERC20 internal token;
    ReviewerRewardTreasuryV25 internal treasury;
    SignedAttestationVerifierV25 internal verifier;
    ThresholdNetworkAdapterV25 internal adapter;
    CouncilGovernanceV25 internal governance;
    AlphaNovaSeedV25 internal nft;
    NovaSeedRegistryV25 internal registry;

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

        ChallengePolicyModuleV25 challenge = new ChallengePolicyModuleV25(address(this));
        nft = new AlphaNovaSeedV25(address(this));
        registry = new NovaSeedRegistryV25(address(this), nft, adapter, treasury, governance, challenge);
        nft.setRegistry(address(registry));
        treasury.setDistributor(address(registry), true);
        registry.setCreator(address(this), true);
        ThresholdNetworkAdapterV25.BindingProfile memory seededProfile = ThresholdNetworkAdapterV25.BindingProfile({
            profileId: keccak256(abi.encodePacked(uint16(3), uint16(2), uint64(1))),
            provider: "lit",
            networkName: "seeded",
            committeeRoot: bytes32(uint256(11)),
            relayerRoot: bytes32(uint256(12)),
            committeeSize: 3,
            threshold: 2,
            timeoutSeconds: 60,
            policyHash: bytes32(uint256(13)),
            active: true
        });
        adapter.setBindingProfile(seededProfile);
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

    function testFuzz_treasury_arithmetic(uint128 accrueAmount, uint128 slashAmount, bool claimNow) external {
        treasury.accrue(address(this), accrueAmount, keccak256("accrue"));
        totalAccrued += accrueAmount;

        uint256 boundedSlash = slashAmount;
        if (boundedSlash > treasury.accrued(address(this))) boundedSlash = treasury.accrued(address(this));

        if (boundedSlash > 0) {
            treasury.clawback(address(this), boundedSlash, keccak256("slash"));
            totalClawed += boundedSlash;
        }

        uint256 claimable = treasury.accrued(address(this));
        uint256 available = token.balanceOf(address(this));
        if (claimNow && claimable > 0 && claimable <= available) {
            token.transfer(address(treasury), claimable);
            treasury.claim();
            totalClaimed += claimable;
        }

        require(totalAccrued == totalClaimed + totalClawed + treasury.accrued(address(this)), "value drift");
    }

    function testFuzz_governance_seat_count_coherence(uint32 seatId, uint96 weight) external {
        uint32 requestedSeatId = uint32((seatId % 10) + 1);
        governance.assignSeat(requestedSeatId, address(uint160(requestedSeatId + 100)), weight, true);

        uint32 expectedAssignedSeatId = requestedSeatId;
        if (requestedSeatId == 0 || requestedSeatId > governance.seatCount()) {
            expectedAssignedSeatId = uint32(governance.seatCount());
        }

        (address occupant,,) = governance.seats(expectedAssignedSeatId);
        require(occupant != address(0), "seat assignment missing");
        require(governance.seatCount() >= expectedAssignedSeatId, "seat count incoherent");
    }

    function testFuzz_registry_seed_uniqueness(bytes32 seedId) external {
        if (seedId == bytes32(0)) seedId = keccak256("non-zero");
        bytes32 h = keccak256("h");
        if (registry.seeds(seedId).seedId == bytes32(0)) {
            registry.draftSeed(seedId, h, h, h, h, h, h, h, h, h, h, "payload", "summary", "fusion", "token");
        }

        (bool ok,) = address(registry).call(
            abi.encodeWithSelector(
                registry.draftSeed.selector,
                seedId,
                h,
                h,
                h,
                h,
                h,
                h,
                h,
                h,
                h,
                h,
                "payload",
                "summary",
                "fusion",
                "token"
            )
        );
        require(!ok, "duplicate seed admitted");
    }

    function invariant_treasury_no_negative_accounting() external view {
        require(totalAccrued == totalClaimed + totalClawed + treasury.accrued(address(this)), "underflow accounting invariant");
        require(treasury.claimed(address(this)) == totalClaimed, "claim accounting mismatch");
    }

    function invariant_governance_seatcount_nonzero_for_assigned() external view {
        for (uint32 i = 1; i <= governance.seatCount(); i++) {
            (address occupant,,) = governance.seats(i);
            require(occupant != address(0), "seat gap");
        }
    }

    function invariant_threshold_profile_always_valid_when_active() external view {
        bytes32 profileId = keccak256(abi.encodePacked(uint16(3), uint16(2), uint64(1)));
        (
            bytes32 persistedId,
            string memory provider,
            string memory network,
            bytes32 committeeRoot,
            bytes32 relayerRoot,
            uint16 committeeSize,
            uint16 threshold,
            uint64 timeoutSeconds,
            bytes32 policyHash,
            bool active
        ) = adapter.profiles(profileId);

        provider;
        network;
        committeeRoot;
        relayerRoot;
        timeoutSeconds;
        policyHash;

        if (persistedId != bytes32(0) && active) {
            require(threshold > 0 && threshold <= committeeSize, "invalid persisted threshold");
        }
    }

    function invariant_registry_unauthorized_creator_cannot_draft() external {
        RegistryOutsider outsider = new RegistryOutsider();
        bytes32 seedId = keccak256("outsider-seed");
        bytes32 h = keccak256("outsider-h");
        (bool ok,) = address(outsider).call(
            abi.encodeWithSelector(
                outsider.attemptDraft.selector,
                registry,
                seedId,
                h,
                "payload",
                "summary",
                "fusion",
                "token"
            )
        );
        require(!ok, "unauthorized draft succeeded");
    }
}
