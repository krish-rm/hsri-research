# Raw Source Data Archive (`data/raw/`)

This directory stores authentic raw and primary source datasets downloaded or extracted from primary institutional providers (World Bank, OECD, V-Dem, ITU, UNESCO, IMF, etc.).

## Directory Hierarchy

Each provider has a dedicated subdirectory keyed by `source_id`:

```
data/raw/
├── README.md
├── WGI_WorldBank/           # Worldwide Governance Indicators (World Bank API / bulk extract)
├── VDEM_Vdem/               # Varieties of Democracy (V-Dem Institute open dataset)
├── PISA_OECD/               # OECD PISA 2022 Digital Reading & Fact vs Opinion tables
├── UNESCO_STEM/             # UNESCO Institute for Statistics (UIS) Tertiary Education data
├── ITU_SKILLS/              # International Telecommunication Union Digital Development data
├── IMF_AI/                  # IMF AI Preparedness Index published tables
├── OXFORD_AI/               # Oxford Insights Government AI Readiness dataset
└── EMLI_CouncilEurope/      # European Media Literacy Index (OSIS / Council of Europe)
```

## Ingestion & Provenance Standard

1. **No Manual Fudging:** Raw files are saved in their unmodified format (`.csv`, `.json`, or tabular `.tsv`).
2. **Missingness Preservation:** When an economy is not included in a provider's survey sample, the ingestion parser must output `NaN` or `None`. Under no circumstance may values be imputed or carried across geographic borders.
3. **Reproducibility:** All programmatic download scripts reside in [`scripts/ingestion/`](../../scripts/ingestion/).
