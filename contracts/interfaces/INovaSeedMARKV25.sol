// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface INovaSeedMARKV25 {
    function onSeedSealed(bytes32 seedId) external;
    function onSeedGreenlit(bytes32 seedId) external;
    function onSeedQuarantined(bytes32 seedId) external;
    function onSovereignRegistered(bytes32 seedId, bytes32 sovereignPackageHash) external;
}
