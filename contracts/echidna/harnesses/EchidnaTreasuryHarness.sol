// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../ReviewerRewardTreasuryV25.sol";
import "../../mocks/MockERC20.sol";

contract EchidnaTreasuryHarness {
    MockERC20 internal token;
    ReviewerRewardTreasuryV25 internal treasury;

    address internal immutable REVIEWER = address(this);
    uint256 internal totalAccrued;
    uint256 internal totalSlashed;
    uint256 internal totalClaimed;

    constructor() {
        token = new MockERC20("R", "R", 1e24);
        treasury = new ReviewerRewardTreasuryV25(address(this), token);
        treasury.setDistributor(address(this), true);
    }

    function accrue(uint128 amount) external {
        treasury.accrue(REVIEWER, amount, keccak256("accrue"));
        totalAccrued += amount;
    }

    function slash(uint128 amount) external {
        uint256 bal = treasury.accrued(REVIEWER);
        if (bal == 0) return;
        uint256 bounded = amount % (bal + 1);
        if (bounded == 0) return;
        treasury.clawback(REVIEWER, bounded, keccak256("slash"));
        totalSlashed += bounded;
    }

    function fundAndClaim() external {
        uint256 amount = treasury.accrued(REVIEWER);
        if (amount == 0) return;
        token.transfer(address(treasury), amount);
        (bool ok,) = address(treasury).call(abi.encodeWithSelector(treasury.claim.selector));
        if (ok) {
            totalClaimed += amount;
        }
    }

    function echidna_clawback_not_exceeding_accrued() external view returns (bool) {
        uint256 accruedNow = treasury.accrued(REVIEWER);
        uint256 clawedNow = treasury.clawedBack(REVIEWER);
        return clawedNow == totalSlashed && accruedNow + clawedNow + totalClaimed == totalAccrued;
    }

    function echidna_no_double_claimable_balance() external view returns (bool) {
        return treasury.accrued(REVIEWER) == 0 || token.balanceOf(address(treasury)) == 0;
    }
}
