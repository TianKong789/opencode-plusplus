---
name: "{{SKILL_NAME}} Report Template"
id: "{{SKILL_ID}}-report-template"
category: "{{CATEGORY}}"
level: "{{LEVEL}}"
version: "{{VERSION}}"
owner: "{{OWNER}}"
priority: "{{PRIORITY}}"
requires: []
tags:
  - "review"
  - "report"
  - "{{REVIEW_DOMAIN}}"
---

# {{SKILL_NAME}} Review: {{REVIEW_SUBJECT}}

## Review Metadata

| Field | Value |
| --- | --- |
| Reviewer | {{REVIEWER}} |
| Date | {{DATE}} |
| Review domain | {{REVIEW_DOMAIN}} |
| Subject | {{REVIEW_SUBJECT}} |
| Scope | {{REVIEW_SCOPE}} |
| Input artifacts | {{INPUT_ARTIFACTS}} |

## Executive Summary

{{Summarize the outcome, strongest evidence, primary risk, and decision in two to five sentences.}}

## Overall Score

| Measure | Result |
| --- | --- |
| Checklist score | {{SCORE}} / 100 |
| Score band | {{SCORE_BAND}} |
| Applicable items | {{APPLICABLE_COUNT}} |
| Not reviewed items | {{NOT_REVIEWED_COUNT}} |
| Triggered red flags | {{RED_FLAG_COUNT}} |

**Score rationale:** {{SCORE_RATIONALE}}

## Checklist Status

| Group | Status | Score | Evidence | Notes |
| --- | --- | ---: | --- | --- |
| {{CHECKLIST_GROUP}} | {{STATUS}} | {{GROUP_SCORE}} | {{EVIDENCE}} | {{NOTES}} |

See [CHECKLIST.md](CHECKLIST.md) for status and scoring definitions.

## Strengths

- **{{STRENGTH}}:** {{EVIDENCE_AND_IMPACT}}

## Findings

List findings from highest to lowest severity. Remove empty severity sections.

### Critical

#### {{FINDING_TITLE}}

- **Location:** {{ARTIFACT_LOCATION}}
- **Observation:** {{OBSERVATION}}
- **Impact:** {{IMPACT}}
- **Recommendation:** {{RECOMMENDATION}}
- **Owner / next step:** {{OWNER_OR_NEXT_STEP}}

### High

#### {{FINDING_TITLE}}

- **Location:** {{ARTIFACT_LOCATION}}
- **Observation:** {{OBSERVATION}}
- **Impact:** {{IMPACT}}
- **Recommendation:** {{RECOMMENDATION}}
- **Owner / next step:** {{OWNER_OR_NEXT_STEP}}

### Medium

#### {{FINDING_TITLE}}

- **Location:** {{ARTIFACT_LOCATION}}
- **Observation:** {{OBSERVATION}}
- **Impact:** {{IMPACT}}
- **Recommendation:** {{RECOMMENDATION}}
- **Owner / next step:** {{OWNER_OR_NEXT_STEP}}

### Low

#### {{FINDING_TITLE}}

- **Location:** {{ARTIFACT_LOCATION}}
- **Observation:** {{OBSERVATION}}
- **Impact:** {{IMPACT}}
- **Recommendation:** {{RECOMMENDATION}}
- **Owner / next step:** {{OWNER_OR_NEXT_STEP}}

## Risks

| Risk | Likelihood | Impact | Evidence | Mitigation |
| --- | --- | --- | --- | --- |
| {{RISK}} | {{LIKELIHOOD}} | {{IMPACT}} | {{EVIDENCE}} | {{MITIGATION}} |

## Prioritized Recommendations

Order actions by risk reduction and dependency, not by ease.

### Required Before Acceptance

1. {{REQUIRED_ACTION}}

### Required After Acceptance

1. {{CONDITIONAL_ACTION}}

### Optional Improvements

1. {{OPTIONAL_ACTION}}

## Assumptions And Gaps

- **Assumption:** {{ASSUMPTION}}
- **Missing evidence:** {{MISSING_EVIDENCE}}
- **Not reviewed:** {{NOT_REVIEWED_AREA}}

## Red-Flag Escalations

State `None` or record each triggered item from [RED_FLAGS.md](RED_FLAGS.md).

### {{RED_FLAG_TITLE}}

- **Evidence:** {{EVIDENCE}}
- **Impact:** {{IMPACT}}
- **Required mitigation:** {{REQUIRED_MITIGATION}}
- **Decision effect:** {{DECISION_EFFECT}}

## Go / No-Go Decision

**Decision:** {{GO | GO WITH CONDITIONS | NO-GO}}

**Rationale:** {{DECISION_RATIONALE}}

**Conditions:** {{CONDITIONS_OR_NONE}}

## References

- [SKILL.md](SKILL.md): Review process, evidence, severity, and decision rules
- [CHECKLIST.md](CHECKLIST.md): Criteria, statuses, and scoring
- [RED_FLAGS.md](RED_FLAGS.md): Escalation triggers
