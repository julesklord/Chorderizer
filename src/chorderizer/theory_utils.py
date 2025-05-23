from typing import List, Dict, Tuple, Optional, Any, Union, Mapping

# -----------------------------------------------------------------------------
# Class MusicTheoryUtils: Utility functions for music theory
# -----------------------------------------------------------------------------
class MusicTheoryUtils:
    @staticmethod
    def get_note_name(note_index: int, use_flats: bool = False) -> str:
        if use_flats:
            flat_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
            return flat_names[note_index % 12]
        return MusicTheory.CHROMATIC_NOTES[note_index % 12]

    @staticmethod
    def get_note_index(note_name: str) -> int:
        base_note = note_name.upper()
        flat_to_sharp_equivalents = {"DB": "C#", "EB": "D#", "FB": "E", "GB": "F#", "AB": "G#", "BB": "A#",
                                     "CB": "B"}
        for flat, sharp in flat_to_sharp_equivalents.items():
            if base_note.startswith(flat):
                base_note = sharp + base_note[len(flat):]
                break
        root_note_str = ""
        for char_note in base_note:
            if char_note.isalpha() or char_note == '#':
                root_note_str += char_note
            else:
                break
        try:
            return MusicTheory.CHROMATIC_NOTES.index(root_note_str)
        except ValueError:
            raise ValueError(f"Base note '{root_note_str}' from '{note_name}' not recognized.")


# -----------------------------------------------------------------------------
# Class MusicTheory: Constants and basic music theory definitions
# -----------------------------------------------------------------------------
class MusicTheory:
    CHROMATIC_NOTES: List[str] = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    MIDI_BASE_OCTAVE: int = 60  # C4

    INTERVALS: Dict[str, int] = {
        "R": 0, "m2": 1, "M2": 2, "m3": 3, "M3": 4, "P4": 5, "A4": 6, "TRITONE": 6, "d5": 6, "P5": 7, "A5": 8,
        "m6": 8, "M6": 9, "d7": 9, "m7": 10, "M7": 11, "P8": 12,
        "m9": 13, "M9": 14, "A9": 15,
        "P11": 17, "A11": 18,
        "m13": 20, "M13": 21
    }

    CHORD_STRUCTURES: Dict[str, List[int]] = {
        "major": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"]],
        "minor": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"]],
        "diminished": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["d5"]],
        "augmented": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["A5"]],
        "sus4": [INTERVALS["R"], INTERVALS["P4"], INTERVALS["P5"]],
        "sus2": [INTERVALS["R"], INTERVALS["M2"], INTERVALS["P5"]],
        "major6": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["M6"]],
        "minor6": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["M6"]],
        "dom7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["m7"]],
        "maj7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["M7"]],
        "min7": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["m7"]],
        "minMaj7": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["M7"]],
        "dim7": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["d5"], INTERVALS["d7"]],
        "halfdim7": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["d5"], INTERVALS["m7"]],  # m7b5
        "aug7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["A5"], INTERVALS["m7"]],
        "augMaj7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["A5"], INTERVALS["M7"]],
        "dom9": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"]],
        "maj9": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["M7"], INTERVALS["M9"]],
        "min9": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"]],
        "minMaj9": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["M7"], INTERVALS["M9"]],
        "halfdim9": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["d5"], INTERVALS["m7"], INTERVALS["m9"]],
        "dimM9": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["d5"], INTERVALS["d7"], INTERVALS["M9"]],
        "dom11": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"],
                  INTERVALS["P11"]],
        "maj11": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["M7"], INTERVALS["M9"],
                  INTERVALS["P11"]],
        "min11": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"],
                  INTERVALS["P11"]],
        "dom13": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"],
                  INTERVALS["M13"]],
        "maj13": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["P5"], INTERVALS["M7"], INTERVALS["M9"],
                  INTERVALS["M13"]],
        "min13": [INTERVALS["R"], INTERVALS["m3"], INTERVALS["P5"], INTERVALS["m7"], INTERVALS["M9"],
                  INTERVALS["M13"]],
    }

    # Scale Definitions
    SCALE_MAJOR: str = "Major"
    SCALE_NATURAL_MINOR: str = "Natural Minor"
    SCALE_HARMONIC_MINOR: str = "Harmonic Minor"
    SCALE_MELODIC_MINOR_ASC: str = "Melodic Minor (Asc)"
    SCALE_MAJOR_PENTATONIC: str = "Major Pentatonic"
    SCALE_MINOR_PENTATONIC: str = "Minor Pentatonic"

    # Diatonic Chords for Scales
    MAJOR_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "I": {"root_interval": 0, "base_quality": "major", "full_quality": "maj7", "display_suffix": "maj7"},
        "ii": {"root_interval": 2, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "iii": {"root_interval": 4, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "IV": {"root_interval": 5, "base_quality": "major", "full_quality": "maj7", "display_suffix": "maj7"},
        "V": {"root_interval": 7, "base_quality": "major", "full_quality": "dom7", "display_suffix": "7"},
        "vi": {"root_interval": 9, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "vii°": {"root_interval": 11, "base_quality": "diminished", "full_quality": "halfdim7",
                 "display_suffix": "m7b5"}
    }
    NATURAL_MINOR_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "i": {"root_interval": 0, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "ii°": {"root_interval": 2, "base_quality": "diminished", "full_quality": "halfdim7",
                "display_suffix": "m7b5"},
        "III": {"root_interval": 3, "base_quality": "major", "full_quality": "maj7", "display_suffix": "maj7"},
        "iv": {"root_interval": 5, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "v": {"root_interval": 7, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "VI": {"root_interval": 8, "base_quality": "major", "full_quality": "maj7", "display_suffix": "maj7"},
        "VII": {"root_interval": 10, "base_quality": "major", "full_quality": "dom7", "display_suffix": "7"}
    }
    HARMONIC_MINOR_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "i": {"root_interval": 0, "base_quality": "minor", "full_quality": "minMaj7", "display_suffix": "m(maj7)"},
        "ii°": {"root_interval": 2, "base_quality": "diminished", "full_quality": "halfdim7",
                "display_suffix": "m7b5"},
        "III+": {"root_interval": 3, "base_quality": "augmented", "full_quality": "augMaj7",
                 "display_suffix": "aug(maj7)"},
        "iv": {"root_interval": 5, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "V": {"root_interval": 7, "base_quality": "major", "full_quality": "dom7", "display_suffix": "7"},
        "VI": {"root_interval": 8, "base_quality": "major", "full_quality": "maj7", "display_suffix": "maj7"},
        "vii°7": {"root_interval": 11, "base_quality": "diminished", "full_quality": "dim7", "display_suffix": "dim7"}
    }
    MELODIC_MINOR_ASC_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "i": {"root_interval": 0, "base_quality": "minor", "full_quality": "minMaj7", "display_suffix": "m(maj7)"},
        "ii": {"root_interval": 2, "base_quality": "minor", "full_quality": "min7", "display_suffix": "m7"},
        "III+": {"root_interval": 3, "base_quality": "augmented", "full_quality": "augMaj7",
                 "display_suffix": "aug(maj7)"},
        "IV": {"root_interval": 5, "base_quality": "major", "full_quality": "dom7", "display_suffix": "7"},
        "V": {"root_interval": 7, "base_quality": "major", "full_quality": "dom7", "display_suffix": "7"},
        "vi°": {"root_interval": 9, "base_quality": "diminished", "full_quality": "halfdim7",
                "display_suffix": "m7b5"},
        "vii°": {"root_interval": 11, "base_quality": "diminished", "full_quality": "halfdim7",
                 "display_suffix": "m7b5"}
    }
    MAJOR_PENTATONIC_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "I": {"root_interval": 0, "base_quality": "major", "full_quality": "major", "display_suffix": ""},
        "ii_p": {"root_interval": 2, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"},
        "iii_p": {"root_interval": 4, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"},
        "V_p": {"root_interval": 7, "base_quality": "major", "full_quality": "major", "display_suffix": ""},
        "vi_p": {"root_interval": 9, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"}
    }
    MINOR_PENTATONIC_SCALE_DEGREES: Dict[str, Dict[str, Any]] = {
        "i_p": {"root_interval": 0, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"},
        "III_p": {"root_interval": 3, "base_quality": "major", "full_quality": "major", "display_suffix": ""},
        "iv_p": {"root_interval": 5, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"},
        "v_p": {"root_interval": 7, "base_quality": "minor", "full_quality": "minor", "display_suffix": "m"},
        "VII_p": {"root_interval": 10, "base_quality": "major", "full_quality": "major", "display_suffix": ""}
    }

    AVAILABLE_SCALES: Dict[str, Dict[str, Any]] = {
        "1": {"name": SCALE_MAJOR, "degrees": MAJOR_SCALE_DEGREES, "tonic_suffix": ""},
        "2": {"name": SCALE_NATURAL_MINOR, "degrees": NATURAL_MINOR_SCALE_DEGREES, "tonic_suffix": "m"},
        "3": {"name": SCALE_HARMONIC_MINOR, "degrees": HARMONIC_MINOR_SCALE_DEGREES, "tonic_suffix": "m"},
        "4": {"name": SCALE_MELODIC_MINOR_ASC, "degrees": MELODIC_MINOR_ASC_SCALE_DEGREES, "tonic_suffix": "m"},
        "5": {"name": SCALE_MAJOR_PENTATONIC, "degrees": MAJOR_PENTATONIC_SCALE_DEGREES, "tonic_suffix": ""},
        "6": {"name": SCALE_MINOR_PENTATONIC, "degrees": MINOR_PENTATONIC_SCALE_DEGREES, "tonic_suffix": "m"},
    }

    MIDI_PROGRAMS: Dict[int, str] = {
        0: "Acoustic Grand Piano", 1: "Bright Acoustic Piano", 2: "Electric Grand Piano", 3: "Honky-tonk Piano",
        4: "Electric Piano 1 (Rhodes)", 5: "Electric Piano 2 (Chorused)", 6: "Harpsichord", 7: "Clavinet",
        8: "Celesta", 9: "Glockenspiel", 10: "Music Box", 11: "Vibraphone", 12: "Marimba", 13: "Xylophone",
        16: "Drawbar Organ", 17: "Percussive Organ", 19: "Church Organ",
        24: "Acoustic Guitar (nylon)", 25: "Acoustic Guitar (steel)", 26: "Electric Guitar (jazz)",
        27: "Electric Guitar (clean)",
        28: "Electric Guitar (muted)", 29: "Overdriven Guitar", 30: "Distortion Guitar",
        32: "Acoustic Bass", 33: "Electric Bass (finger)", 34: "Electric Bass (pick)", 35: "Fretless Bass",
        36: "Slap Bass 1", 37: "Slap Bass 2", 38: "Synth Bass 1", 39: "Synth Bass 2",
        40: "Violin", 41: "Viola", 42: "Cello", 43: "Contrabass", 48: "String Ensemble 1", 49: "String Ensemble 2",
        52: "Choir Aahs", 53: "Voice Oohs", 54: "Synth Voice", 56: "Trumpet", 57: "Trombone", 60: "French Horn",
        64: "Soprano Sax", 65: "Alto Sax", 66: "Tenor Sax", 67: "Baritone Sax", 71: "Clarinet", 73: "Flute",
        80: "Synth Lead 1 (square)", 81: "Synth Lead 2 (sawtooth)", 88: "Synth Pad 1 (new age)",
        90: "Synth Pad 3 (polysynth)"
    }

# Ensure Mapping is available if used by get_numbered_option if it were moved here.
# For now, it's fine as MusicTheory itself does not use Mapping directly in its annotations.
# If get_note_name or get_note_index were to use Mapping, it would be needed.
# The original chorderizer.py used Union for get_numbered_option's `options` parameter,
# which might be Dict[str, Any] or Dict[int, Any].
# So, `Mapping` is a good general type hint for options in get_numbered_option.
# `MusicTheory` uses `Dict[str, Any]` and `Dict[int, str]` which are compatible.
# Adding `Mapping` to the import list for completeness, though not strictly used by these two classes directly.
