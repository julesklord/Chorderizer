import sys
import pytest
from unittest.mock import MagicMock, patch

sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.ui import get_yes_no_answer


def test_get_yes_no_answer_true():
    with patch("builtins.input", return_value="y"):
        assert get_yes_no_answer("Test") is True
    with patch("builtins.input", return_value="yes"):
        assert get_yes_no_answer("Test") is True
    with patch("builtins.input", return_value="si"):
        assert get_yes_no_answer("Test") is True
    with patch("builtins.input", return_value="s"):
        assert get_yes_no_answer("Test") is True


def test_get_yes_no_answer_false():
    with patch("builtins.input", return_value="n"):
        assert get_yes_no_answer("Test") is False
    with patch("builtins.input", return_value="no"):
        assert get_yes_no_answer("Test") is False
    with patch("builtins.input", return_value=""):
        assert get_yes_no_answer("Test") is False


@patch("builtins.print")
def test_get_yes_no_answer_invalid_then_valid(mock_print):
    # input returns invalid "maybe", then valid "y"
    with patch("builtins.input", side_effect=["maybe", "y"]):
        assert get_yes_no_answer("Test") is True


@patch("chorderizer.ui.print_operation_cancelled")
def test_get_yes_no_answer_keyboard_interrupt(mock_print_cancelled):
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit) as e:
            get_yes_no_answer("Test")
        assert e.value.code == 0
    mock_print_cancelled.assert_called_once()


@patch("chorderizer.ui.print_operation_cancelled")
def test_get_yes_no_answer_eof_error(mock_print_cancelled):
    with patch("builtins.input", side_effect=EOFError):
        with pytest.raises(SystemExit) as e:
            get_yes_no_answer("Test")
        assert e.value.code == 0
    mock_print_cancelled.assert_called_once()
