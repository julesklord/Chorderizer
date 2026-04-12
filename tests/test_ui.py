import sys
from unittest.mock import MagicMock
import pytest

# Mock colorama
mock_colorama = MagicMock()
mock_colorama.Fore = MagicMock()
mock_colorama.Fore.GREEN = ""
mock_colorama.Fore.YELLOW = ""
mock_colorama.Style = MagicMock()
mock_colorama.Style.RESET_ALL = ""
sys.modules["colorama"] = mock_colorama

# Mock mido
sys.modules["mido"] = MagicMock()

from chorderizer.ui import print_welcome_message  # noqa: E402


def test_print_welcome_message(capsys):
    print_welcome_message()
    captured = capsys.readouterr()

    # Check that standard output contains expected phrases
    assert "Welcome to the Advanced Chord Generator!" in captured.out
    assert "Modularized Version 1.2.0" in captured.out
