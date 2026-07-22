# Runtime Red Flags

Immediately report any of the following.

## Execution

* Runtime performing planning
* Runtime performing reflection
* Runtime performing memory management
* Runtime making business decisions

## Coupling

* Runtime depending directly on OpenCode
* Runtime depending directly on an LLM
* Engine-specific logic leaking into orchestration

## Reliability

* Shared mutable state
* Resource leaks
* Missing cleanup
* Unhandled exceptions

## Workspace

* Shared workspaces
* Non-isolated execution
* Hardcoded paths

## Workflow

* Hidden execution paths
* Implicit state transitions
* Circular workflow execution

## Events

* Missing events
* Events published in incorrect order
* Missing execution metadata
