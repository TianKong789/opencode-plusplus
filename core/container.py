"""Core layer composition root — removed per AG-5 architectural review.

The DI container lives in ``applications.container`` because the core
layer must remain inward-facing (models, ports, pure policy only).
"""

raise ImportError(
    "core.container has been moved to applications.container. "
    "Import from there instead."
)
