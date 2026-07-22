# Runtime Review Checklist

## Workflow

* [ ] Workflow execution is deterministic
* [ ] Workflow steps are isolated
* [ ] Step ordering is correct
* [ ] Retry behavior is defined

## Execution Engine

* [ ] Depends only on interfaces
* [ ] Multiple engines are supported
* [ ] No engine-specific logic leaks upward

## Workspace

* [ ] Workspaces are isolated
* [ ] Cleanup is reliable
* [ ] Temporary files are managed

## Git

* [ ] Repository lifecycle is correct
* [ ] Commits are atomic
* [ ] Errors are handled gracefully

## Events

* [ ] Runtime events are published
* [ ] Events contain sufficient context
* [ ] Event ordering is consistent

## Reliability

* [ ] Failures are recoverable
* [ ] Resources are released
* [ ] Logging is sufficient

## Testability

* [ ] Components are mockable
* [ ] Integration tests exist
* [ ] End-to-end workflow is tested

## Architecture

* [ ] Runtime contains no planning logic
* [ ] Runtime contains no memory logic
* [ ] Runtime contains no LLM logic
