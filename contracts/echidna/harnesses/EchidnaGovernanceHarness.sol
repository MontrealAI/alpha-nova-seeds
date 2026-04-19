// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../CouncilGovernanceV25.sol";

contract GovernanceExternalCaller {
    function tryResolve(CouncilGovernanceV25 gov, bytes32 challengeId, bool upheld) external returns (bool ok) {
        (ok,) = address(gov).call(abi.encodeWithSelector(gov.resolveSeatChallenge.selector, challengeId, upheld));
    }
}

contract EchidnaGovernanceHarness {
    CouncilGovernanceV25 internal gov;
    GovernanceExternalCaller internal outsider;
    bytes32 internal lastChallengeId;

    constructor() {
        gov = new CouncilGovernanceV25(address(this));
        gov.setElectionAdmin(address(this), true);
        gov.openTerm();
        outsider = new GovernanceExternalCaller();
    }

    function assign(uint32 seatId, uint96 weight) external {
        gov.assignSeat(seatId % 16, address(uint160(uint256(keccak256(abi.encodePacked(seatId, weight))))), weight, true);
    }

    function openChallenge(uint32 seatId, bytes32 reasonHash, uint96 bondSeed) external {
        if (gov.seatCount() == 0) {
            gov.assignSeat(1, address(0x1234), 1, true);
        }
        uint32 bounded = uint32((seatId % gov.seatCount()) + 1);
        uint256 bond = uint256(bondSeed) + 1;
        lastChallengeId = gov.openSeatChallenge{value: bond}(bounded, reasonHash);
    }

    function echidna_seat_count_coherent() external view returns (bool) {
        for (uint32 i = 1; i <= gov.seatCount(); i++) {
            (address occupant,,) = gov.seats(i);
            if (occupant == address(0)) return false;
        }
        return true;
    }

    function echidna_only_admin_can_resolve() external returns (bool) {
        if (lastChallengeId == bytes32(0)) return true;
        bool ok = outsider.tryResolve(gov, lastChallengeId, false);
        return !ok;
    }

    receive() external payable {}
}
