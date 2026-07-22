from __future__ import annotations

from applications.container import Container


def main() -> None:
    """Bootstrap the application and wire dependencies.

    Creates the DI container, loads configuration, and prints
    a startup summary. The full pipeline is not yet implemented.
    """
    container = Container()
    config = container.application()

    print("opencode++ v0.1.0")
    print(f"  env:      {config.env}")
    print(f"  log_level: {config.log_level}")
    print(f"  debug:    {config.debug}")


if __name__ == "__main__":
    main()
