import sys
from unittest.mock import MagicMock, patch
import pytest

# Mock colorama
sys.modules["colorama"] = MagicMock()
sys.modules["colorama.Fore"] = MagicMock()
sys.modules["colorama.Style"] = MagicMock()

from chorderizer.ui import get_numbered_option  # noqa: E402

def test_get_numbered_option_valid():
    options = {"1": "Option 1", "2": "Option 2"}
    with patch("builtins.input", side_effect=["1"]):
        result = get_numbered_option("Choose:", options)
        assert result == "1"

def test_get_numbered_option_cancel():
    options = {"1": "Option 1", "2": "Option 2"}
    with patch("builtins.input", side_effect=["0"]):
        result = get_numbered_option("Choose:", options, allow_cancel=True, cancel_key="0")
        assert result is None

def test_get_numbered_option_no_cancel():
    options = {"1": "Option 1", "2": "Option 2"}
    with patch("builtins.input", side_effect=["0", "1"]):
        result = get_numbered_option("Choose:", options, allow_cancel=False, cancel_key="0")
        assert result == "1"

def test_get_numbered_option_invalid_then_valid():
    options = {"1": "Option 1"}
    with patch("builtins.input", side_effect=["99", "1"]):
        result = get_numbered_option("Choose:", options)
        assert result == "1"

def test_get_numbered_option_empty_then_valid():
    options = {"1": "Option 1"}
    with patch("builtins.input", side_effect=["", "1"]):
        result = get_numbered_option("Choose:", options)
        assert result == "1"

def test_get_numbered_option_keyboard_interrupt():
    options = {"1": "Option 1"}
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        result = get_numbered_option("Choose:", options)
        assert result is None

def test_get_numbered_option_eof_error():
    options = {"1": "Option 1"}
    with patch("builtins.input", side_effect=EOFError):
        result = get_numbered_option("Choose:", options)
        assert result is None

def test_get_numbered_option_dict_value():
    options = {"1": {"name": "Dict Option"}}
    with patch("builtins.input", side_effect=["1"]):
        result = get_numbered_option("Choose:", options)
        assert result == "1"
