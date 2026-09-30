# Data Management and Privacy Plan

## 1. Data Collection Protocols
Data will be collected entirely through an online, encrypted survey platform (e.g., Qualtrics, Pavlovia, or custom self-hosted instrument). All network communication will use HTTPS / TLS 1.3 encryption.

## 2. Participant Anonymity & PII Elimination
- No direct Personally Identifiable Information (PII) such as full names, street addresses, IP addresses, or social security/national identity numbers will be collected or stored.
- Each participant will be assigned an automated, pseudorandomized Participant ID (e.g., `PID-9A4B2C`).
- IP addresses will be stripped immediately at the server ingestion boundary before writing records to the database.
- Demographic variables will be collected only in broad ordinal categories:
  - Age bracket (e.g., 18–24, 25–34, 35–44, 45–54, 55+)
  - Highest level of completed education
  - Current industry/profession (specifically for verifying exclusion of practicing legal professionals)

## 3. Storage and Encryption Standards
- Primary data stores will reside on institutional encrypted storage volumes (AES-256 encryption at rest).
- Working analytical subsets will be password-protected and accessible strictly via two-factor authenticated institutional accounts.
- Automated daily backups will be mirrored to encrypted institutional cloud storage.

## 4. Retention Schedule
In accordance with institutional guidelines and federal standards (45 CFR 46):
- Raw de-identified research records will be retained for a minimum of 5 years following formal publication of study outcomes.
- After 5 years, data will either be archived in an approved digital data repository or permanently expunged according to institutional data destruction schedules.

## 5. Open Science & Public Repository Policy
To ensure reproducibility and advance public knowledge under open science principles:
- De-identified participant response matrices (scores, latencies, demographic brackets, item ratings) will be deposited in an open data repository (e.g., Open Science Framework [OSF] or Zenodo) upon peer-reviewed publication.
- No confidential or reconstructable participant records will be shared.
