// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../CouncilGovernanceV25.sol";

contract EchidnaGovernanceHarness {
    CouncilGovernanceV25 internal gov;

    constructor() {
        gov = new CouncilGovernanceV25(address(this));
        gov.setElectionAdmin(address(this), true);
        gov.openTerm();
    }

    function assign(uint32 seatId, uint96 weight) external {
        gov.assignSeat(seatId % 16, address(uint160(uint256(keccak256(abi.encodePacked(seatId, weight))))), weight, true);
    }

    function echidna_seat_count_coherent() external view returns (bool) {
        for (uint32 i = 1; i <= gov.seatCount(); i++) {
            (address occupant,,) = gov.seats(i);
            if (occupant == address(0)) return false;
        }
        return true;
    }
}
