import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Mock colorama and mido before importing chorderizer
sys.modules["colorama"] = MagicMock()
sys.modules["mido"] = MagicMock()

from chorderizer.chorderizer import _generate_midi_filename_helper, process_single_run


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


def test_process_single_run_missing_scale_info():
    ui_mock = MagicMock()
    ui_mock.select_tonic_and_scale.return_value = (None, None)

    # process_single_run should return True when scale info is missing
    result = process_single_run(ui_mock, None, None, None, "/tmp")

    assert result is True
    ui_mock.select_tonic_and_scale.assert_called_once()


@patch("chorderizer.chorderizer.get_chord_settings")
def test_process_single_run_missing_chord_settings(mock_get_chord_settings):
    from chorderizer.chorderizer import process_single_run

    # Setup mocks
    ui_mock = MagicMock()
    ui_mock.select_tonic_and_scale.return_value = ("C", {"name": "Major"})

    chord_builder_mock = MagicMock()
    tab_builder_mock = MagicMock()
    midi_builder_mock = MagicMock()

    # When get_chord_settings returns None
    mock_get_chord_settings.return_value = None

    # Act
    result = process_single_run(
        ui_mock, chord_builder_mock, tab_builder_mock, midi_builder_mock, "/tmp/midi"
    )

    # Assert
    assert result is True
    mock_get_chord_settings.assert_called_once()
    chord_builder_mock.generate_scale_chords.assert_not_called()
