from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text()


def test_registry_release_metadata_surface_exists():
    text = _read("contracts/NovaSeedRegistryV25.sol")
    assert 'string public constant VERSION = "2.6.0-rc1";' in text
    assert 'function releaseMetadata() external pure returns' in text


def test_reviewer_stake_accounting_surface_exists():
    text = _read("contracts/ReviewerRewardTreasuryV25.sol")
    assert 'struct ReviewerStakeAccount' in text
    assert 'function recordStake' in text
    assert 'function slash' in text
    assert 'function reviewerAccount' in text


def test_council_lifecycle_surface_exists():
    text = _read("contracts/CouncilGovernanceV25.sol")
    assert 'enum SeatStatus' in text
    assert 'function setSeatStatus' in text


def test_seed_identity_and_governance_functions_present():
    text = _read("contracts/NovaSeedRegistryV25.sol")
    assert 'function draftSeed' in text
    assert 'function openReview' in text
    assert 'function finalizeReview' in text


def test_threshold_attestation_surface_present():
    text = _read("contracts/ThresholdNetworkAdapterV25.sol")
    assert 'function openRequest' in text
    assert 'function completeRequest' in text
    assert 'event DecryptionCompleted' in text
