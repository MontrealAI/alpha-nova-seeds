// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IReviewerSlashHookV25 {
    function slashReviewer(address reviewer, uint256 amount, bytes32 reasonHash) external;
}
