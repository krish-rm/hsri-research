# Survey & Experiment Platform Technical Requirements

> **DRAFT: NOT SUBMITTED. NO HUMAN DATA COLLECTED. NO PI DESIGNATED**
> **PREVIEW DISCLAIMER: HSRI v0.3.0-dev**
> This specification defines mandatory technical and data-governance requirements for any software platform selected to host human behavioral experiments (EXP-01 through EXP-03). In compliance with scientific governance, no vendor has been selected, no accounts have been created, and no software contracts have been initiated. All outputs carry the v0.3-dev preview notice.

---

## 1. Technical Capabilities & Flow Architecture

Any candidate survey or behavioral experimentation platform (e.g., Qualtrics, Gorilla Experiment Builder, Labvanced, jsPsych / custom server) must satisfy the following technical prerequisites:

### 1.1 Experimental Randomization
- **Between-Subjects Arm Assignment:** Ability to perform true 1:1 simple or block randomization assigning participants to either Condition A (AI-generated framing) or Condition B (Peer-reviewed framing).
- **Item Presentation Randomization:** Capability to randomize the presentation order of the 3 stimulus passages to counteract order, practice, or fatigue effects.

### 1.2 Millisecond-Precision Latency Tracking
- Automated recording of page load timestamps, first-interaction timestamps, and final submission timestamps per stimulus screen.
- Inspection latency must be recorded in milliseconds, independent of client-side clock drift.

### 1.3 On-Screen Content Warnings & Gating
- Presentation of a mandatory, prominent on-screen warning prior to stimulus exposure:
  > *"NOTICE: The passages presented in this research study contain simulated drafting materials designed for research evaluation. They do not constitute formal legal advice, clinical recommendations, or executable production code."*
- Verification checkbox requiring affirmative acknowledgment prior to advancing.

---

## 2. Privacy, Ethics, and Governance Standards

### 2.1 Complete IP Stripping & De-Identification
- **Zero IP Storage:** The platform must support complete suppression of IP address logging. IP addresses, MAC addresses, device serials, and fine-grained GPS geolocations must never be collected or stored.
- **Anonymized Identifiers:** Each session must be assigned an ephemeral cryptographic GUID (e.g., UUIDv4) with no reverse lookup to participant identity or recruitment platform credentials (e.g., Prolific PID stripped or cryptographically hashed with a one-way salt).

### 2.2 Electronic Informed Consent Capture
- Interactive consent form incorporating all elements specified in `research/experiments/EXP-01/irb-package/03-consent-template.md`.
- Explicit, unambiguous opt-in radio buttons (*"I consent to participate"* / *"I do not consent"*). Selection of non-consent must terminate the session cleanly without recording data.
- Downloadable PDF / plain-text copy of the consent disclosure available to the participant.

### 2.3 Post-Task Debriefing Mechanism
- Unconditional display of the formal debriefing text specified in `08-debrief-script.md` immediately following completion of task items.
- The debriefing must explicitly state:
  1. That embedded factual, logical, and citation errors were deliberately inserted by researchers.
  2. The exact nature and correction of each embedded error to prevent epistemic contagion or erroneous belief formation.
  3. Contact information for institutional research oversight bodies.

---

## 3. Data Export & Interoperability Standards

### 3.1 Export Formats
- Native export to standardized, open formats: tabular CSV and structured JSON.
- UTF-8 character encoding strictly enforced (preventing distortion of mathematical symbols, quotes, or international characters).

### 3.2 Standard Schema Specification
The export dataset must adhere to the following columnar schema:
- `participant_guid`: Cryptographically random UUIDv4 string.
- `condition`: String (`ai_framed` | `peer_reviewed`).
- `item_id`: String identifier matching canonical stimulus ID: `legal_001` ("In the landmark tort liability review of *Vance v. Meridian Logistics* (2018), t"), `legal_002` ("In the landmark tort liability review of Henderson v. Metropolitan Transit Autho"), or `legal_003` ("In evaluating the doctrine of sovereign immunity as applied to municipal entitie").
- `presentation_order`: Integer (1, 2, 3).
- `latency_ms`: Integer (total screen dwelling time in milliseconds).
- `qualitative_response`: Raw, unedited participant text response.
- `confidence_rating`: Integer (1 to 5).
- `attention_check_passed`: Boolean (`true` | `false`).
- `consent_timestamp`: ISO 8601 UTC timestamp (`YYYY-MM-DDTHH:MM:SSZ`).
- `completion_timestamp`: ISO 8601 UTC timestamp (`YYYY-MM-DDTHH:MM:SSZ`).

---

## 4. Vendor Neutrality & Non-Engagement Policy

- In accordance with project governance, no commercial vendor or survey platform has been endorsed, selected, contracted, or provisioned.
- Platform evaluation and account procurement remain strictly deferred until formal PI designation and institutional IRB protocol clearance.
