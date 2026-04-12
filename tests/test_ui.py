import sys
from unittest.mock import MagicMock, patch

# Mock external dependencies
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.ui import get_chord_settings, get_tablature_filter


def test_get_chord_settings_success():
    with patch("chorderizer.ui.get_numbered_option", side_effect=["1", "1"]):
        ext, inv = get_chord_settings()
        assert ext == 0
        assert inv == 0


def test_get_chord_settings_different_options():
    with patch("chorderizer.ui.get_numbered_option", side_effect=["3", "2"]):
        ext, inv = get_chord_settings()
        assert ext == 2  # extension_map["3"] = 2
        assert inv == 1  # int("2") - 1 = 1


def test_get_chord_settings_cancel_extension():
    with patch("chorderizer.ui.get_numbered_option", return_value=None):
        ext, inv = get_chord_settings()
        assert ext is None
        assert inv is None


def test_get_chord_settings_cancel_inversion():
    with patch("chorderizer.ui.get_numbered_option", side_effect=["1", None]):
        ext, inv = get_chord_settings()
        assert ext is None
        assert inv is None


def test_get_tablature_filter_success():
    with patch("chorderizer.ui.get_numbered_option", return_value="3"):
        result = get_tablature_filter()
        assert result == "3"


def test_get_tablature_filter_cancel():
    with patch("chorderizer.ui.get_numbered_option", return_value=None):
        result = get_tablature_filter()
        assert result == "8"
