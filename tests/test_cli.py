# pylint: disable=too-few-public-methods,missing-function-docstring

from contextlib import contextmanager
from typing import List, Optional

import pytest
from click.testing import CliRunner, Result

import blacktape
from blacktape.cli import main_command


@contextmanager
def does_not_raise():
    yield


class Expected:
    """
    Result object type for parametrized tests. Expand as necessary...
    """

    def __init__(self, status: int, tokens: List[str], **kwargs):
        self.status = status
        self.tokens = tokens

        for key, value in kwargs.items():
            setattr(self, key, value)


def run_command(
    cmd: Optional[str],
    options: Optional[List[str]],
    args: Optional[str],
    runner: CliRunner,
    expected: Optional[Expected],
) -> Result:
    """
    Block of code to run a CLI command as part of a test
    """

    command = [cmd] if cmd else []
    command.extend(options or [])

    if args:
        command.append(args)

    result = runner.invoke(main_command, command)

    if expected:
        assert result.exit_code == expected.status

        for token in expected.tokens:
            assert token in result.output

    return result


@pytest.mark.parametrize(
    "cmd, options, args, expected",
    [
        # (None, None, None, Expected(status=0, tokens=["Usage", "Options", "Commands"])),
        (None, None, None, Expected(status=0, tokens=["Usage", "Options"])),
        (
            None,
            ["--version"],
            None,
            Expected(status=0, tokens=[blacktape.__version__]),
        ),
    ],
)
def test_blacktape(cli_runner, cmd, options, args, expected):
    run_command(cmd, options, args, cli_runner, expected)
