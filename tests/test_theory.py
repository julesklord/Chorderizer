import pytest
from chorderizer.theory_utils import MusicTheoryUtils


def test_get_note_index():
    assert MusicTheoryUtils.get_note_index("C") == 0
    assert MusicTheoryUtils.get_note_index("C#") == 1
    assert MusicTheoryUtils.get_note_index("Db") == 1
    assert MusicTheoryUtils.get_note_index("G") == 7
    assert MusicTheoryUtils.get_note_index("B") == 11
    with pytest.raises(ValueError):
        MusicTheoryUtils.get_note_index("Z")


def test_get_note_name():
    assert MusicTheoryUtils.get_note_name(0) == "C"
    assert MusicTheoryUtils.get_note_name(1) == "C#"
    assert MusicTheoryUtils.get_note_name(1, use_flats=True) == "Db"
    assert MusicTheoryUtils.get_note_name(13) == "C#"


def test_should_use_flats():
    assert MusicTheoryUtils.should_use_flats("F") is True
    assert MusicTheoryUtils.should_use_flats("Bb") is True
    assert MusicTheoryUtils.should_use_flats("C") is False
    assert MusicTheoryUtils.should_use_flats("G") is False
    assert MusicTheoryUtils.should_use_flats("Eb Major") is True


def test_split_chord_name():
    assert MusicTheoryUtils.split_chord_name("Cmaj7") == ("C", "maj7")
    assert MusicTheoryUtils.split_chord_name("F#m7") == ("F#", "m7")
    assert MusicTheoryUtils.split_chord_name("Bb7") == ("Bb", "7")
    assert MusicTheoryUtils.split_chord_name("G") == ("G", "")


def test_transpose_chords():
    original_chords = {"I": "Cmaj7", "ii": "Dm7", "V": "G7"}
    # Transpose from C to D
    transposed = MusicTheoryUtils.transpose_chords(original_chords, "C", "D")
    assert transposed == {"I": "Dmaj7", "ii": "Em7", "V": "A7"}

    # Transpose from C to F (should use flats)
    transposed_f = MusicTheoryUtils.transpose_chords(original_chords, "C", "F")
    assert transposed_f == {"I": "Fmaj7", "ii": "Gm7", "V": "C7"}

    # Transpose from G to Bb (should use flats)
    original_g = {"I": "Gmaj7", "IV": "Cmaj7", "V": "D7"}
    transposed_bb = MusicTheoryUtils.transpose_chords(original_g, "G", "Bb")
    assert transposed_bb == {"I": "Bbmaj7", "IV": "Ebmaj7", "V": "F7"}
