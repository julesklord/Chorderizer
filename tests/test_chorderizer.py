"""
test_chorderizer.py — Tests for the main orchestration module.
"""

import os
import re
import sys
from unittest.mock import MagicMock

# Mock external dependencies before importing chorderizer
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.chorderizer import (  # noqa: E402
    _generate_midi_filename_helper,
    process_single_run,
)


def _verify_midi_filename(path, tonic, scale_name, prefix="prog_"):
    """Verify MIDI filename contains expected components."""
    filename = os.path.basename(path)
    # Check prefix
    assert filename.startswith(prefix), f"Expected prefix '{prefix}', got '{filename}'"
    # Check tonic
    assert tonic.replace(" ", "_") in filename, f"Expected tonic in '{filename}'"
    # Check scale (without special chars)
    safe_scale = scale_name.replace(" ", "_").replace("(", "").replace(")", "")
    assert safe_scale in filename, f"Expected scale in '{filename}'"
    # Check timestamp format (YYYYMMDD_HHMMSS)
    assert re.search(r"_\d{8}_\d{6}\.mid$", filename), f"Expected timestamp in '{filename}'"
    return True


def test_generate_midi_filename_helper_basic():
    tonic = "C"
    scale_info = {"name": "Major"}
    base_dir = "temp_midi_dir"

    result = _generate_midi_filename_helper(tonic, scale_info, base_dir)
    assert _verify_midi_filename(result, tonic, scale_info["name"])


def test_generate_midi_filename_helper_with_spaces_in_tonic():
    tonic = "C # "
    scale_info = {"name": "Major"}
    base_dir = "temp_midi_dir"

    result = _generate_midi_filename_helper(tonic, scale_info, base_dir)
    assert _verify_midi_filename(result, tonic, scale_info["name"])


def test_generate_midi_filename_helper_with_parentheses_and_spaces_in_scale():
    tonic = "D"
    scale_info = {"name": "Minor (Harmonic)"}
    base_dir = "temp_midi_dir"

    result = _generate_midi_filename_helper(tonic, scale_info, base_dir)
    assert _verify_midi_filename(result, tonic, scale_info["name"])


def test_generate_midi_filename_helper_custom_prefix():
    tonic = "G"
    scale_info = {"name": "Dorian"}
    base_dir = "temp_midi_dir"
    prefix = "custom_"

    result = _generate_midi_filename_helper(tonic, scale_info, base_dir, prefix=prefix)
    assert _verify_midi_filename(result, tonic, scale_info["name"], prefix=prefix)


def test_generate_midi_filename_helper_empty_base_dir():
    tonic = "A"
    scale_info = {"name": "Phrygian"}
    base_dir = ""

    result = _generate_midi_filename_helper(tonic, scale_info, base_dir)
    assert _verify_midi_filename(result, tonic, scale_info["name"])


def test_process_single_run_missing_scale_info():
    """process_single_run returns True (loop) when scale selection is cancelled."""
    ui_mock = MagicMock()
    # select_scale_config is the new method; select_tonic_and_scale is the compat alias
    ui_mock.select_scale_config.return_value = (None, None)

    result = process_single_run(ui_mock, None, None, None, "temp_midi")

    assert result is True
    ui_mock.select_scale_config.assert_called_once()


def test_process_single_run_missing_chord_settings():
    """process_single_run returns True (loop) when chord config is cancelled."""
    ui_mock = MagicMock()
    ui_mock.select_scale_config.return_value = (
        "C",
        {"name": "Major", "degrees": {}, "tonic_suffix": ""},
    )
    ui_mock.select_chord_config.return_value = (None, None)

    chord_builder_mock = MagicMock()

    result = process_single_run(
        ui_mock, chord_builder_mock, MagicMock(), MagicMock(), "temp_midi_dir"
    )

    assert result is True
    ui_mock.select_chord_config.assert_called_once()
    chord_builder_mock.generate_scale_chords.assert_not_called()
