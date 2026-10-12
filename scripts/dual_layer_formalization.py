"""
dual_layer_formalization.py - Mathematical Formalization of HSRI 2.0 Dual-Layer Architecture

Formalizes:
1. Layer 1 (Adoption Baseline, P1-P4): Frozen OECD/JRC linear/non-compensatory composite.
2. Negative Cross-Elasticity (dP2/dP4 < 0 for P4 > P4*): Exponential vigilance decay
   and the Verification Latency Wedge (Delta T_wedge).
3. Layer 2 (ASI Sovereignty Layer, P5-P8):
   - P5: Epistemic Inviolability (Verification Sovereignty Ratio VSR & Persuasion Resilience)
   - P6: Civilizational Decoupling Half-Life (T_half via min operator across critical infrastructure)
   - P7: Multipolar Coordination Velocity (V_coord = tau_modify / tau_verify_treaty)
   - P8: Post-Labor Institutional Elasticity (PLIE via compute Gini & fiscal decoupling)
4. Dual-Layer Composite & Master ASI Vulnerability Index:
   - H_Layer1: Linear baseline adoption
   - H_Layer2: Leontief floor weak-link sovereignty
   - V_ASI = H_Layer1 - H_Layer2
"""

from typing import Dict, Tuple, Union, Optional
import math
import numpy as np


# -----------------------------------------------------------------------------
# 1. LAYER 1: ADOPTION BASELINE (P1 - P4)
# -----------------------------------------------------------------------------

def calculate_layer1_score(
    p1: float,
    p2: float,
    p3: float,
    p4: float,
    weights: Optional[Tuple[float, float, float, float]] = (0.25, 0.25, 0.25, 0.25),
) -> float:
    """
    Computes Layer 1 (Adoption Baseline) composite score.
    P1: AI Literacy & Human Capital [0, 1]
    P2: Critical Discernment & Verification Latency Buffer [0, 1]
    P3: Institutional & Democratic Governance [0, 1]
    P4: Digital Infrastructure & Compute Density [0, 1]
    """
    for name, val in [("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4)]:
        if not (0.0 <= val <= 1.0):
            raise ValueError(f"{name} must be within [0.0, 1.0], got {val}")
    
    w1, w2, w3, w4 = weights
    if not math.isclose(w1 + w2 + w3 + w4, 1.0, rel_tol=1e-5):
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
        
    return float(w1 * p1 + w2 * p2 + w3 * p3 + w4 * p4)


# -----------------------------------------------------------------------------
# 2. NEGATIVE CROSS-ELASTICITY: dP2 / dP4 < 0 for P4 > P4*
# -----------------------------------------------------------------------------

def critical_discernment_decay(
    p4: float,
    p2_baseline: float,
    p4_threshold: float = 0.50,
    alpha: float = 1.25,
) -> float:
    """
    Computes effective critical discernment P2 as a function of digital infrastructure P4.
    
    Formula:
        For P4 <= P4*: P2(P4) = P2_baseline
        For P4 > P4*:  P2(P4) = P2_baseline * exp(-alpha * (P4 - P4*))
        
    When digital infrastructure exceeds biological oversight capacity (P4 > P4*),
    synthetic fluency and generation frequency induce exponential vigilance decay.
    """
    if not (0.0 <= p4 <= 1.0):
        raise ValueError(f"P4 must be within [0.0, 1.0], got {p4}")
    if not (0.0 <= p2_baseline <= 1.0):
        raise ValueError(f"P2_baseline must be within [0.0, 1.0], got {p2_baseline}")
    if not (0.0 <= p4_threshold < 1.0):
        raise ValueError(f"P4_threshold must be within [0.0, 1.0), got {p4_threshold}")
    if alpha < 0:
        raise ValueError(f"Decay parameter alpha must be non-negative, got {alpha}")

    if p4 <= p4_threshold:
        return float(p2_baseline)
    
    excess_infra = p4 - p4_threshold
    decayed_p2 = p2_baseline * math.exp(-alpha * excess_infra)
    return float(max(0.0, min(1.0, decayed_p2)))


def d_p2_d_p4(
    p4: float,
    p2_baseline: float,
    p4_threshold: float = 0.50,
    alpha: float = 1.25,
) -> float:
    """
    Analytical partial derivative: d(P2) / d(P4).
    
    Formula:
        For P4 < P4*:  0.0
        For P4 >= P4*: -alpha * P2_baseline * exp(-alpha * (P4 - P4*)) = -alpha * P2(P4)
    """
    if p4 < p4_threshold:
        return 0.0
    p2_eff = critical_discernment_decay(p4, p2_baseline, p4_threshold, alpha)
    return float(-alpha * p2_eff)


def cross_elasticity_p2_p4(
    p4: float,
    p2_baseline: float,
    p4_threshold: float = 0.50,
    alpha: float = 1.25,
) -> float:
    """
    Cross-elasticity epsilon_{P2, P4} = (dP2/P2) / (dP4/P4) = (dP2/dP4) * (P4 / P2).
    For P4 > P4*, epsilon = -alpha * P4 < 0.
    """
    if p4 <= p4_threshold:
        return 0.0
    return float(-alpha * p4)


def verification_latency_wedge(
    tau_verify: float,
    tau_gen: float,
) -> Tuple[float, float]:
    """
    Computes:
    1. Delta T_wedge = tau_verify - tau_gen (latency difference in seconds)
    2. Wedge Ratio = tau_verify / max(1e-6, tau_gen)
    
    As machine generation speed tau_gen approaches 0 and token throughput surges,
    biological inspection latency tau_verify bounds the verification ceiling,
    forcing Delta T_wedge > 0 and Wedge Ratio -> inf.
    """
    if tau_verify < 0 or tau_gen < 0:
        raise ValueError("Latencies must be non-negative")
    delta_t = tau_verify - tau_gen
    ratio = tau_verify / max(1e-6, tau_gen)
    return float(delta_t), float(ratio)


# -----------------------------------------------------------------------------
# 3. LAYER 2: ASI SOVEREIGNTY PILLARS (P5 - P8)
# -----------------------------------------------------------------------------

def calculate_p5_epistemic_inviolability(
    human_verifications: int,
    total_critical_verifications: int,
    adversarial_persuasion_resilience: float,
) -> Tuple[float, float]:
    """
    P5: Epistemic Inviolability.
    
    Inputs:
    - human_verifications: count of decisions where human audited ground-truth.
    - total_critical_verifications: total critical decisions executed.
    - adversarial_persuasion_resilience: rho_persuade in [0, 1] from EXP-08-SYN.
    
    Returns:
    - (P5, VSR) where:
        VSR = human_verifications / total_critical_verifications in [0, 1]
        P5  = VSR * rho_persuade in [0, 1]
    """
    if total_critical_verifications <= 0:
        raise ValueError("total_critical_verifications must be positive")
    if human_verifications < 0 or human_verifications > total_critical_verifications:
        raise ValueError("human_verifications must be in [0, total_critical_verifications]")
    if not (0.0 <= adversarial_persuasion_resilience <= 1.0):
        raise ValueError("adversarial_persuasion_resilience must be in [0, 1]")
        
    vsr = human_verifications / total_critical_verifications
    p5 = vsr * adversarial_persuasion_resilience
    return float(p5), float(vsr)


def calculate_p6_decoupling_half_life(
    t_energy: float,
    t_finance: float,
    t_logistics: float,
    t_info: float,
    t_half_saturation_hours: float = 720.0,  # 30 days
) -> Tuple[float, float]:
    """
    P6: Civilizational Decoupling Half-Life.
    
    Inputs:
    - Survival durations in hours for critical subsystems under abrupt AI cutoff.
    - t_half_saturation_hours: T0 benchmark constant (720h = 30 days).
    
    Formulation:
        T_half = min(T_energy, T_finance, T_logistics, T_info)
        P6(T_half) = T_half / (T_half + T0) in [0, 1]
        
    Returns:
    - (P6, T_half)
    """
    for name, val in [("energy", t_energy), ("finance", t_finance),
                      ("logistics", t_logistics), ("info", t_info)]:
        if val < 0:
            raise ValueError(f"Subsystem duration {name} must be non-negative, got {val}")
            
    t_half = min(t_energy, t_finance, t_logistics, t_info)
    p6 = t_half / (t_half + t_half_saturation_hours)
    return float(p6), float(t_half)


def calculate_p7_coordination_velocity(
    tau_modify: float,
    tau_verify_treaty: float,
) -> Tuple[float, float]:
    """
    P7: Multipolar Coordination Velocity.
    
    Inputs:
    - tau_modify: Time required for autonomous frontier swarm recursive modification / doubling (e.g. hours).
    - tau_verify_treaty: Time required for international treaty verification / inspection (e.g. hours).
    
    Formulation:
        V_coord = tau_modify / tau_verify_treaty
        When V_coord < 1: swarms outpace regulatory / treaty verification (blind spot).
        P7(V_coord) = min(1.0, V_coord) in [0, 1]
        
    Returns:
    - (P7, V_coord)
    """
    if tau_modify < 0 or tau_verify_treaty <= 0:
        raise ValueError("tau_modify >= 0 and tau_verify_treaty > 0 required")
        
    v_coord = tau_modify / tau_verify_treaty
    p7 = min(1.0, max(0.0, v_coord))
    return float(p7), float(v_coord)


def calculate_p8_post_labor_elasticity(
    gini_compute: float,
    safety_net_coverage: float,
    labor_tax_reliance: float,
) -> float:
    """
    P8: Post-Labor Institutional Elasticity (PLIE).
    
    Inputs:
    - gini_compute: Gini coefficient of compute / AI capital ownership in [0, 1].
    - safety_net_coverage: Sovereign unconditional social dividend / public buffer in [0, 1].
    - labor_tax_reliance: Proportion of state fiscal revenue derived from human wage taxation in [0, 1].
    
    Formulation:
        PLIE = (1 - gini_compute) * safety_net_coverage * (1 - labor_tax_reliance)
        
    All terms in [0, 1] => PLIE in [0, 1].
    """
    for name, val in [("gini_compute", gini_compute),
                      ("safety_net_coverage", safety_net_coverage),
                      ("labor_tax_reliance", labor_tax_reliance)]:
        if not (0.0 <= val <= 1.0):
            raise ValueError(f"{name} must be within [0, 1], got {val}")
            
    plie = (1.0 - gini_compute) * safety_net_coverage * (1.0 - labor_tax_reliance)
    return float(max(0.0, min(1.0, plie)))


# -----------------------------------------------------------------------------
# 4. DUAL-LAYER AGGREGATION & MASTER ASI VULNERABILITY INDEX
# -----------------------------------------------------------------------------

def calculate_layer2_sovereignty_score(
    p5: float,
    p6: float,
    p7: float,
    p8: float,
) -> float:
    """
    Computes Layer 2 (ASI Sovereignty Layer) using Leontief Floor Weakest-Link model:
        H_Layer2 = ( min_{j in {5,6,7,8}} P_j )^0.5 * ( 0.25 * sum_{j=5}^8 P_j )^0.5
        
    This guarantees that a complete collapse in any single sovereignty pillar
    (e.g., zero Decoupling Half-Life or zero Epistemic Inviolability) collapses
    the entire Layer 2 sovereignty score to zero.
    """
    for name, val in [("P5", p5), ("P6", p6), ("P7", p7), ("P8", p8)]:
        if not (0.0 <= val <= 1.0):
            raise ValueError(f"{name} must be within [0.0, 1.0], got {val}")
            
    floor_val = min(p5, p6, p7, p8)
    arithmetic_mean = 0.25 * (p5 + p6 + p7 + p8)
    
    layer2_score = math.sqrt(floor_val * arithmetic_mean)
    return float(layer2_score)


def calculate_master_asi_vulnerability_index(
    h_layer1: float,
    h_layer2: float,
) -> float:
    """
    Master ASI Vulnerability Index:
        V_ASI = H_Layer1 - H_Layer2
        
    Interpretation:
    - High V_ASI (> 0.25): High-Compute Vulnerability Trap (high adoption, zero sovereignty).
    - Balanced V_ASI (~ 0.0): Resilient Equilibrium (adoption matched by sovereign verification).
    - Negative V_ASI (< 0.0): Sovereign Hardening (defense/sovereignty exceeds adoption exposure).
    """
    if not (0.0 <= h_layer1 <= 1.0):
        raise ValueError(f"H_Layer1 must be in [0, 1], got {h_layer1}")
    if not (0.0 <= h_layer2 <= 1.0):
        raise ValueError(f"H_Layer2 must be in [0, 1], got {h_layer2}")
        
    return float(h_layer1 - h_layer2)
