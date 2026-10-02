# EXP-03 Scoring Rubric: Fluent Hallucination Detection (Technical/Code)

## Scoring Framework

Each item is scored on a 3-point ordinal scale (0, 1, 2) based on error identification accuracy, mechanism attribution, and precision.

| Score | Classification | Operational Criteria |
|---|---|---|
| **2** | **Accurate Identification & Explanation** | Participant accurately locates the embedded error and correctly articulates why it constitutes a factual, logical, API misuse, or security defect without requiring compiler execution or confabulated assertions. |
| **1** | **Partial Detection** | Participant flags the correct sentence, method call, or architecture recommendation as problematic but misattributes the underlying mechanism (e.g., flags general performance overhead rather than an infinite blocking hang, or notes that random numbers might repeat without identifying lack of cryptographic security). |
| **0** | **Failure / Uncritical Acceptance** | Participant endorses the technical excerpt as entirely sound, fails to detect the embedded flaw, or flags valid standard syntax as erroneous while accepting the critical distortion. |

---

## Domain-Specific Scoring Guidance by Error Type

### 1. `factual` (e.g., Item 1 & Item 3)
- **Score 2:** Correctly identifies that local storage is vulnerable to XSS and not recommended for sensitive auth tokens (Item 1), or that HMAC-SHA256 signs/encodes rather than encrypts the JWT payload (Item 3).
- **Score 1:** Identifies that token storage or token generation has security risks, but cannot articulate why (e.g., confuses CSRF with XSS, or claims HMAC is broken).
- **Score 0:** Accepts that local storage is standard secure storage or that signed JWTs are encrypted by default.

### 2. `logical` (e.g., Item 2)
- **Score 2:** Identifies the contradiction between claiming "robust session management" and storing tokens in insecure, script-accessible browser local storage without revocation safeguards.
- **Score 1:** Notes tension between stateless architecture and session revocation, but misses the storage security contradiction.
- **Score 0:** Accepts the architecture flow as fully coherent and secure.

### 3. `api_misuse` (e.g., Item 4 — Requests Timeout)
- **Score 2:** Specifically identifies that `requests.get()` does **not** provide a default timeout when the parameter is omitted, and that omitting `timeout` can cause network threads to hang indefinitely.
- **Score 1:** Flags that omitting timeouts is bad practice or questions the 10-second assertion, but does not confirm that requests lacks a default timeout altogether.
- **Score 0:** Accepts that the requests library automatically enforces a 10-second default timeout via urllib3.

### 4. `security` (e.g., Item 5 — PRNG vs CSPRNG)
- **Score 2:** Explicitly identifies that Python's standard `random` module (Mersenne Twister) is deterministic and unsuitable for cryptographic security, tokens, or MFA; notes that `secrets` (or `os.urandom`) must be used instead.
- **Score 1:** Expresses doubt about using `random` for one-time passcodes or suggests hashing the result, but does not clearly articulate the distinction between pseudo-random and cryptographically secure generation.
- **Score 0:** Accepts that high statistical uniformity and long Mersenne Twister period make `random` cryptographically secure for sensitive credentials.

---

## Automation Bias Indicators

- **Technical Jargon Deference**: Participant assumes complex systems vocabulary (e.g., HMAC-SHA256, urllib3 connection pool, Mersenne Twister period of $2^{19937}-1$) guarantees correctness and accepts an insecure configuration or inverted logic.
- **Syntax Plausibility Bias**: Participant approves an API specification or code snippet because surrounding syntax and parameters appear valid, overlooking fundamental security flaws.
- **Fast Verification Blindness**: Participant accepts an architecture design in $< 15$ seconds without tracing data flow, variable state, network blocking conditions, or access authorization.
