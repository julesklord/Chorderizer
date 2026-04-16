import sys
from unittest.mock import MagicMock

# Mock colorama
sys.modules["colorama"] = MagicMock()
sys.modules["colorama.Fore"] = MagicMock()
sys.modules["colorama.Style"] = MagicMock()

# Mock mido (needed by generators which is imported by chorderizer)
sys.modules["mido"] = MagicMock()

import os
import unittest

from chorderizer.chorderizer import _sanitize_midi_path


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "safe_midi_exports"
        self.default_path = os.path.join(self.base_dir, "default.mid")

    def test_sanitize_empty_input(self):
        result = _sanitize_midi_path("", self.default_path, self.base_dir)
        self.assertEqual(result, self.default_path)

    def test_sanitize_normal_filename(self):
        result = _sanitize_midi_path("my_song.mid", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "my_song.mid"))

    def test_sanitize_path_traversal(self):
        # basename("../../../etc/passwd") is "passwd"
        result = _sanitize_midi_path("../../../etc/passwd", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "passwd"))

    def test_sanitize_absolute_path(self):
        # basename("evil.mid") is "evil.mid"
        result = _sanitize_midi_path("evil.mid", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "evil.mid"))

    def test_sanitize_nested_traversal(self):
        # os.path.basename("subdir/../other.mid") is "other.mid"
        result = _sanitize_midi_path("subdir/../other.mid", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "other.mid"))


if __name__ == "__main__":
    unittest.main()
