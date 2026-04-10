import sys
from unittest.mock import MagicMock

# Mock colorama
sys.modules["colorama"] = MagicMock()
sys.modules["colorama.Fore"] = MagicMock()
sys.modules["colorama.Style"] = MagicMock()

# Mock mido (needed by generators which is imported by chorderizer)
sys.modules["mido"] = MagicMock()

import os  # noqa: E402
import unittest  # noqa: E402
from chorderizer.chorderizer import _sanitize_midi_path  # noqa: E402


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/user/midi_exports"
        self.default_path = os.path.join(self.base_dir, "default.mid")

    def test_sanitize_empty_input(self):
        result = _sanitize_midi_path("", self.default_path, self.base_dir)
        self.assertEqual(result, self.default_path)

    def test_sanitize_normal_filename(self):
        result = _sanitize_midi_path("my_song.mid", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "my_song.mid"))

    def test_sanitize_path_traversal(self):
        # On Linux, os.path.basename("../../../etc/passwd") is "passwd"
        result = _sanitize_midi_path(
            "../../../etc/passwd", self.default_path, self.base_dir
        )
        self.assertEqual(result, os.path.join(self.base_dir, "passwd"))

    def test_sanitize_absolute_path(self):
        # On Linux, os.path.basename("/tmp/evil.mid") is "evil.mid"
        result = _sanitize_midi_path("/tmp/evil.mid", self.default_path, self.base_dir)
        self.assertEqual(result, os.path.join(self.base_dir, "evil.mid"))

    def test_sanitize_nested_traversal(self):
        # os.path.basename("subdir/../other.mid") is "other.mid"
        result = _sanitize_midi_path(
            "subdir/../other.mid", self.default_path, self.base_dir
        )
        self.assertEqual(result, os.path.join(self.base_dir, "other.mid"))


if __name__ == "__main__":
    unittest.main()
