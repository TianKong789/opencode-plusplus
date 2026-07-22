---
name: "{{SKILL_NAME}} Red Flags"
id: "{{SKILL_ID}}-red-flags"
category: "{{CATEGORY}}"
level: "{{LEVEL}}"
version: "{{VERSION}}"
owner: "{{OWNER}}"
priority: "{{PRIORITY}}"
requires: []
tags:
  - "review"
  - "red-flags"
  - "{{REVIEW_DOMAIN}}"
---

# {{SKILL_NAME}} Red Flags

## Purpose

Red flags identify conditions that require immediate attention and override an
otherwise acceptable checklist score. They are not automatic accusations; each
trigger must be supported by specific evidence.

## Escalation Rule

When a red flag is observed:

1. Stop the normal approval flow for the affected area.
2. Capture the artifact location, observation, impact, and uncertainty.
3. Identify the minimum mitigation and the owner responsible for it.
4. Record the trigger in the `Red-Flag Escalations` report section.
5. Issue `No-Go` unless the risk is bounded by an explicit, verified mitigation;
   only then may `Go With Conditions` be considered.

Do not lower severity or omit a red flag to preserve a target score or deadline.

## Missing Required Evidence

- Required artifacts, tests, measurements, or approvals are absent.
- A material claim cannot be traced to a source or reproduced.
- Applicable areas are marked `Not Applicable` to avoid review.
- Verification is asserted without commands, outputs, or equivalent evidence.

## Contradictory Or Unverifiable Claims

- The implementation, report, and stated contract disagree.
- Evidence is selectively presented or known counter-evidence is omitted.
- Assumptions are presented as verified facts.
- Conclusions exceed what the available data can support.

## Unbounded Scope Expansion

- The change introduces unrelated responsibilities or behavior.
- Review boundaries are changed without disclosure or approval.
- A local change requires broad redesign without a documented decision.
- Subjective style preferences are used to justify high-risk churn.

## Critical Correctness, Security, Or Data Risk

- A known path can corrupt, lose, expose, or irreversibly alter data.
- A correctness defect invalidates the primary outcome.
- Authorization, trust boundaries, or sensitive inputs are handled unsafely.
- A destructive operation lacks proportionate safeguards or recovery.

## Architecture Boundary Violations

- Dependencies cross prohibited boundaries or form a cycle.
- A component acquires unrelated responsibilities.
- Implementation details leak through a public interface.
- Multiple conflicting sources of truth are introduced.
- Hidden dependencies prevent independent replacement or testing.

## Runtime Safety And Reliability

- Shared mutable state creates nondeterministic behavior.
- Resource ownership, cleanup, or isolation is missing.
- Failures are swallowed, unrecoverable, or invisible to operators.
- Execution paths or state transitions are implicit or incorrectly ordered.
- Required operational events or metadata are absent or misleading.

## Invalid Or Misleading Measurement

- A metric does not measure the stated objective.
- Benchmark leakage, reward hacking, cherry-picking, or overfitting is present.
- Results cannot be reproduced or compared to a relevant baseline.
- Aggregation hides regressions, failures, or affected populations.
- A claimed improvement is within noise or lacks sufficient evidence.

## Unsafe Refactoring

- Behavior or a public contract changes without explicit intent.
- Behavior preservation is assumed without tests or equivalent proof.
- Tests are removed or weakened to make the change pass.
- Complexity is moved rather than reduced.
- Compatibility paths are added without a real external contract.

## Missing Implementation Validation

- Changed behavior has no relevant automated or manual validation.
- Required tests, type checks, lint checks, or builds were not run.
- Failing checks are dismissed without demonstrating they are pre-existing.
- Error paths, boundary cases, or user-visible behavior remain unverified.

## Release Or Adoption Blockers

- An unresolved Critical or unmitigated High finding remains.
- Required owner, deadline, rollback, or mitigation is missing.
- Documentation or operational readiness contradicts actual behavior.
- A required dependency, approval, or migration is incomplete.

## Required Escalation Format

For each red flag, report:

- **Title:** A concise description of the trigger.
- **Location:** The affected artifact or observation point.
- **Evidence:** What proves or strongly supports the trigger.
- **Impact:** The credible consequence if unresolved.
- **Required mitigation:** The minimum action needed to bound the risk.
- **Decision effect:** `No-Go` or justified `Go With Conditions`.

## References

- [SKILL.md](SKILL.md): Escalation workflow and decision rules
- [CHECKLIST.md](CHECKLIST.md): Criteria affected by each red flag
- [TEMPLATE.md](TEMPLATE.md): Required escalation report format
