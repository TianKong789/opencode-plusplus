---
name: "{{SKILL_NAME}} Checklist"
id: "{{SKILL_ID}}-checklist"
category: "{{CATEGORY}}"
level: "{{LEVEL}}"
version: "{{VERSION}}"
owner: "{{OWNER}}"
priority: "{{PRIORITY}}"
requires: []
tags:
  - "review"
  - "checklist"
  - "{{REVIEW_DOMAIN}}"
---

# {{SKILL_NAME}} Checklist

## How To Use This Checklist

Select the groups relevant to {{REVIEW_SUBJECT}}. Mark every item with one of
the statuses below. Add evidence for every `Partial`, `Fail`, and `Not Reviewed`
status. Use [TEMPLATE.md](TEMPLATE.md) to summarize group results.

## Status Values

| Status | Meaning | Score |
| --- | --- | ---: |
| Pass | Criterion is fully satisfied with supporting evidence | 1 |
| Partial | Criterion is partly satisfied or mitigation is incomplete | 0.5 |
| Fail | Criterion is not satisfied | 0 |
| Not Applicable | Criterion does not apply to the review subject | Excluded |
| Not Reviewed | Criterion applies but could not be evaluated | 0 |

## Scoring

Calculate the percentage from applicable items:

`score = earned points / applicable items * 100`

Round once at the end. Report `Not Reviewed` items separately so a score never
hides missing evidence. A triggered red flag overrides the numeric score.

| Score | Interpretation | Default Decision |
| --- | --- | --- |
| 90-100 | Strong evidence of readiness | Go |
| 75-89 | Acceptable with improvements | Go or Go With Conditions |
| 60-74 | Material gaps remain | Go With Conditions or No-Go |
| Below 60 | Insufficient readiness | No-Go |

## Intent And Scope

- [ ] The intended outcome and acceptance criteria are explicit.
- [ ] The reviewed artifacts and boundaries are identified.
- [ ] In-scope and out-of-scope concerns are distinguished.
- [ ] Assumptions, dependencies, and constraints are documented.
- [ ] The implementation or decision matches its stated intent.

## Correctness And Completeness

- [ ] Required behavior or reasoning is correct.
- [ ] Important success, failure, and edge cases are addressed.
- [ ] State transitions and side effects are explicit.
- [ ] Error handling is proportionate to realistic failure modes.
- [ ] No required outcome is missing or contradicted.

## Evidence Quality

- [ ] Claims point to specific artifacts, observations, or measurements.
- [ ] Evidence is reproducible or independently verifiable.
- [ ] Facts, assumptions, and opinions are clearly separated.
- [ ] Missing evidence is recorded rather than inferred.
- [ ] Conclusions are proportionate to the available evidence.

## Architecture And Boundaries

- [ ] Responsibilities and module boundaries remain clear.
- [ ] Coupling is controlled and cohesion is preserved.
- [ ] Dependency direction follows the intended design.
- [ ] Interfaces are focused and implementation-independent.
- [ ] No circular dependency, abstraction leak, or duplicate source of truth is introduced.

## Runtime And Operations

- [ ] Execution paths and state transitions are deterministic where required.
- [ ] Isolation, cleanup, and resource ownership are explicit.
- [ ] Failures are observable and recoverable at the appropriate boundary.
- [ ] Events, logs, and operational metadata are sufficient and correctly ordered.
- [ ] Hidden mutable state and environment-specific assumptions are avoided.

## Benchmarks And Performance

- [ ] Metrics measure the intended quality or behavior.
- [ ] Baselines, comparison methods, and thresholds are defined.
- [ ] Results are repeatable and statistically meaningful where applicable.
- [ ] Coverage includes regressions, failures, and representative edge cases.
- [ ] Leakage, reward hacking, overfitting, and misleading aggregation are controlled.

## Refactoring Safety

- [ ] Existing behavior and public contracts are preserved or intentionally changed.
- [ ] Behavior preservation is demonstrated by tests or equivalent evidence.
- [ ] The change reduces complexity, duplication, coupling, or maintenance cost.
- [ ] New abstractions are justified by concrete reuse or separation needs.
- [ ] Dead code and obsolete paths are removed without weakening validation.

## Implementation Quality

- [ ] Naming and control flow communicate intent clearly.
- [ ] Functions, classes, and modules have focused responsibilities.
- [ ] Types, invariants, and boundary validation are explicit.
- [ ] Documentation and comments explain non-obvious contracts or trade-offs.
- [ ] Logging and errors provide actionable context without hiding failures.

## Testing And Validation

- [ ] Tests cover changed behavior, public contracts, and realistic edge cases.
- [ ] Relevant tests, checks, or builds have been executed successfully.
- [ ] Regressions are distinguished from pre-existing failures.
- [ ] Manual validation covers user-visible or operational behavior where needed.
- [ ] Verification evidence includes commands, outcomes, or result artifacts.

## Documentation And Traceability

- [ ] Decisions and significant trade-offs are recorded.
- [ ] User and developer documentation matches the reviewed behavior.
- [ ] Risks, limitations, and follow-up work are explicit.
- [ ] Terminology is consistent across artifacts.
- [ ] Findings can be traced to evidence and assigned actions.

## Readiness

- [ ] No unresolved Critical or unmitigated High finding remains.
- [ ] Required owners, actions, and deadlines are identified.
- [ ] Rollback or recovery is defined when consequences warrant it.
- [ ] Dependencies and external approvals are satisfied.
- [ ] The proposed decision is consistent with the findings and red flags.

## Domain Adaptation

- **ADR review:** Emphasize context, alternatives, trade-offs, consequences, and decision traceability.
- **Milestone review:** Emphasize completion evidence, cross-area readiness, documentation, and technical debt.
- **Architecture guardian review:** Emphasize boundaries, dependency direction, drift, interfaces, and evolvability.
- **Runtime review:** Emphasize deterministic execution, isolation, cleanup, failure recovery, events, and observability.
- **Benchmark review:** Emphasize validity, reproducibility, coverage, fairness, overfitting, and regression detection.
- **Refactoring review:** Emphasize behavior preservation, simplification, duplication, coupling, and maintenance cost.
- **Implementation review:** Emphasize correctness, readability, types, errors, logging, documentation, and tests.

## References

- [SKILL.md](SKILL.md): Review behavior and decision rules
- [TEMPLATE.md](TEMPLATE.md): Checklist summary and final report
- [RED_FLAGS.md](RED_FLAGS.md): Conditions that override scoring
