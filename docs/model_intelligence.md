Describe the architecture of the Model Intelligence subsystem.

The subsystem consists of:

Model Registry
Capability Assessor
Capability Profile
Task Classifier
Model Router

Responsibilities

Model Registry
    stores every known model

Capability Assessor
    executes benchmark suites and produces capability scores

Capability Profile
    stores strengths, weaknesses, performance, latency,
    cost, context size, supported languages, supported domains

Task Classifier
    determines capabilities required for a task

Model Router
    selects the best model based on capability profile
    and routing policy

The subsystem must follow Clean Architecture.

Everything depends only on core interfaces.

No implementation details in the document.

Include diagrams.