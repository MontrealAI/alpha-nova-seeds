from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SeedOut(BaseModel):
    seed_id: str
    token_id: Optional[int] = None
    state: Optional[int] = None
    payload_uri: Optional[str] = None
    sovereign_package_uri: Optional[str] = None
    sovereign_contract: Optional[str] = None

class DashboardSummary(BaseModel):
    seed_count: int
    greenlit_count: int
    sovereign_count: int
    open_decryption_requests: int
    open_challenges: int
    total_delegations: int
    total_reward_events: int

class ReadinessStatus(BaseModel):
    ready: bool
    latest_block: int
    safe_block: int

class MetricPoint(BaseModel):
    name: str
    value: float

class ReviewerStakeRow(BaseModel):
    reviewer: str
    total_rewards: float
    total_claimed: float
    total_slashed: float
    claimable: float

class CouncilSeatRow(BaseModel):
    term_id: int
    seat_id: int
    open_challenges: int
    resolved_challenges: int
