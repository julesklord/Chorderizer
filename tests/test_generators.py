import pytest
import sys
from unittest.mock import MagicMock

# Mock external dependencies
sys.modules['mido'] = MagicMock()

from chorderizer.theory_utils import MusicTheory
from chorderizer.generators import ChordGenerator

def test_chord_generator_happy_path():
    theory = MusicTheory()
    generator = ChordGenerator(theory)

    # C Major scale info
    scale_info = theory.AVAILABLE_SCALES["1"]

    # Default parameters: extension_level=2 (7ths), inversion=0
    generated_chords, notes_names, notes_midi, base_qualities = generator.generate_scale_chords("C", scale_info)

    assert "I" in generated_chords
    assert generated_chords["I"] == "Cmaj7"
    assert notes_names["I"] == ["C", "E", "G", "B"]
    assert base_qualities["I"] == "major"

    assert "ii" in generated_chords
    assert generated_chords["ii"] == "Dm7"
    assert base_qualities["ii"] == "minor"

def test_chord_generator_extension_levels():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"] # Major

    # Triads (extension_level=0)
    generated_chords, _, _, _ = generator.generate_scale_chords("C", scale_info, extension_level=0)
    assert generated_chords["I"] == "C"
    assert generated_chords["ii"] == "Dm"

def test_chord_generator_inversions():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"] # Major

    # Root position (inversion=0)
    _, _, notes_midi_root, _ = generator.generate_scale_chords("C", scale_info, inversion=0)

    # First inversion (inversion=1)
    _, _, notes_midi_inv1, _ = generator.generate_scale_chords("C", scale_info, inversion=1)

    # Verify the lowest note in inversion 1 is different and higher than root position lowest note (or shifted)
    # The actual MIDI values depend on the specific octave selection logic, but we can verify
    # the relative pitch class or simply that the MIDI sequence is different.
    assert notes_midi_root["I"] != notes_midi_inv1["I"]

def test_chord_generator_invalid_tonic():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"] # Major

    # Invalid tonic
    generated_chords, notes_names, notes_midi, base_qualities = generator.generate_scale_chords("Z", scale_info)

    assert generated_chords == {}
    assert notes_names == {}
    assert notes_midi == {}
    assert base_qualities == {}

def test_chord_generator_caching():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"]

    # Call first time
    res1 = generator.generate_scale_chords("C", scale_info)

    # Call second time
    res2 = generator.generate_scale_chords("C", scale_info)

    # Results should be equal in value
    assert res1 == res2

    # But they should NOT be the exact same object (because of copy.deepcopy)
    assert id(res1[0]) != id(res2[0])
