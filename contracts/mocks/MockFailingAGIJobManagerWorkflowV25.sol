// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../interfaces/IAGIJobManagerWorkflowV25.sol";

contract MockFailingAGIJobManagerWorkflowV25 is IAGIJobManagerWorkflowV25 {
    function createAssayJob(bytes32, bytes32, uint256) external pure returns (uint256) {
        revert("CREATE_BLOCKED");
    }

    function requestCompletion(uint256, string calldata) external pure {
        revert("REQUEST_BLOCKED");
    }

    function validateJob(uint256) external pure {
        revert("VALIDATE_BLOCKED");
    }

    function disapproveJob(uint256) external pure {
        revert("DISAPPROVE_BLOCKED");
    }

    function finalizeJob(uint256) external pure {
        revert("FINALIZE_BLOCKED");
    }
}
