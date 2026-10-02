# Data Management and Privacy Plan (EXP-02)

> **PREVIEW NOTICE: HSRI v0.3.0-dev**
> This research document is an exploratory artifact from the Human Superintelligence Readiness Index (HSRI) behavioral lab pipeline. Synthetic-persona pilots test stimulus behavior only and do not provide evidence about human cognition. Stimuli cleared for IRB submission. Not validated on human participants.

## 1. Data Collection Protocols
Data collection is conducted via a secure web-based survey instrument. All client-server communications use HTTPS with TLS 1.3 protocol encryption.

## 2. Participant Anonymity & PII/PHI Elimination
- Under HIPAA and 45 CFR Part 46, no Protected Health Information (PHI) and no direct Personally Identifiable Information (PII) is collected.
- Participant sessions are assigned a random pseudonymous identifier (e.g. `EXP02-SUB-8291F`).
- Client IP addresses are stripped at the server web server gateway prior to recording trial data.
- Demographic variables are restricted to broad categorical ranges:
  - Age bracket (18–24, 25–34, 35–44, 45–54, 55+)
  - Highest completed education level
  - Clinical profession screener (affirmative/negative only, used strictly for eligibility exclusion)

## 3. Storage and Encryption Standards
- Server databases reside on encrypted storage volumes utilizing AES-256 encryption at rest.
- Analytical working copies are accessible exclusively by authorized research staff via two-factor authentication.
- Automated system backups are encrypted and stored in secure institutional cloud environments.

## 4. Retention Schedule
- De-identified research trial records will be retained for five (5) years following initial publication in peer-reviewed scientific journals, in accordance with institutional policy.
- Following the retention period, digital archives will either be permanently transitioned to an approved open scientific repository or securely expunged per institutional data destruction guidelines.

## 5. Open Science & Reproducibility Policy
To support scientific reproducibility under open access standards:
- Fully de-identified trial data (accuracy scores, response latencies, ordinal confidence ratings, demographic brackets) will be archived on the Open Science Framework (OSF) and/or Zenodo upon publication.
- No individual-level identifiers or unscrubbed free-text records containing potential self-identifying participant disclosures will be published.
