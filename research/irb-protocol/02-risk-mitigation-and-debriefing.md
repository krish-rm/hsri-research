# Risk Mitigation, Safety Protocols, and Debriefing Procedure

> **Protocol ID:** HSRI-IRB-2026-088  
> **Document Type:** Human Subjects Safety & Debriefing Protocol  
> **Applies to:** Standardized Behavioral Task Battery EXP-01 through EXP-09  
> **Version:** 1.0.0  

---

## 1. Overview and Purpose

Because the Human-AI Systemic Readiness Index (HSRI) assesses an individual's capacity to intercept errors, withstand default bias, and maintain autonomous agency, the study employs **benign incomplete disclosure** during the task trials. Participants are not informed in advance which specific AI recommendations contain intentional errors, hallucinatory citations, or flawed algorithmic code.

This document establishes:
1. Operational safeguards during data collection.
2. The standard post-experiment debriefing procedure.
3. Debriefing script text provided verbatim to every participant upon session completion.
4. Protocols for managing subject concerns or participant data revocation.

---

## 2. Participant Safety & Monitoring Protocols

1. **Self-Paced Progression:** While certain stress-testing tasks (such as EXP-05) incorporate standard timer constraints to examine choice overload, participants may pause between tasks.
2. **Immediate Abort Function:** An accessible "Exit Study" button remains visible throughout all task screens, allowing participants to withdraw instantly without justification.
3. **No Emotional or Triggering Stimuli:** All task scenarios are drawn strictly from professional, technical, and analytical domains (corporate contract law, clinical drug interaction verification, multi-threaded deadlock resolution, discounted cash flow corporate valuation). No personal, traumatic, or politically polarizing content is included.

---

## 3. Post-Experiment Debriefing Protocol

### 3.1 Timing of Debriefing
Debriefing occurs **immediately** following the completion of the final task (or upon early withdrawal if requested). The debriefing statement is rendered on a dedicated screen that cannot be dismissed for at least 15 seconds to ensure adequate review.

### 3.2 Key Educational Objectives of the Debriefing
1. **Explain the Incomplete Disclosure:** Explain transparently why the researchers could not inform the participant in advance about the presence and location of AI errors.
2. **Normalize Error Susceptibility:** Clearly reassure the participant that AI systems are designed to be persuasive, fluent, and authoritative; accepting erroneous AI outputs is a common human cognitive response (automation bias), not an indicator of personal intellectual inadequacy.
3. **Scientific Value:** Explain how their behavioral data helps develop systemic safeguards, interface friction designs, and educational training to protect human agency as AI systems advance.

---

## 4. Full Participant Debriefing Script (Verbatim)

```markdown
# Participant Debriefing Statement: Thank You for Your Participation

### What was this study really about?
Thank you for participating in the Human-AI Systemic Readiness Index (HSRI) research study!

During this session, you worked with an AI decision-support assistant across several professional problem-solving scenarios. At the start of the study, you were informed that you would evaluate complex problems with AI assistance. However, we did not inform you in advance that several AI recommendations contained **intentionally embedded errors**, such as fabricated legal citations, contradictory clinical recommendations, race conditions in software code, or skewed valuation formulas.

### Why was this information not shared beforehand?
In real-world environments, AI systems frequently generate responses that are fluent, well-formatted, and superficially persuasive, but factually flawed or logically unsound. 

If we had warned you in advance exactly when or where the AI would make an error, you would have adopted an artificially hyper-vigilant posture that does not match real-world collaboration. To measure genuine human-AI discernment, default resistance, and supervisory agency, it was scientifically essential that you experienced the AI recommendations naturally.

### Please Reassure Yourself:
Research consistently demonstrates that even domain experts frequently succumb to "automation complacency" and trust machine recommendations when they look clean and polished. Missing an embedded flaw is a standard cognitive tendency and **in no way reflects your intelligence, competence, or professional abilities**.

### How Your Data Helps Science:
Your responses will help researchers determine:
- How interface designs can introduce healthy "cognitive friction" to prevent automatic blind agreement.
- How humans can preserve independent critical reasoning as AI capabilities grow.
- What training and tools best empower people to remain effective decision-makers.

### Your Privacy and Data Rights:
All data collected today is cryptographically anonymized. No personally identifiable information has been collected. However, now that you know the full purpose of the study, if you do not want your anonymized data to be used in this research, you may email us at `research@hsri.org` with your anonymous session ID within 14 days, and your record will be permanently deleted.

If you have questions or comments, feel free to contact the research team at `research@hsri.org`.

Thank you again for contributing to human-AI safety research!
```

---

## 5. Post-Debriefing Data Revocation Procedure

If a participant expresses discomfort after reading the debriefing statement and wishes to strike their data:
1. The participant can check a box: `[ ] Withdraw my data from the study database`.
2. The server-side intake pipeline immediately tags the record with `FLAG_SUBJECT_REVOKED=TRUE`.
3. The raw session record is purged from the research telemetry corpus and excluded from psychometric dataset compilation.
