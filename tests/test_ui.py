import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock colorama before importing ui
sys.modules["colorama"] = MagicMock()

from chorderizer.ui import get_tablature_filter


class TestUI(unittest.TestCase):
    @patch("chorderizer.ui.get_numbered_option")
    def test_get_tablature_filter_valid_choice(self, mock_get_option):
        """Test when the user makes a valid selection for tablature filter."""
        mock_get_option.return_value = "3"
        result = get_tablature_filter()

        self.assertEqual(result, "3")
        mock_get_option.assert_called_once()
        args, kwargs = mock_get_option.call_args
        self.assertEqual(args[0], "--- Filter for Displaying Tablatures ---")
        self.assertTrue(kwargs.get("allow_cancel"))

    @patch("chorderizer.ui.get_numbered_option")
    def test_get_tablature_filter_cancel(self, mock_get_option):
        """Test when the user cancels the tablature filter selection (returns None)."""
        mock_get_option.return_value = None
        result = get_tablature_filter()

        # It should default to "8" (No tablatures) when cancelled
        self.assertEqual(result, "8")
        mock_get_option.assert_called_once()
