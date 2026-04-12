import sys
from unittest.mock import MagicMock, patch

# Mock external dependencies before importing local modules
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.ui import get_tablature_filter  # noqa: E402

@patch("chorderizer.ui.get_numbered_option")
def test_get_tablature_filter_valid_option(mock_get_numbered_option):
    """Test that when a user selects a valid option, it returns that option."""
    mock_get_numbered_option.return_value = "1"

    result = get_tablature_filter()

    assert result == "1"
    mock_get_numbered_option.assert_called_once()


@patch("chorderizer.ui.get_numbered_option")
def test_get_tablature_filter_cancelled(mock_get_numbered_option):
    """Test that when a user cancels the selection, it defaults to returning '8'."""
    mock_get_numbered_option.return_value = None

    result = get_tablature_filter()

    assert result == "8"
    mock_get_numbered_option.assert_called_once()
