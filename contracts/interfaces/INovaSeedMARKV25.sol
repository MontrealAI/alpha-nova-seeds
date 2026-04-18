// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface INovaSeedMARKV25 {
    /// @notice Hook fired when a seed is sealed.
    function onSeedSealed(bytes32 seedId) external;
    /// @notice Hook fired when a seed passes review.
    function onSeedGreenlit(bytes32 seedId) external;
    /// @notice Hook fired when a seed is quarantined.
    function onSeedQuarantined(bytes32 seedId) external;
    /// @notice Hook fired when a sovereign package is registered.
    function onSovereignRegistered(bytes32 seedId, bytes32 sovereignPackageHash) external;
}
