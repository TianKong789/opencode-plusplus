from __future__ import annotations

import argparse


def cli(argv: list[str] | None = None) -> int:
    """CLI entry point for opencode++.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].

    Returns:
        Exit code (0 for success).
    """
    parser = argparse.ArgumentParser(
        prog="opencode++",
        description="Continuously learning AI engineering platform",
    )
    parser.add_argument("task", nargs="?", help="Task description to execute")
    parser.add_argument("--workspace", default=".workspaces", help="Workspace root directory")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args(argv)

    if args.verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    if args.task:
        print(f"Received task: {args.task}")
        print("Pipeline not yet implemented.")
        return 0

    parser.print_help()
    return 0
