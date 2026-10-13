"""
hsri_engine.models - Pydantic Schemas for HSRI 2.0 Engine Core API
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator


class PillarInput(BaseModel):
    """Pillar scores normalized to [0.0, 1.0]."""
    p1: float = Field(..., ge=0.0, le=1.0, description="P1: AI Literacy & Human Capital")
    p2: float = Field(..., ge=0.0, le=1.0, description="P2: Critical Discernment & Verification Latency Buffer")
    p3: float = Field(..., ge=0.0, le=1.0, description="P3: Institutional & Democratic Governance")
    p4: float = Field(..., ge=0.0, le=1.0, description="P4: Digital Infrastructure & Compute Density")
    p5: Optional[float] = Field(None, ge=0.0, le=1.0, description="P5: Epistemic Inviolability (Layer 2)")
    p6: Optional[float] = Field(None, ge=0.0, le=1.0, description="P6: Civilizational Decoupling Half-Life (Layer 2)")
    p7: Optional[float] = Field(None, ge=0.0, le=1.0, description="P7: Multipolar Coordination Velocity (Layer 2)")
    p8: Optional[float] = Field(None, ge=0.0, le=1.0, description="P8: Post-Labor Institutional Elasticity (Layer 2)")


class RawTelemetryInput(BaseModel):
    """Raw infrastructure and human-AI telemetry metrics."""
    human_verifications: Optional[int] = Field(None, ge=0, description="Count of human ground-truth verified actions")
    total_critical_verifications: Optional[int] = Field(None, gt=0, description="Total critical autonomous decisions")
    adversarial_persuasion_resilience: Optional[float] = Field(None, ge=0.0, le=1.0, description="Persuasion resistance rho in [0, 1]")
    t_energy: Optional[float] = Field(None, ge=0.0, description="Energy grid survival duration under AI cutoff (hours)")
    t_finance: Optional[float] = Field(None, ge=0.0, description="Financial clearing survival duration (hours)")
    t_logistics: Optional[float] = Field(None, ge=0.0, description="Supply chain/food survival duration (hours)")
    t_info: Optional[float] = Field(None, ge=0.0, description="Telecom/routing survival duration (hours)")
    tau_modify: Optional[float] = Field(None, ge=0.0, description="Autonomous swarm recursive doubling time (hours)")
    tau_verify_treaty: Optional[float] = Field(None, gt=0.0, description="Treaty inspection/verification time (hours)")
    gini_compute: Optional[float] = Field(None, ge=0.0, le=1.0, description="Gini coefficient of compute concentration")
    safety_net_coverage: Optional[float] = Field(None, ge=0.0, le=1.0, description="Unconditional social dividend buffer")
    labor_tax_reliance: Optional[float] = Field(None, ge=0.0, le=1.0, description="Proportion of state revenue from human wages")
    tau_verify: Optional[float] = Field(None, ge=0.0, description="Human expert audit latency (seconds)")
    tau_gen: Optional[float] = Field(None, ge=0.0, description="Machine artifact generation latency (seconds)")


class EvaluationRequest(BaseModel):
    """Request payload for evaluating infrastructure sovereignty."""
    entity_id: str = Field("custom-node", description="Unique entity or nation identifier")
    entity_name: str = Field("Custom Infrastructure Node", description="Human-readable name")
    pillars: Optional[PillarInput] = Field(None, description="Pre-calculated pillar scores P1-P8")
    telemetry: Optional[RawTelemetryInput] = Field(None, description="Raw telemetry to calculate P5-P8 dynamically")
    layer1_weights: Optional[List[float]] = Field(
        [0.25, 0.25, 0.25, 0.25],
        description="Weights for P1-P4 (must sum to 1.0)"
    )
    apply_negative_cross_elasticity: bool = Field(
        False,
        description="Whether to apply empirical exponential discernment decay to P2 based on P4"
    )

    @field_validator("layer1_weights")
    @classmethod
    def validate_weights(cls, v):
        if v is not None:
            if len(v) != 4:
                raise ValueError("layer1_weights must contain exactly 4 values")
            if not (0.999 <= sum(v) <= 1.001):
                raise ValueError(f"layer1_weights must sum to 1.0, got {sum(v)}")
        return v


class EvaluationResponse(BaseModel):
    """Evaluation output schema providing full dual-layer sovereignty diagnostics."""
    entity_id: str
    entity_name: str
    layer1_score: float = Field(..., description="Linear baseline adoption score")
    layer2_score: float = Field(..., description="Leontief floor weak-link sovereignty score (beta=0.50)")
    geometric_score: float = Field(..., description="Non-compensatory geometric mean score")
    choquet_score: float = Field(..., description="Choquet 2-additive capacity integral score")
    master_vulnerability_index: float = Field(..., description="V_ASI = Layer1 - Layer2")
    is_high_compute_trap: bool = Field(..., description="True if V_ASI >= 0.25 and P4 >= 0.70")
    weakest_link_pillar: str = Field(..., description="Pillar governing the Leontief floor")
    weakest_link_score: float = Field(..., description="Score of the governing bottleneck pillar")
    pillars: Dict[str, float] = Field(..., description="Individual normalized scores for P1 through P8")
    sovereignty_diagnostics: Dict[str, Any] = Field(..., description="Telemetry diagnostics (VSR, T_half, V_coord, PLIE, Wedge)")
    timestamp: str


class MonteCarloRequest(BaseModel):
    """Request payload for JRC Step 7 Dirichlet Monte Carlo sensitivity analysis."""
    evaluation_request: EvaluationRequest
    iterations: int = Field(500, ge=50, le=2000, description="Monte Carlo iterations")
    alpha_dirichlet: float = Field(1.0, gt=0.0, description="Concentration parameter for Dirichlet distribution")


class MonteCarloResponse(BaseModel):
    """Monte Carlo sensitivity results."""
    entity_id: str
    iterations: int
    mean_layer2_score: float
    std_layer2_score: float
    ci_95_lower: float
    ci_95_upper: float
    kendall_w_concordance: float
    vulnerability_stability: str


class BenchmarkSummaryResponse(BaseModel):
    """Summary of the 39-nation official empirical benchmark."""
    total_nations: int
    benchmark_version: str
    doi: str
    top_sovereign_nations: List[Dict[str, Any]]
    high_compute_traps: List[Dict[str, Any]]


class PrecursorTelemetryResponse(BaseModel):
    """Real-time precursor seismograph telemetry status."""
    master_threat_score: float
    overall_classification: str
    cors_score: float
    cors_description: str
    latency_wedge_seconds: float
    latency_wedge_ratio: float
    tripwires_active_critical: int
    tripwires_triggering_amber: int
    tripwires_latent_green: int
    total_tripwires: int
