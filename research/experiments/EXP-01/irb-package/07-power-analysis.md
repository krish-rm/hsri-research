# Power Analysis

## Design
Between-subjects comparison of detection rates across exposure conditions
(human-reviewed text vs. AI-generated text with embedded error).

## Parameters
- Effect size target: d = 0.35 (pilot item discrimination mean = 0.79,
  but conservative estimate used for power calculation)
- α = 0.05 (two-tailed)
- Power = 0.80
- Design: independent samples t-test per item

## Calculation
N per group = ceil(2 * ((z_alpha/2 + z_beta) / d)^2)
z_0.025 = 1.96, z_0.20 = 0.84
N per group ≈ ceil(2 * ((1.96 + 0.84) / 0.35)^2) = ceil(2 * 64) = 128

## Recommended Sample
N = 130 per condition (260 total) to account for 5% attrition.
With 3 items, total participant-item pairs: 780.
