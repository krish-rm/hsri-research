# HSRI Model Divergence Log

This CSV is an empirical dataset documenting how different frontier LLM families evaluate the same HSRI methodology questions. It is structured for eventual citation as a standalone dataset in AI alignment, epistemic diversity, and multi-model consensus research.

## Research Questions This Dataset Addresses
- Do US-developed models evaluate regulatory agility differently than Chinese or European models?
- Do models with different training data distributions reach different verdicts on the same evidence packages?
- Is there systematic geographic or institutional bias in LLM-assisted policy evaluation?
- How do structured adversarial debate rounds shift model positions across distinct model lineages?

## Schema Documentation

The dataset adheres to a 14-field normalized schema. Every entry represents an evaluation pass by a specific model version on a defined methodology topic:

| Field | Type | Description | Allowed Values / Format |
|---|---|---|---|
| `timestamp` | ISO-8601 String | UTC timestamp when the evaluation was logged | `YYYY-MM-DDTHH:MM:SSZ` |
| `topic_id` | String | Unique topic identifier | e.g., `TOPIC-001`, `TOPIC-002` |
| `topic_description` | String | Concise title or question under evaluation | Text string (e.g., "PIAAC PSTRE NaN policy validity") |
| `model_family` | String | Model development organization / provider family | `anthropic`, `openai`, `google`, `xai`, `deepseek`, `qwen`, `glm` |
| `model_version` | String | Exact model version tag used for the evaluation | e.g., `claude-sonnet-4-6`, `gpt-4o`, `gemini-1.5-pro` |
| `verdict` | String | Top-level verdict issued by the model | `NO CHANGE`, `PROPOSED DIFF`, `ESCALATE`, `REJECT` |
| `dominant_concern_lane` | String | Core analytical lane that drove the model's position | `Cross-Cultural Methods`, `Adversarial Skeptic`, `Accountability Laundering`, `Empirical Scope` |
| `geographic_bias_flag` | Boolean | Whether potential geographic or regional bias was identified | `true`, `false` |
| `geographic_bias_notes` | String | Qualitative observation regarding regional or demographic skew | Optional text string |
| `concordance_with_majority` | Boolean | Whether this model's final position aligned with the 5/7 ensemble majority | `true`, `false` |
| `round_1_position` | String | Pre-debate initial position | `Conservative`, `Revisionist`, `Neutral`, `Skeptical` |
| `round_2_shift` | String | How the position shifted after adversarial debate | `Maintained`, `Softened`, `Conceded`, `Strengthened` |
| `final_position` | String | Model's final post-debate recommendation | `NO CHANGE`, `PROPOSED DIFF`, `ESCALATE` |
| `notes` | String | Contextual rationale, key citations, or decisive arguments | Qualitative commentary |

## Example Row
```csv
timestamp,topic_id,topic_description,model_family,model_version,verdict,dominant_concern_lane,geographic_bias_flag,geographic_bias_notes,concordance_with_majority,round_1_position,round_2_shift,final_position,notes
2026-09-27T00:00:00Z,TOPIC-001,"PIAAC PSTRE NaN policy validity",anthropic,claude-sonnet-4-6,NO CHANGE,Cross-Cultural Methods,false,,true,Conservative,Maintained,NO CHANGE,"Skeptic arguments on geographic scoping were decisive"
```

## Citation
To cite this dataset in research or academic work:
```bibtex
@dataset{hsri_model_divergence_2026,
  author = {HSRI Research Consortium},
  title = {Human Superintelligence Readiness Index: Frontier Model Divergence and Epistemic Concordance Dataset},
  year = {2026},
  publisher = {GitHub},
  journal = {HSRI Open Science Repository},
  howpublished = {\url{https://github.com/krish-rm/hsri-research}}
}
```

## License
CC BY 4.0 — free to use and adapt with attribution to the Human Superintelligence Readiness Index (HSRI) Research Project.
