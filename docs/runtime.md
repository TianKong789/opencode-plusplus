# Runtime Specification

## Responsibilities

The Runtime is responsible for executing workflows.

It does not perform planning.

It does not perform reflection.

It does not perform memory management.

## Components

- WorkflowRunner
- ExecutionEngine
- WorkspaceManager
- GitManager
- EventBus

## Execution Flow

Task
  ↓
Workflow
  ↓
WorkflowRunner
  ↓
ExecutionEngine
  ↓
Workspace
  ↓
ExecutionResult