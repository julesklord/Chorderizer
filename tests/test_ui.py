"""
test_ui.py — Tests for the UI layer.
"""
from unittest.mock import patch
from chorderizer.ui import get_chord_settings, get_tablature_filter

# ─── get_chord_settings ───────────────────────────────────────────────────────

@patch('chorderizer.ui.print_formatted_text')
@patch('chorderizer.ui.clear')
@patch("chorderizer.ui._width", return_value=80)
def test_get_chord_settings_success(mock_width, mock_clear, mock_print):
    """Choosing extension=1 (Triads) and inversion=1 (Root) returns (0, 0)."""
    with patch("chorderizer.ui.prompt_menu", side_effect=["1", "1"]):
        ext, inv = get_chord_settings()
    assert ext == 0   # extension_map["1"] = 0
    assert inv == 0   # int("1") - 1 = 0


@patch('chorderizer.ui.print_formatted_text')
@patch('chorderizer.ui.clear')
@patch("chorderizer.ui._width", return_value=80)
def test_get_chord_settings_different_options(mock_width, mock_clear, mock_print):
    """Choosing extension=3 (Sevenths) and inversion=2 (1st) returns (2, 1)."""
    with patch("chorderizer.ui.prompt_menu", side_effect=["3", "2"]):
        ext, inv = get_chord_settings()
    assert ext == 2   # extension_map["3"] = 2
    assert inv == 1   # int("2") - 1 = 1


@patch('chorderizer.ui.print_formatted_text')
@patch('chorderizer.ui.clear')
@patch("chorderizer.ui._width", return_value=80)
def test_get_chord_settings_cancel_extension(mock_width, mock_clear, mock_print):
    """Cancelling the extension step returns (None, None)."""
    with patch("chorderizer.ui.prompt_menu", return_value=None):
        ext, inv = get_chord_settings()
    assert ext is None
    assert inv is None


@patch('chorderizer.ui.print_formatted_text')
@patch('chorderizer.ui.clear')
@patch("chorderizer.ui._width", return_value=80)
def test_get_chord_settings_cancel_inversion(mock_width, mock_clear, mock_print):
    """Cancelling the inversion step (after a valid extension) returns (None, None)."""
    with patch("chorderizer.ui.prompt_menu", side_effect=["1", None]):
        ext, inv = get_chord_settings()
    assert ext is None
    assert inv is None


# ─── get_tablature_filter ─────────────────────────────────────────────────────

@patch('chorderizer.ui.print_formatted_text')
def test_get_tablature_filter_success(mock_print):
    """A valid selection is returned as-is."""
    with patch("chorderizer.ui.prompt_menu", return_value="3"):
        result = get_tablature_filter()
    assert result == "3"


@patch('chorderizer.ui.print_formatted_text')
def test_get_tablature_filter_cancel(mock_print):
    """Cancelling defaults to '8' (no tablature)."""
    with patch("chorderizer.ui.prompt_menu", return_value=None):
        result = get_tablature_filter()
    assert result == "8"
