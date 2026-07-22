# Architectural Red Flags

Immediately flag any of the following.

## Dependency Violations

* Concrete classes depending on concrete classes.
* Circular dependencies.
* Cross-layer imports.

## Interface Growth

* More than one responsibility.
* Large interfaces.
* Optional parameters accumulating.

## Domain Drift

* Duplicate domain concepts.
* Conflicting terminology.
* Multiple sources of truth.

## Technical Debt

* Temporary code becoming permanent.
* TODOs without milestones.
* Feature-specific hacks.

## Experience Violations

* Engineering work not producing Experiences.
* Experiences that cannot be benchmarked.
* Experiences that cannot become reusable assets.

## Evolution Violations

* Hard-coded prompts.
* Hard-coded workflows.
* Hard-coded policies.
* Non-versioned assets.

## Complexity

* Unnecessary abstractions.
* Premature optimization.
* Deep inheritance hierarchies.
* Hidden dependencies.
* Large modules.
