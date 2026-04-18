// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface INovaSeedRegistryV25View {
    /// @notice Returns the numeric seed state enum value.
    function seedState(bytes32 seedId) external view returns (uint8);
    /// @notice Returns the ERC721 token id associated with a seed.
    function seedTokenId(bytes32 seedId) external view returns (uint256);
    /// @notice Returns the parent lineage seed id.
    function parentSeed(bytes32 seedId) external view returns (bytes32);
    /// @notice Returns sovereign package hash recorded during promotion.
    function sovereignPackageHash(bytes32 seedId) external view returns (bytes32);
}
