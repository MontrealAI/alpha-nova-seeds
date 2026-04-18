// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface INovaSeedRegistryV25View {
    function seedState(bytes32 seedId) external view returns (uint8);
    function seedTokenId(bytes32 seedId) external view returns (uint256);
    function parentSeed(bytes32 seedId) external view returns (bytes32);
    function sovereignPackageHash(bytes32 seedId) external view returns (bytes32);
}
