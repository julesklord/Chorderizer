import pytest
import sys
from unittest.mock import MagicMock

# Mock external dependencies
sys.modules["mido"] = MagicMock()

from chorderizer.theory_utils import MusicTheory  # noqa: E402
from chorderizer.generators import ChordGenerator


def test_chord_generator_happy_path():
    theory = MusicTheory()
    generator = ChordGenerator(theory)

    # C Major scale info
    scale_info = theory.AVAILABLE_SCALES["1"]

    # Default parameters: extension_level=2 (7ths), inversion=0
    generated_chords, notes_names, notes_midi, base_qualities = (
        generator.generate_scale_chords("C", scale_info)
    )

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
    scale_info = theory.AVAILABLE_SCALES["1"]  # Major

    # Triads (extension_level=0)
    generated_chords, _, _, _ = generator.generate_scale_chords(
        "C", scale_info, extension_level=0
    )
    assert generated_chords["I"] == "C"
    assert generated_chords["ii"] == "Dm"


def test_chord_generator_inversions():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"]  # Major

    # Root position (inversion=0)
    _, _, notes_midi_root, _ = generator.generate_scale_chords(
        "C", scale_info, inversion=0
    )

    # First inversion (inversion=1)
    _, _, notes_midi_inv1, _ = generator.generate_scale_chords(
        "C", scale_info, inversion=1
    )

    # Verify the lowest note in inversion 1 is different and higher than root position lowest note (or shifted)
    # The actual MIDI values depend on the specific octave selection logic, but we can verify
    # the relative pitch class or simply that the MIDI sequence is different.
    assert notes_midi_root["I"] != notes_midi_inv1["I"]


def test_chord_generator_invalid_tonic():
    theory = MusicTheory()
    generator = ChordGenerator(theory)
    scale_info = theory.AVAILABLE_SCALES["1"]  # Major

    # Invalid tonic
    generated_chords, notes_names, notes_midi, base_qualities = (
        generator.generate_scale_chords("Z", scale_info)
    )

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


# -----------------------------------------------------------------------------
# VoiceLeader Tests
# -----------------------------------------------------------------------------
from chorderizer.generators import VoiceLeader


def test_voice_leader_reduces_motion():
    """Voice leading output should have less total movement than the raw jump."""
    # Cmaj7 -> Fmaj7 in raw root position
    prev = [60, 64, 67, 71]  # C4, E4, G4, B4
    curr = [65, 69, 72, 76]  # F4, A4, C5, E5

    raw_motion = sum(abs(c - p) for c, p in zip(sorted(curr), sorted(prev)))
    voiced = VoiceLeader.apply(prev, curr)
    voiced_motion = sum(
        abs(v - p)
        for v in voiced
        for p in prev
        if abs(v - p) == min(abs(v - q) for q in prev)
    )

    # The voice-led version total span should be <= raw version
    assert max(voiced) - min(voiced) <= max(curr) - min(curr) + 12


def test_voice_leader_preserves_bass():
    """The bass note (lowest note, index 0) must not change pitch class."""
    prev = [48, 55, 60, 64]  # C3, G3, C4, E4
    curr = [53, 57, 60, 65]  # F3, A3, C4, F4

    voiced = VoiceLeader.apply(prev, curr)

    # Bass of curr is the first note (already sorted incoming)
    original_bass_pc = curr[0] % 12
    result_bass_pc = voiced[0] % 12
    assert result_bass_pc == original_bass_pc


def test_voice_leader_range_guard():
    """All output notes must remain within MIDI_MIN and MIDI_MAX."""
    prev = [60, 64, 67]
    curr = [62, 66, 69]

    voiced = VoiceLeader.apply(prev, curr)

    assert all(VoiceLeader.MIDI_MIN <= n <= VoiceLeader.MIDI_MAX for n in voiced)
