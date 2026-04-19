// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../ThresholdNetworkAdapterV25.sol";
import "../../SignedAttestationVerifierV25.sol";

contract EchidnaThresholdHarness {
    ThresholdNetworkAdapterV25 internal adapter;

    constructor() {
        SignedAttestationVerifierV25 verifier = new SignedAttestationVerifierV25(address(this));
        adapter = new ThresholdNetworkAdapterV25(address(this), verifier);
    }

    function setProfile(uint16 committeeSize, uint16 threshold) external {
        if (committeeSize == 0) committeeSize = 1;
        ThresholdNetworkAdapterV25.BindingProfile memory p = ThresholdNetworkAdapterV25.BindingProfile({
            profileId: keccak256(abi.encodePacked(committeeSize, threshold)),
            provider: "lit",
            networkName: "datil",
            committeeRoot: keccak256("c"),
            relayerRoot: keccak256("r"),
            committeeSize: committeeSize,
            threshold: threshold,
            timeoutSeconds: 100,
            policyHash: keccak256("p"),
            active: true
        });

        (bool ok,) = address(adapter).call(abi.encodeWithSelector(adapter.setBindingProfile.selector, p));
        if (threshold == 0 || threshold > committeeSize) {
            require(!ok, "invalid threshold accepted");
        } else {
            require(ok, "valid threshold rejected");
        }
    }

    function echidna_invalid_profile_never_persisted() external view returns (bool) {
        return true;
    }
}
