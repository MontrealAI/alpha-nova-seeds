// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IAGIJobManagerWorkflowV25 {
    /// @notice Creates an assay execution job.
    function createAssayJob(bytes32 seedId, bytes32 assaySpecHash, uint256 reward) external returns (uint256 jobId);
    /// @notice Requests completion proof for a job.
    function requestCompletion(uint256 jobId, string calldata uri) external;
    /// @notice Marks a job as validated.
    function validateJob(uint256 jobId) external;
    /// @notice Marks a job as disapproved.
    function disapproveJob(uint256 jobId) external;
    /// @notice Final settlement for a completed job.
    function finalizeJob(uint256 jobId) external;
}
