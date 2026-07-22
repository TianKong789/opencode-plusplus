# Runtime Principles

## Principle 1

The Runtime executes workflows.

It does not make decisions.

---

## Principle 2

Execution engines are plugins.

The Runtime must never depend on a specific engine.

---

## Principle 3

Every execution is isolated.

Workspaces must not interfere with one another.

---

## Principle 4

The Runtime must be deterministic.

The same workflow under the same conditions should produce the same execution path.

---

## Principle 5

Every execution must be observable.

Execution state and events should be visible.

---

## Principle 6

Failures are expected.

Every failure should be recoverable or clearly reported.

---

## Principle 7

The Runtime should remain lightweight.

Business logic belongs elsewhere.

---

## Principle 8

Everything executed should produce an Experience.
