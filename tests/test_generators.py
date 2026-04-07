import sys
from unittest.mock import MagicMock

# Mock out mido, colorama to bypass missing dependency errors
sys.modules['mido'] = MagicMock()
sys.modules['colorama'] = MagicMock()

import pytest
from chorderizer.generators import TablatureGenerator

@pytest.fixture
def tablature_generator():
    mock_theory = MagicMock()
    return TablatureGenerator(theory=mock_theory)

def test_assign_fret_to_string_valid(tablature_generator):
    # chord_note_midi, open_string_midi, max_frets

    # Exact match with open string (fret 0)
    assert tablature_generator._assign_fret_to_string(40, 40, 22) == 0

    # Note above open string but within max frets
    assert tablature_generator._assign_fret_to_string(45, 40, 22) == 5

    # Note exactly max frets above open string
    assert tablature_generator._assign_fret_to_string(62, 40, 22) == 22

def test_assign_fret_to_string_invalid(tablature_generator):
    # Note lower than open string
    assert tablature_generator._assign_fret_to_string(39, 40, 22) is None

    # Note higher than max frets
    assert tablature_generator._assign_fret_to_string(63, 40, 22) is None
