from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text()


def test_seed_identity_and_release_metadata_surface_present():
    content = _read('contracts/NovaSeedRegistryV25.sol')
    assert 'function draftSeed(' in content
    assert 'function releaseMetadata()' in content
    assert 'RELEASE_VERSION' in content


def test_governance_and_challenge_lifecycle_surface_present():
    content = _read('contracts/CouncilGovernanceV25.sol')
    assert 'function openTerm()' in content
    assert 'function openSeatChallenge(' in content
    assert 'function resolveSeatChallenge(' in content


def test_reviewer_stake_and_threshold_attestation_surface_present():
    treasury = _read('contracts/ReviewerRewardTreasuryV25.sol')
    verifier = _read('contracts/SignedAttestationVerifierV25.sol')
    assert 'function accrue(' in treasury
    assert 'function clawback(' in treasury
    assert 'function verify(' in verifier
