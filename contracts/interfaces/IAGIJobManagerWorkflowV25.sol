// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IAGIJobManagerWorkflowV25 {
    function createAssayJob(bytes32 seedId, bytes32 assaySpecHash, uint256 reward) external returns (uint256 jobId);
    function requestCompletion(uint256 jobId, string calldata uri) external;
    function validateJob(uint256 jobId) external;
    function disapproveJob(uint256 jobId) external;
    function finalizeJob(uint256 jobId) external;
}
