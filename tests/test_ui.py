import sys
from unittest.mock import MagicMock

# Mock external dependencies
sys.modules["colorama"] = MagicMock()
sys.modules["colorama.Fore"] = MagicMock()
sys.modules["colorama.Style"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.ui import print_operation_cancelled  # noqa: E402


def test_print_operation_cancelled(capsys):
    print_operation_cancelled()
    captured = capsys.readouterr()
    assert "Operation cancelled by the user." in captured.out
