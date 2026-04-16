import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from colorama import Fore, Style


# -----------------------------------------------------------------------------
# Class MusicTheoryUtils: Utility functions for music theory
# -----------------------------------------------------------------------------
class MusicTheoryUtils:
    @staticmethod
    def get_note_name(note_index: int, use_flats: bool = False) -> str:
        if use_flats:
            flat_names = [
                "C",
                "Db",
                "D",
                "Eb",
                "E",
                "F",
                "Gb",
                "G",
                "Ab",
                "A",
                "Bb",
                "B",
            ]
            return flat_names[note_index % 12]
        return MusicTheory.CHROMATIC_NOTES[note_index % 12]

    @staticmethod
    def should_use_flats(tonic_str: str) -> bool:
        """Heuristic to determine if a scale/key should conventionally use flats."""
        tonic_upper = tonic_str.upper()
        # Explicit flat in name ('b') or known flat keys (F is the classic one)
        # We check for 'b' in lowercase string.
        if "b" in tonic_str.lower():
            return True
        # Check start of the string for keys that use flats but don't have 'b' in name (F Major)
        for flat_key in ["F", "BB", "EB", "AB", "DB", "GB"]:
            if tonic_upper.startswith(flat_key):
                return True
        return False

    # Pre-calculated cache for get_note_index to improve performance
    _NOTE_INDEX_CACHE: Dict[str, int] = {}

    @staticmethod
    def get_note_index(note_name: str) -> int:
        base_note = note_name.upper()

        # Check cache first for common notes
        if base_note in MusicTheoryUtils._NOTE_INDEX_CACHE:
            return MusicTheoryUtils._NOTE_INDEX_CACHE[base_note]

        flat_to_sharp_equivalents = {
            "DB": "C#",
            "EB": "D#",
            "FB": "E",
            "GB": "F#",
            "AB": "G#",
            "BB": "A#",
            "CB": "B",
        }
        for flat, sharp in flat_to_sharp_equivalents.items():
            if base_note.startswith(flat):
                base_note = sharp + base_note[len(flat) :]
                break
        root_note_str = ""
        for char_note in base_note:
            if char_note.isalpha() or char_note == "#":
                root_note_str += char_note
            else:
                break
        try:
            res = MusicTheory.CHROMATIC_NOTES.index(root_note_str)
            # Cache the result for future calls
            MusicTheoryUtils._NOTE_INDEX_CACHE[note_name.upper()] = res
            return res
        except ValueError as err:
            raise ValueError(
                f"Base note '{root_note_str}' from '{note_name}' not recognized."
            ) from err

    @staticmethod
    def split_chord_name(chord_name: str) -> Tuple[str, str]:
        """Splits a chord name into its root and its suffix (e.g., 'C#maj7' -> ('C#', 'maj7'))."""
        if not chord_name:
            return "", ""

        # Check for two-character roots (C#, Bb, etc.)
        if len(chord_name) > 1 and chord_name[1] in ["#", "b", "B"]:
            return chord_name[:2], chord_name[2:]

        # Default to one-character root
        return chord_name[:1], chord_name[1:]

    @staticmethod
    def transpose_chords(
        original_chords_dict: Dict[str, str],
        original_scale_tonic_str: str,
        new_scale_tonic_str: str,
    ) -> Optional[Dict[str, str]]:
        """Transposes a dictionary of chords to a new scale tonic."""
        try:
            original_tonic_idx = MusicTheoryUtils.get_note_index(original_scale_tonic_str)
            new_tonic_idx = MusicTheoryUtils.get_note_index(new_scale_tonic_str)
        except ValueError as e:
            logging.error(f"Error parsing tonic for transposition: {e}")
            print(
                f"{Fore.RED}Error parsing tonic for transposition. Please check your input.{Style.RESET_ALL}"
            )
            return None

        transposition_interval = new_tonic_idx - original_tonic_idx
        transposed_chords_dict = {}

        for degree, original_chord_name in original_chords_dict.items():
            root_str, suffix = MusicTheoryUtils.split_chord_name(original_chord_name)

            try:
                original_root_idx = MusicTheoryUtils.get_note_index(root_str)
            except ValueError:
                # If we can't parse the root, keep the original chord name
                transposed_chords_dict[degree] = original_chord_name
                continue

            new_root_idx = (original_root_idx + transposition_interval) % 12
            # Determine whether to use flats based on the new tonic
            use_flats = MusicTheoryUtils.should_use_flats(new_scale_tonic_str)

            new_root_name = MusicTheoryUtils.get_note_name(new_root_idx, use_flats)
            transposed_chords_dict[degree] = new_root_name + suffix

        return transposed_chords_dict


# -----------------------------------------------------------------------------
# Class MusicTheory: Constants and basic music theory definitions
# -----------------------------------------------------------------------------
class MusicTheory:
    def __init__(self):
        self.AVAILABLE_SCALES = {}
        self._load_scales()

    def note_to_midi(self, note_name: str) -> int:
        """Converts a note name (e.g., 'C#') to its 0-11 pitch class index."""
        return MusicTheoryUtils.get_note_index(note_name)

    def _load_scales(self):
        """Loads scale definitions from a JSON file."""
        data_path = os.path.join(os.path.dirname(__file__), "data", "scales.json")
        try:
            if os.path.exists(data_path):
                with open(data_path, encoding="utf-8") as f:
                    self.AVAILABLE_SCALES = json.load(f)
            else:
                logging.warning(
                    f"Scales data file not found at {data_path}. Using internal defaults."
                )
                self.AVAILABLE_SCALES = self._get_default_scales()
        except Exception as e:
            logging.error(f"Error loading scales from JSON: {e}")
            self.AVAILABLE_SCALES = self._get_default_scales()

    def _get_default_scales(self) -> Dict[str, Any]:
        """Provides a fallback set of scales if the JSON file cannot be loaded."""
        # Simple fallback with at least Major and Natural Minor
        return {
            "1": {
                "name": "Major",
                "tonic_suffix": "",
                "degrees": {
                    "I": {
                        "root_interval": 0,
                        "base_quality": "major",
                        "full_quality": "maj7",
                        "display_suffix": "maj7",
                    },
                    "ii": {
                        "root_interval": 2,
                        "base_quality": "minor",
                        "full_quality": "min7",
                        "display_suffix": "m7",
                    },
                    "iii": {
                        "root_interval": 4,
                        "base_quality": "minor",
                        "full_quality": "min7",
                        "display_suffix": "m7",
                    },
                    "IV": {
                        "root_interval": 5,
                        "base_quality": "major",
                        "full_quality": "maj7",
                        "display_suffix": "maj7",
                    },
                    "V": {
                        "root_interval": 7,
                        "base_quality": "major",
                        "full_quality": "dom7",
                        "display_suffix": "7",
                    },
                    "vi": {
                        "root_interval": 9,
                        "base_quality": "minor",
                        "full_quality": "min7",
                        "display_suffix": "m7",
                    },
                    "vii°": {
                        "root_interval": 11,
                        "base_quality": "diminished",
                        "full_quality": "halfdim7",
                        "display_suffix": "m7b5",
                    },
                },
            }
        }

    CHROMATIC_NOTES: List[str] = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]
    MIDI_BASE_OCTAVE: int = 60  # C4

    INTERVALS: Dict[str, int] = {
        "R": 0,
        "m2": 1,
        "M2": 2,
        "m3": 3,
        "M3": 4,
        "P4": 5,
        "A4": 6,
        "TRITONE": 6,
        "d5": 6,
        "P5": 7,
        "A5": 8,
        "m6": 8,
        "M6": 9,
        "d7": 9,
        "m7": 10,
        "M7": 11,
        "P8": 12,
        "m9": 13,
        "M9": 14,
        "A9": 15,
        "P11": 17,
        "A11": 18,
        "m13": 20,
        "M13": 21,
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
        "halfdim7": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["d5"],
            INTERVALS["m7"],
        ],  # m7b5
        "aug7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["A5"], INTERVALS["m7"]],
        "augMaj7": [INTERVALS["R"], INTERVALS["M3"], INTERVALS["A5"], INTERVALS["M7"]],
        "dom9": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
        ],
        "maj9": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["M7"],
            INTERVALS["M9"],
        ],
        "min9": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
        ],
        "minMaj9": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["P5"],
            INTERVALS["M7"],
            INTERVALS["M9"],
        ],
        "halfdim9": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["d5"],
            INTERVALS["m7"],
            INTERVALS["m9"],
        ],
        "dimM9": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["d5"],
            INTERVALS["d7"],
            INTERVALS["M9"],
        ],
        "dom11": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
            INTERVALS["P11"],
        ],
        "maj11": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["M7"],
            INTERVALS["M9"],
            INTERVALS["P11"],
        ],
        "min11": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
            INTERVALS["P11"],
        ],
        "dom13": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
            INTERVALS["M13"],
        ],
        "maj13": [
            INTERVALS["R"],
            INTERVALS["M3"],
            INTERVALS["P5"],
            INTERVALS["M7"],
            INTERVALS["M9"],
            INTERVALS["M13"],
        ],
        "min13": [
            INTERVALS["R"],
            INTERVALS["m3"],
            INTERVALS["P5"],
            INTERVALS["m7"],
            INTERVALS["M9"],
            INTERVALS["M13"],
        ],
    }

    AVAILABLE_SCALES: Dict[str, Dict[str, Any]] = {}

    MIDI_PROGRAMS: Dict[int, str] = {
        0: "Acoustic Grand Piano",
        1: "Bright Acoustic Piano",
        2: "Electric Grand Piano",
        3: "Honky-tonk Piano",
        4: "Electric Piano 1 (Rhodes)",
        5: "Electric Piano 2 (Chorused)",
        6: "Harpsichord",
        7: "Clavinet",
        8: "Celesta",
        9: "Glockenspiel",
        10: "Music Box",
        11: "Vibraphone",
        12: "Marimba",
        13: "Xylophone",
        16: "Drawbar Organ",
        17: "Percussive Organ",
        19: "Church Organ",
        24: "Acoustic Guitar (nylon)",
        25: "Acoustic Guitar (steel)",
        26: "Electric Guitar (jazz)",
        27: "Electric Guitar (clean)",
        28: "Electric Guitar (muted)",
        29: "Overdriven Guitar",
        30: "Distortion Guitar",
        32: "Acoustic Bass",
        33: "Electric Bass (finger)",
        34: "Electric Bass (pick)",
        35: "Fretless Bass",
        36: "Slap Bass 1",
        37: "Slap Bass 2",
        38: "Synth Bass 1",
        39: "Synth Bass 2",
        40: "Violin",
        41: "Viola",
        42: "Cello",
        43: "Contrabass",
        48: "String Ensemble 1",
        49: "String Ensemble 2",
        52: "Choir Aahs",
        53: "Voice Oohs",
        54: "Synth Voice",
        56: "Trumpet",
        57: "Trombone",
        60: "French Horn",
        64: "Soprano Sax",
        65: "Alto Sax",
        66: "Tenor Sax",
        67: "Baritone Sax",
        71: "Clarinet",
        73: "Flute",
        80: "Synth Lead 1 (square)",
        81: "Synth Lead 2 (sawtooth)",
        88: "Synth Pad 1 (new age)",
        90: "Synth Pad 3 (polysynth)",
    }
