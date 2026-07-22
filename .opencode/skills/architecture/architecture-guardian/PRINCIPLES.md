# Architectural Principles

These principles are non-negotiable.

## Principle 1

Everything is an Experience.

Every engineering activity should produce an Experience.

---

## Principle 2

Everything Evolvable is Versioned.

Skills.

Prompts.

Workflows.

Benchmarks.

Agents.

Policies.

---

## Principle 3

Everything Reusable is an Asset.

Do not duplicate knowledge.

Extract reusable assets.

---

## Principle 4

Interfaces before Implementations.

Implementations may change.

Interfaces should remain stable.

---

## Principle 5

Depend on Abstractions.

Never depend directly on concrete implementations.

---

## Principle 6

Benchmark before Promotion.

Never promote a change because it "looks better."

Promote only after objective evaluation.

---

## Principle 7

Prefer Simplicity.

Choose the simplest design that satisfies current requirements.

---

## Principle 8

Protect Long-Term Maintainability.

Never trade long-term architecture for short-term convenience.

---

## Principle 9

Architecture is the Product.

Code is only one implementation of the architecture.

---

## Principle 10
Architecture Leads Implementation

Architectural documents (ARCHITECTURE.md, docs/runtime.md, ADRs) define the intended system design. When implementation and architecture diverge, the default assumption is that the implementation should be brought back into alignment unless there is an explicit architectural decision to change the design.