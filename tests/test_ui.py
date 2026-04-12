import sys
import pytest
from unittest.mock import MagicMock

# Mock external dependencies
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

# Setup colorama mock values to be strings instead of Mock objects to prevent formatting issues
colorama_mock = sys.modules["colorama"]
colorama_mock.Fore.RED = "RED_"
colorama_mock.Style.RESET_ALL = "_RESET"

from chorderizer.ui import print_operation_cancelled  # noqa: E402


def test_print_operation_cancelled(capsys):
    print_operation_cancelled()
    captured = capsys.readouterr()
    assert "Operation cancelled by the user." in captured.out
