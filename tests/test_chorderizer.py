import os
import sys
from unittest.mock import MagicMock

# Mock colorama and mido before importing chorderizer
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.chorderizer import _generate_midi_filename_helper  # noqa: E402


def test_generate_midi_filename_helper_basic():
    tonic = "C"
    scale_info = {"name": "Major"}
    base_dir = "/tmp/midi"

    expected_filename = "prog_C_Major.mid"
    expected_path = os.path.join(base_dir, expected_filename)

    assert _generate_midi_filename_helper(tonic, scale_info, base_dir) == expected_path


def test_generate_midi_filename_helper_with_spaces_in_tonic():
    tonic = "C # "
    scale_info = {"name": "Major"}
    base_dir = "/tmp/midi"

    expected_filename = "prog_C_#__Major.mid"
    expected_path = os.path.join(base_dir, expected_filename)

    assert _generate_midi_filename_helper(tonic, scale_info, base_dir) == expected_path


def test_generate_midi_filename_helper_with_parentheses_and_spaces_in_scale():
    tonic = "D"
    scale_info = {"name": "Minor (Harmonic)"}
    base_dir = "/tmp/midi"

    expected_filename = "prog_D_Minor_Harmonic.mid"
    expected_path = os.path.join(base_dir, expected_filename)

    assert _generate_midi_filename_helper(tonic, scale_info, base_dir) == expected_path


def test_generate_midi_filename_helper_custom_prefix():
    tonic = "G"
    scale_info = {"name": "Dorian"}
    base_dir = "/tmp/midi"
    prefix = "custom_"

    expected_filename = "custom_G_Dorian.mid"
    expected_path = os.path.join(base_dir, expected_filename)

    assert (
        _generate_midi_filename_helper(tonic, scale_info, base_dir, prefix=prefix)
        == expected_path
    )


def test_generate_midi_filename_helper_empty_base_dir():
    tonic = "A"
    scale_info = {"name": "Phrygian"}
    base_dir = ""

    expected_filename = "prog_A_Phrygian.mid"
    expected_path = os.path.join(base_dir, expected_filename)

    assert _generate_midi_filename_helper(tonic, scale_info, base_dir) == expected_path
