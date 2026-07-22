from applications.cli import cli


def test_cli_no_args() -> None:
    exit_code = cli([])
    assert exit_code == 0


def test_cli_with_task() -> None:
    exit_code = cli(["fix the bug"])
    assert exit_code == 0
