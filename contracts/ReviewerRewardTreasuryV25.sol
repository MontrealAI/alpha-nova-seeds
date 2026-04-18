// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @title ReviewerRewardTreasuryV25
/// @notice Tracks reviewer rewards, stake, slashing, and claims for deterministic governance accounting.
contract ReviewerRewardTreasuryV25 is Ownable {
    struct ReviewerStakeAccount {
        uint256 staked;
        uint256 accrued;
        uint256 claimed;
        uint256 slashed;
        uint64 updatedAt;
    }

    IERC20 public immutable rewardToken;
    mapping(address => ReviewerStakeAccount) internal _accounts;
    mapping(address => bool) public distributors;

    event DistributorSet(address indexed distributor, bool allowed);
    event ReviewerStaked(address indexed reviewer, uint256 amount);
    event ReviewerUnstaked(address indexed reviewer, uint256 amount);
    event RewardAccrued(address indexed reviewer, uint256 amount, bytes32 indexed ref);
    event RewardClaimed(address indexed reviewer, uint256 amount);
    event ReviewerSlashed(address indexed reviewer, uint256 amount, bytes32 indexed reasonHash);

    modifier onlyDistributor() {
        require(distributors[msg.sender], "NOT_DISTRIBUTOR");
        _;
    }

    /// @param initialOwner Owner address.
    /// @param _rewardToken ERC20 used for reviewer settlement.
    constructor(address initialOwner, IERC20 _rewardToken) Ownable(initialOwner) {
        rewardToken = _rewardToken;
    }

    /// @notice Sets or unsets an authorized distributor.
    function setDistributor(address distributor, bool allowed) external onlyOwner {
        distributors[distributor] = allowed;
        emit DistributorSet(distributor, allowed);
    }

    /// @notice Records reviewer stake locked for governance participation.
    function recordStake(address reviewer, uint256 amount) external onlyDistributor {
        ReviewerStakeAccount storage a = _accounts[reviewer];
        a.staked += amount;
        a.updatedAt = uint64(block.timestamp);
        emit ReviewerStaked(reviewer, amount);
    }

    /// @notice Records stake release after lifecycle completion.
    function recordUnstake(address reviewer, uint256 amount) external onlyDistributor {
        ReviewerStakeAccount storage a = _accounts[reviewer];
        require(a.staked >= amount, "INSUFFICIENT_STAKE");
        a.staked -= amount;
        a.updatedAt = uint64(block.timestamp);
        emit ReviewerUnstaked(reviewer, amount);
    }

    /// @notice Accrues a deterministic reward event for a reviewer.
    function accrue(address reviewer, uint256 amount, bytes32 ref) external onlyDistributor {
        ReviewerStakeAccount storage a = _accounts[reviewer];
        a.accrued += amount;
        a.updatedAt = uint64(block.timestamp);
        emit RewardAccrued(reviewer, amount, ref);
    }

    /// @notice Claims all currently accrued rewards for caller.
    function claim() external {
        ReviewerStakeAccount storage a = _accounts[msg.sender];
        uint256 amount = a.accrued;
        require(amount > 0, "NO_REWARD");
        a.accrued = 0;
        a.claimed += amount;
        a.updatedAt = uint64(block.timestamp);
        require(rewardToken.transfer(msg.sender, amount), "TRANSFER_FAIL");
        emit RewardClaimed(msg.sender, amount);
    }

    /// @notice Applies deterministic slashing to reviewer stake first, then accrued rewards.
    function slash(address reviewer, uint256 amount, bytes32 reasonHash) external onlyDistributor {
        ReviewerStakeAccount storage a = _accounts[reviewer];
        uint256 remaining = amount;
        if (a.staked >= remaining) {
            a.staked -= remaining;
            remaining = 0;
        } else {
            remaining -= a.staked;
            a.staked = 0;
        }
        if (remaining > 0) {
            require(a.accrued >= remaining, "INSUFFICIENT_ACCRUED");
            a.accrued -= remaining;
        }
        a.slashed += amount;
        a.updatedAt = uint64(block.timestamp);
        emit ReviewerSlashed(reviewer, amount, reasonHash);
    }

    /// @notice Returns reviewer accounting values plus net available claim.
    function reviewerAccount(address reviewer) external view returns (
        uint256 staked,
        uint256 accrued,
        uint256 claimed,
        uint256 slashed,
        uint256 claimable
    ) {
        ReviewerStakeAccount memory a = _accounts[reviewer];
        return (a.staked, a.accrued, a.claimed, a.slashed, a.accrued);
    }
}
