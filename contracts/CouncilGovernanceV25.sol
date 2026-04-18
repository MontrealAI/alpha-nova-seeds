// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

/// @title CouncilGovernanceV25
/// @notice Handles council terms, delegations, seat lifecycle, and challenge resolution.
contract CouncilGovernanceV25 is Ownable {
    enum SeatStatus {
        NONE,
        ACTIVE,
        INACTIVE,
        RETIRED
    }

    struct Seat {
        address occupant;
        uint96 weight;
        SeatStatus status;
        uint64 activatedAt;
        uint64 deactivatedAt;
        uint64 retiredAt;
        bytes32 metadataHash;
    }

    struct DelegationSnapshot {
        uint64 termId;
        address delegator;
        address delegatee;
        uint96 votingWeight;
    }

    struct Challenge {
        bytes32 challengeId;
        uint64 termId;
        address challenger;
        uint32 seatId;
        bytes32 reasonHash;
        uint256 bond;
        bool resolved;
        bool upheld;
    }

    uint64 public currentTermId;
    uint32 public seatCount;
    mapping(uint32 => Seat) public seats;
    mapping(uint64 => mapping(address => address)) public delegationOf;
    mapping(uint64 => DelegationSnapshot[]) internal _termSnapshots;
    mapping(bytes32 => Challenge) public challenges;
    mapping(address => bool) public electionAdmins;

    event TermOpened(uint64 indexed termId);
    event SeatAssigned(uint64 indexed termId, uint32 indexed seatId, address occupant, uint96 weight, SeatStatus status);
    event SeatStatusChanged(uint64 indexed termId, uint32 indexed seatId, SeatStatus status);
    event Delegated(uint64 indexed termId, address indexed delegator, address indexed delegatee, uint96 votingWeight);
    event ChallengeOpened(bytes32 indexed challengeId, uint64 indexed termId, uint32 indexed seatId, address challenger, bytes32 reasonHash, uint256 bond);
    event ChallengeResolved(bytes32 indexed challengeId, bool upheld);

    modifier onlyElectionAdmin() {
        require(electionAdmins[msg.sender] || msg.sender == owner(), "NOT_ELECTION_ADMIN");
        _;
    }

    constructor(address initialOwner) Ownable(initialOwner) {}

    /// @notice Sets election admin permissions.
    function setElectionAdmin(address admin, bool allowed) external onlyOwner {
        electionAdmins[admin] = allowed;
    }

    /// @notice Opens a new governance term.
    function openTerm() external onlyElectionAdmin returns (uint64 termId) {
        termId = ++currentTermId;
        emit TermOpened(termId);
    }

    /// @notice Assigns a seat and records lifecycle metadata.
    function assignSeat(uint32 seatId, address occupant, uint96 weight, bool active, bytes32 metadataHash) external onlyElectionAdmin {
        if (seatId == 0 || seatId > seatCount) {
            seatCount += 1;
            seatId = seatCount;
        }
        SeatStatus status = active ? SeatStatus.ACTIVE : SeatStatus.INACTIVE;
        seats[seatId] = Seat({
            occupant: occupant,
            weight: weight,
            status: status,
            activatedAt: active ? uint64(block.timestamp) : 0,
            deactivatedAt: active ? 0 : uint64(block.timestamp),
            retiredAt: 0,
            metadataHash: metadataHash
        });
        emit SeatAssigned(currentTermId, seatId, occupant, weight, status);
    }

    /// @notice Updates seat status with deterministic timestamps.
    function setSeatStatus(uint32 seatId, SeatStatus status) external onlyElectionAdmin {
        Seat storage s = seats[seatId];
        require(s.occupant != address(0), "NO_SEAT");
        s.status = status;
        if (status == SeatStatus.ACTIVE) {
            s.activatedAt = uint64(block.timestamp);
            s.deactivatedAt = 0;
        } else if (status == SeatStatus.INACTIVE) {
            s.deactivatedAt = uint64(block.timestamp);
        } else if (status == SeatStatus.RETIRED) {
            s.retiredAt = uint64(block.timestamp);
            s.deactivatedAt = uint64(block.timestamp);
        }
        emit SeatStatusChanged(currentTermId, seatId, status);
    }

    /// @notice Delegates voting weight in the active term.
    function delegate(address delegatee, uint96 votingWeight) external {
        delegationOf[currentTermId][msg.sender] = delegatee;
        _termSnapshots[currentTermId].push(DelegationSnapshot(currentTermId, msg.sender, delegatee, votingWeight));
        emit Delegated(currentTermId, msg.sender, delegatee, votingWeight);
    }

    /// @notice Reads delegation snapshots for a term.
    function delegationSnapshots(uint64 termId) external view returns (DelegationSnapshot[] memory) {
        return _termSnapshots[termId];
    }

    /// @notice Opens a challenge against a seat with an economic bond.
    function openSeatChallenge(uint32 seatId, bytes32 reasonHash) external payable returns (bytes32 challengeId) {
        require(seats[seatId].occupant != address(0), "NO_SEAT");
        require(msg.value > 0, "BOND_REQUIRED");
        challengeId = keccak256(abi.encodePacked(block.chainid, currentTermId, seatId, msg.sender, reasonHash, block.timestamp));
        challenges[challengeId] = Challenge(challengeId, currentTermId, msg.sender, seatId, reasonHash, msg.value, false, false);
        emit ChallengeOpened(challengeId, currentTermId, seatId, msg.sender, reasonHash, msg.value);
    }

    /// @notice Resolves a challenge and updates seat status when upheld.
    function resolveSeatChallenge(bytes32 challengeId, bool upheld) external onlyElectionAdmin {
        Challenge storage c = challenges[challengeId];
        require(!c.resolved, "ALREADY_RESOLVED");
        c.resolved = true;
        c.upheld = upheld;
        if (upheld) {
            seats[c.seatId].status = SeatStatus.INACTIVE;
            seats[c.seatId].deactivatedAt = uint64(block.timestamp);
            payable(c.challenger).transfer(c.bond);
        } else {
            payable(owner()).transfer(c.bond);
        }
        emit ChallengeResolved(challengeId, upheld);
    }
}
