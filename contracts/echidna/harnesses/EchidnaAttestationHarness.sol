// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../SignedAttestationVerifierV25.sol";

contract AttestationAttacker {
    function setTrustedSigner(SignedAttestationVerifierV25 verifier, address signer, bool trusted) external {
        verifier.setTrustedSigner(signer, trusted);
    }
}

contract EchidnaAttestationHarness {
    SignedAttestationVerifierV25 internal verifier;
    AttestationAttacker internal attacker;

    address internal constant SIGNER = address(0xBEEF);

    bytes32 internal lastManifestDigest;
    bytes32 internal lastDecryptDigest;
    bytes32 internal lastChallengeDigest;

    constructor() {
        verifier = new SignedAttestationVerifierV25(address(this));
        attacker = new AttestationAttacker();
    }

    function trustSigner(bool trusted) external {
        verifier.setTrustedSigner(SIGNER, trusted);
    }

    function hashAll(bytes32 seedId, bytes32 requestId, bytes32 manifestHash, bytes32 ciphertextHash, bytes32 completionHash) external {
        if (seedId == bytes32(0)) {
            seedId = bytes32(uint256(1));
        }
        if (requestId == bytes32(0)) {
            requestId = bytes32(uint256(2));
        }

        lastManifestDigest = verifier.hashManifestAttestation(seedId, manifestHash, ciphertextHash, 1, block.timestamp + 1 days);
        lastDecryptDigest = verifier.hashDecryptAttestation(requestId, seedId, manifestHash, completionHash, 1, block.timestamp + 1 days);
        lastChallengeDigest = verifier.hashChallengeEvidence(requestId, seedId, manifestHash, 1, block.timestamp + 1 days);
    }

    function echidna_signer_trust_is_owner_only() external returns (bool) {
        (bool ok,) = address(attacker).call(
            abi.encodeWithSelector(attacker.setTrustedSigner.selector, verifier, address(attacker), true)
        );
        return !ok && !verifier.trustedSigners(address(attacker));
    }

    function echidna_domain_separation_between_attestation_types() external view returns (bool) {
        if (lastManifestDigest == bytes32(0) || lastDecryptDigest == bytes32(0) || lastChallengeDigest == bytes32(0)) {
            return true;
        }
        return lastManifestDigest != lastDecryptDigest
            && lastManifestDigest != lastChallengeDigest
            && lastDecryptDigest != lastChallengeDigest;
    }

    function echidna_malformed_signature_never_verifies() external view returns (bool) {
        bytes memory malformed = hex"0102";
        (bool ok,) = address(verifier).staticcall(abi.encodeWithSelector(verifier.verify.selector, keccak256("digest"), malformed));
        return !ok;
    }

    function echidna_no_replay_unsafe_auto_trust() external view returns (bool) {
        if (lastManifestDigest == bytes32(0)) return true;

        bytes memory emptySignature;
        (bool ok, bytes memory data) = address(verifier).staticcall(
            abi.encodeWithSelector(verifier.verify.selector, lastManifestDigest, emptySignature)
        );

        if (!ok || data.length == 0) return true;

        (, bool trusted) = abi.decode(data, (address, bool));
        return !trusted;
    }
}
