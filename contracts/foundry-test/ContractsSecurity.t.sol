// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../AlphaNovaSeedV25.sol";
import "../NovaSeedRegistryV25.sol";
import "../ChallengePolicyModuleV25.sol";
import "../CouncilGovernanceV25.sol";
import "../ReviewerRewardTreasuryV25.sol";
import "../SignedAttestationVerifierV25.sol";
import "../ThresholdNetworkAdapterV25.sol";
import "../NovaSeedWorkflowAdapterV25.sol";
import "../mocks/MockERC20.sol";
import "../mocks/MockAGIJobManagerWorkflowV25.sol";
import "../mocks/MockRegistryViewV25.sol";

contract ExternalCaller {
    function callSetRegistry(AlphaNovaSeedV25 seed, address registry) external {
        seed.setRegistry(registry);
    }

    function callMint(AlphaNovaSeedV25 seed, address to, string calldata uri) external {
        seed.mint(to, uri);
    }

    function callSetCreator(NovaSeedRegistryV25 registry, address creator, bool allowed) external {
        registry.setCreator(creator, allowed);
    }

    function callFinalize(NovaSeedRegistryV25 registry, bytes32 seedId) external {
        registry.finalizeReview(seedId);
    }

    function callSetPolicy(ChallengePolicyModuleV25 module, bytes32 id) external {
        module.setPolicy(id, 1, 1, 1, true);
    }

    function callResolve(CouncilGovernanceV25 gov, bytes32 challengeId) external {
        gov.resolveSeatChallenge(challengeId, false);
    }

    function callSetDistributor(ReviewerRewardTreasuryV25 t, address d, bool allowed) external {
        t.setDistributor(d, allowed);
    }

    function callAccrue(ReviewerRewardTreasuryV25 t, address reviewer, uint256 amount, bytes32 ref) external {
        t.accrue(reviewer, amount, ref);
    }

    function callSetTrustedSigner(SignedAttestationVerifierV25 v, address signer, bool trusted) external {
        v.setTrustedSigner(signer, trusted);
    }

    function callSetBinding(ThresholdNetworkAdapterV25 a, ThresholdNetworkAdapterV25.BindingProfile calldata p) external {
        a.setBindingProfile(p);
    }

    function callSetMark(NovaSeedWorkflowAdapterV25 workflow, INovaSeedMARKV25 mark) external {
        workflow.setMARK(mark);
    }
}

contract ContractsSecurityTest {
    function _expectRevert(address target, bytes memory data) internal returns (bool) {
        (bool ok,) = target.call(data);
        return !ok;
    }

    function test_alpha_seed_registry_and_uri_guards() external {
        AlphaNovaSeedV25 seed = new AlphaNovaSeedV25(address(this));
        ExternalCaller outsider = new ExternalCaller();

        require(_expectRevert(address(seed), abi.encodeWithSelector(outsider.callSetRegistry.selector, seed, address(outsider))), "owner gate");
        seed.setRegistry(address(this));

        uint256 tokenId = seed.mint(address(0xBEEF), "ipfs://seed");
        require(tokenId == 1, "mint id");
        require(keccak256(bytes(seed.tokenURI(tokenId))) == keccak256(bytes("ipfs://seed")), "uri");

        require(_expectRevert(address(seed), abi.encodeWithSelector(outsider.callSetRegistry.selector, seed, address(0))), "set registry outsider");
        require(_expectRevert(address(seed), abi.encodeWithSelector(outsider.callMint.selector, seed, address(this), "x")), "mint outsider");
        require(_expectRevert(address(seed), abi.encodeWithSelector(seed.tokenURI.selector, 999)), "missing token");
    }

    function test_registry_lifecycle_happy_and_revert_paths() external {
        MockERC20 token = new MockERC20("R", "R", 1e24);
        AlphaNovaSeedV25 nft = new AlphaNovaSeedV25(address(this));
        SignedAttestationVerifierV25 verifier = new SignedAttestationVerifierV25(address(this));
        ThresholdNetworkAdapterV25 adapter = new ThresholdNetworkAdapterV25(address(this), verifier);
        ReviewerRewardTreasuryV25 treasury = new ReviewerRewardTreasuryV25(address(this), token);
        CouncilGovernanceV25 gov = new CouncilGovernanceV25(address(this));
        ChallengePolicyModuleV25 challenge = new ChallengePolicyModuleV25(address(this));
        NovaSeedRegistryV25 registry = new NovaSeedRegistryV25(address(this), nft, adapter, treasury, gov, challenge);

        nft.setRegistry(address(registry));
        treasury.setDistributor(address(registry), true);
        registry.setCreator(address(this), true);
        gov.openTerm();

        bytes32 seedId = keccak256("seed");
        bytes32 h = keccak256("h");
        registry.draftSeed(seedId, h, h, h, h, h, h, h, h, h, h, h, "payload", "summary", "fusion", "token");
        require(_expectRevert(address(registry), abi.encodeWithSelector(registry.openReview.selector, seedId)), "bad state");
        registry.sealSeed(seedId);
        registry.openReview(seedId);
        registry.submitReview(seedId, 3, NovaSeedRegistryV25.ReviewDecision.GREENLIGHT, h);
        registry.submitReview(seedId, 2, NovaSeedRegistryV25.ReviewDecision.APPROVE, h);
        registry.finalizeReview(seedId);

        registry.registerSovereign(seedId, h, "ipfs://sovereign", address(this));

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(registry), abi.encodeWithSelector(outsider.callSetCreator.selector, registry, address(outsider), true)), "set creator auth");
        require(_expectRevert(address(registry), abi.encodeWithSelector(registry.draftSeed.selector, seedId, h, h, h, h, h, h, h, h, h, h, h, "payload", "summary", "fusion", "token")), "duplicate id");
    }

    function test_challenge_policy_math_and_finalization() external {
        ChallengePolicyModuleV25 module = new ChallengePolicyModuleV25(address(this));
        bytes32 policyId = keccak256("policy");
        bytes32 challengeId = keccak256("challenge");
        module.setPolicy(policyId, 2, 4, 2, true);
        module.setAdjudicator(address(this), true);

        module.recordVote(challengeId, policyId, true, 2, false);
        module.recordVote(challengeId, policyId, true, 2, false);
        ChallengePolicyModuleV25.Outcome outcome = module.finalize(challengeId);
        require(uint256(outcome) == uint256(ChallengePolicyModuleV25.Outcome.UPHELD), "upheld");

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(module), abi.encodeWithSelector(outsider.callSetPolicy.selector, module, policyId)), "owner only");
        require(_expectRevert(address(module), abi.encodeWithSelector(module.finalize.selector, challengeId)), "double finalize");
    }

    function test_governance_seat_lifecycle_and_challenges() external {
        CouncilGovernanceV25 gov = new CouncilGovernanceV25(address(this));
        gov.setElectionAdmin(address(this), true);
        uint64 termId = gov.openTerm();
        require(termId == 1, "term");

        gov.assignSeat(0, address(0xAA), 4, true);
        gov.assignSeat(0, address(0xBB), 3, true);
        require(gov.seatCount() == 2, "seat count");

        gov.delegate(address(0xCC), 9);
        CouncilGovernanceV25.DelegationSnapshot[] memory snapshots = gov.delegationSnapshots(termId);
        require(snapshots.length == 1, "delegation snapshot");

        (bool opened, bytes memory data) = address(gov).call{value: 1 ether}(abi.encodeWithSelector(gov.openSeatChallenge.selector, 2, keccak256("r")));
        require(opened, "open challenge");
        bytes32 challengeId = abi.decode(data, (bytes32));
        gov.resolveSeatChallenge(challengeId, true);
        (,,bool active) = gov.seats(2);
        require(!active, "deactivate seat");

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(gov), abi.encodeWithSelector(outsider.callResolve.selector, gov, challengeId)), "resolve auth");
    }

    function test_treasury_access_and_accounting_paths() external {
        MockERC20 reward = new MockERC20("R", "R", 1e24);
        ReviewerRewardTreasuryV25 treasury = new ReviewerRewardTreasuryV25(address(this), reward);

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(treasury), abi.encodeWithSelector(outsider.callSetDistributor.selector, treasury, address(outsider), true)), "only owner");

        treasury.setDistributor(address(this), true);
        treasury.accrue(address(this), 100, keccak256("x"));
        treasury.clawback(address(this), 40, keccak256("slash"));
        require(treasury.accrued(address(this)) == 60, "accrued");

        reward.transfer(address(treasury), 60);
        treasury.claim();
        require(treasury.accrued(address(this)) == 0, "post claim");
        require(treasury.claimed(address(this)) == 60, "claimed");
        require(_expectRevert(address(treasury), abi.encodeWithSelector(treasury.claim.selector)), "no double claim");
    }

    function test_attestation_verifier_signer_controls() external {
        SignedAttestationVerifierV25 verifier = new SignedAttestationVerifierV25(address(this));
        bytes32 digest = verifier.hashManifestAttestation(keccak256("seed"), keccak256("m"), keccak256("c"), 1, block.timestamp + 1 days);
        (address signer, bool trusted) = verifier.verify(digest, hex"4c2b17cb97c8a6ea04c5dc68942666326038a83831a52ce419198f84c0e8d8090932e89f7b29d0ebf8f7de2ffd6bd9b6f43b3a8efa1884a5f7cb402ad4f6fe6d1b");
        require(!trusted, "initially untrusted");
        verifier.setTrustedSigner(signer, true);
        (, trusted) = verifier.verify(digest, hex"4c2b17cb97c8a6ea04c5dc68942666326038a83831a52ce419198f84c0e8d8090932e89f7b29d0ebf8f7de2ffd6bd9b6f43b3a8efa1884a5f7cb402ad4f6fe6d1b");
        require(trusted, "trusted signer");

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(verifier), abi.encodeWithSelector(outsider.callSetTrustedSigner.selector, verifier, address(outsider), true)), "owner only");
    }

    function test_threshold_adapter_lifecycle_and_rejections() external {
        SignedAttestationVerifierV25 verifier = new SignedAttestationVerifierV25(address(this));
        ThresholdNetworkAdapterV25 adapter = new ThresholdNetworkAdapterV25(address(this), verifier);

        ThresholdNetworkAdapterV25.BindingProfile memory p = ThresholdNetworkAdapterV25.BindingProfile({
            profileId: keccak256("p"),
            provider: "lit",
            networkName: "datil",
            committeeRoot: keccak256("c"),
            relayerRoot: keccak256("r"),
            committeeSize: 3,
            threshold: 2,
            timeoutSeconds: 100,
            policyHash: keccak256("pol"),
            active: true
        });

        adapter.setBindingProfile(p);
        bytes32 requestId = adapter.openRequest(keccak256("seed"), p.profileId, keccak256("cipher"), keccak256("manifest"));
        adapter.challengeRequest(requestId, keccak256("challenge"));
        adapter.cancelRequest(requestId);

        ExternalCaller outsider = new ExternalCaller();
        require(_expectRevert(address(adapter), abi.encodeWithSelector(outsider.callSetBinding.selector, adapter, p)), "set profile auth");
        require(_expectRevert(address(adapter), abi.encodeWithSelector(adapter.cancelRequest.selector, requestId)), "cancel twice");
    }

    function test_workflow_adapter_integration_paths() external {
        MockRegistryViewV25 registryView = new MockRegistryViewV25();
        MockAGIJobManagerWorkflowV25 workflowEngine = new MockAGIJobManagerWorkflowV25();
        NovaSeedWorkflowAdapterV25 adapter = new NovaSeedWorkflowAdapterV25(address(this), registryView, workflowEngine);

        bytes32 seedId = keccak256("seed");
        registryView.setState(seedId, 4);
        uint256 jobId = adapter.createAssay(seedId, keccak256("assay"), 10);
        adapter.finalizeAssay(seedId, jobId);
        (, , , bool finalized) = workflowEngine.jobs(jobId);
        require(finalized, "job finalized");

        registryView.setState(seedId, 2);
        require(_expectRevert(address(adapter), abi.encodeWithSelector(adapter.createAssay.selector, seedId, keccak256("assay2"), 1)), "state restricted");
    }

    receive() external payable {}
}
