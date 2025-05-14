import os
import random
from typing import List, Dict, Tuple, Optional, Any, Union

from mido import MidiFile, MidiTrack, Message, bpm2tempo, MetaMessage


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


# -----------------------------------------------------------------------------
# UI Helper Functions
# -----------------------------------------------------------------------------
def print_welcome_message() -> None:
    print("\033[32mWelcome to the Advanced Chord Generator!\033[0m")
    print("\033[33mModularized Version\033[0m")


def print_operation_cancelled() -> None:
    print("\n\033[31mOperation cancelled by the user.\033[0m")


def get_yes_no_answer(prompt: str) -> bool:
    while True:
        response = input(f"\033[34m{prompt} (yes/no): \033[0m").strip().lower()
        if response in ["yes", "y", "si", "s"]: return True  # Added si/s for convenience if user slips
        if response in ["no", "n"]: return False
        print("\033[31mInvalid response. Please enter 'yes' or 'no'.\033[0m")


def get_numbered_option(prompt: str, options: Dict[Union[str, int], Any],
                        allow_cancel: bool = True, cancel_key: str = "0") -> Optional[str]:
    print(f"\n\033[36m{prompt}\033[0m")
    display_options = {str(k): v for k, v in options.items()}

    for key_str, value in display_options.items():
        display_name = value.get('name', value) if isinstance(value, dict) else str(value)
        print(f"  {key_str}. {display_name}")

    if allow_cancel:
        print(f"  {cancel_key}. Cancel / Back")

    while True:
        try:
            user_input_str = input("Choose an option number: ").strip()
            if not user_input_str:
                continue

            if allow_cancel and user_input_str == cancel_key:
                return None

            if user_input_str in display_options:
                return user_input_str
            else:
                print("\033[31mInvalid option.\033[0m")
        except (EOFError, KeyboardInterrupt):
            print_operation_cancelled()
            return None


def get_chord_settings() -> Tuple[Optional[int], Optional[int]]:
    print("\n\033[36m--- Chord Settings ---\033[0m")
    extension_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5}
    extension_options = {
        "1": "Simple Triads", "2": "Sixths (or sevenths if 6th doesn't apply)",
        "3": "Sevenths (scale default)", "4": "Ninths",
        "5": "Elevenths (can sound dense!)", "6": "Thirteenths (can sound very dense!)"
    }
    ext_choice_key = get_numbered_option("Chord extension level:", extension_options)
    if ext_choice_key is None: return None, None
    selected_extension_level = extension_map[ext_choice_key]

    inversion_options = {"1": "Root Position", "2": "1st Inversion", "3": "2nd Inversion",
                         "4": "3rd Inversion (for 7ths+)"}
    inv_choice_key = get_numbered_option("Chord inversion:", inversion_options)
    if inv_choice_key is None: return None, None
    selected_inversion = int(inv_choice_key) - 1
    return selected_extension_level, selected_inversion


def get_tablature_filter() -> str:
    tab_filter_options = {
        "1": "All tablatures", "2": "Only Minor chords (minor base quality)",
        "3": "Only chords with Seventh", "4": "Only chords with Ninth",
        "5": "Only Sixth chords (X6, Xm6)", "6": "Only chords with Eleventh",
        "7": "Only chords with Thirteenth", "8": "No tablatures"
    }
    choice = get_numbered_option("--- Filter for Displaying Tablatures ---", tab_filter_options,
                                 allow_cancel=True)
    return choice if choice is not None else "8"  # Default to None if cancelled


# -----------------------------------------------------------------------------
# Class UIManager: Manages console user interface
# -----------------------------------------------------------------------------
class UIManager:
    def __init__(self, theory: MusicTheory):
        self.theory = theory

    def select_tonic_and_scale(self) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        print("\n\033[36m--- Select Scale Tonic ---\033[0m")
        tonic_options = {str(i + 1): note for i, note in enumerate(self.theory.CHROMATIC_NOTES)}

        tonic_choice_key = get_numbered_option("Tonic:", tonic_options, allow_cancel=True, cancel_key="0")
        if tonic_choice_key is None: return None, None
        selected_tonic = tonic_options[tonic_choice_key]

        print("\n\033[36m--- Select Scale Type ---\033[0m")
        scale_choice_key = get_numbered_option("Scale Type:", self.theory.AVAILABLE_SCALES,
                                               allow_cancel=True, cancel_key="0")
        if scale_choice_key is None: return None, None

        selected_scale_info = self.theory.AVAILABLE_SCALES[scale_choice_key]
        full_scale_tonic_name = selected_tonic + selected_scale_info["tonic_suffix"]
        return full_scale_tonic_name, selected_scale_info

    def get_advanced_midi_options(self) -> Dict[str, Any]:
        print("\n\033[36m--- Advanced MIDI Options ---\033[0m")
        options = {
            "bpm": 120, "base_velocity": 70, "velocity_randomization_range": 0,
            "chord_instrument": 0, "add_bass_track": False, "bass_instrument": 33,  # Acoustic Bass
            "arpeggio_style": None, "arpeggio_note_duration_beats": 0.25, "strum_delay_ms": 0
        }

        try:
            bpm_in = input(f"BPM (tempo) for MIDI [default: {options['bpm']}]: ").strip()
            if bpm_in: options["bpm"] = int(bpm_in)
            if not (20 <= options["bpm"] <= 300):  # Reasonable range
                print(f"\033[33mWarning: BPM {options['bpm']} is outside the typical range (20-300).\033[0m")
            if options["bpm"] <= 0: options["bpm"] = 120  # Fallback
        except ValueError:
            print(f"\033[31mInvalid BPM, using {options['bpm']}.\033[0m")

        try:
            vel_in = input(f"Base note velocity (0-127) [default: {options['base_velocity']}]: ").strip()
            if vel_in: options["base_velocity"] = int(vel_in)
            options["base_velocity"] = max(0, min(127, options["base_velocity"]))
        except ValueError:
            print(f"\033[31mInvalid velocity, using {options['base_velocity']}.\033[0m")

        if get_yes_no_answer("Add slight randomization to velocity?"):
            try:
                rand_in = input(f"Randomization range (+/-) [default: 5]: ").strip()
                if rand_in: options["velocity_randomization_range"] = int(rand_in)
                options["velocity_randomization_range"] = max(0, min(20, options["velocity_randomization_range"]))
            except ValueError:
                print(f"\033[31mInvalid range, using 0.\033[0m")

        chord_instr_key = get_numbered_option("Instrument for chords:", self.theory.MIDI_PROGRAMS,
                                              allow_cancel=False)  # Must select an instrument
        options["chord_instrument"] = int(chord_instr_key)

        options["add_bass_track"] = get_yes_no_answer("Add bass track (root notes)?")
        if options["add_bass_track"]:
            bass_instr_key = get_numbered_option("Instrument for bass:", self.theory.MIDI_PROGRAMS,
                                                 allow_cancel=False)
            options["bass_instrument"] = int(bass_instr_key)

        if get_yes_no_answer("Arpeggiate chords? (Otherwise, they will be block chords)"):
            arp_styles = {"1": "up", "2": "down", "3": "updown"}
            style_key = get_numbered_option("Arpeggio style:", arp_styles)
            if style_key:
                options["arpeggio_style"] = arp_styles[style_key]
                try:
                    arp_dur_in = input(
                        f"Duration of each arpeggio note in beats [default: {options['arpeggio_note_duration_beats']}]: ").strip()
                    if arp_dur_in: options["arpeggio_note_duration_beats"] = float(arp_dur_in)
                    if options["arpeggio_note_duration_beats"] <= 0: options["arpeggio_note_duration_beats"] = 0.25
                except ValueError:
                    print(
                        f"\033[31mInvalid arpeggio note duration, using {options['arpeggio_note_duration_beats']}.\033[0m")

        if not options["arpeggio_style"] and get_yes_no_answer(
                "Add strumming effect to block chords?"):
            try:
                strum_in = input(f"Strum delay between notes (milliseconds) [default: 15ms]: ").strip()
                if strum_in: options["strum_delay_ms"] = int(strum_in)
                options["strum_delay_ms"] = max(0, min(100, options["strum_delay_ms"]))  # Cap delay
            except ValueError:
                print(f"\033[31mInvalid strum delay, using 0.\033[0m")
        return options


# -----------------------------------------------------------------------------
# Chord Transposition Function
# -----------------------------------------------------------------------------
def transpose_chord_names(original_chords_dict: Dict[str, str],
                          original_scale_tonic_str: str, new_scale_tonic_str: str
                          ) -> Optional[Dict[str, str]]:
    try:
        original_tonic_idx = MusicTheoryUtils.get_note_index(original_scale_tonic_str)
        new_tonic_idx = MusicTheoryUtils.get_note_index(new_scale_tonic_str)
    except ValueError as e:
        print(f"\033[31mError parsing tonic for transposition: {e}\033[0m")
        return None

    transposition_interval = new_tonic_idx - original_tonic_idx
    transposed_chords_dict = {}

    for degree, original_chord_name in original_chords_dict.items():
        original_chord_root_str, chord_suffix, parsed = "", "", False
        # Basic parsing for root and suffix
        if len(original_chord_name) > 1 and original_chord_name[1] in ['#', 'b', 'B']:  # e.g. C#, Bb
            if original_chord_name[0].isalpha():
                original_chord_root_str, chord_suffix, parsed = original_chord_name[:2], original_chord_name[2:], True
        if not parsed and len(original_chord_name) > 0 and original_chord_name[0].isalpha():  # e.g. C, G
            original_chord_root_str, chord_suffix, parsed = original_chord_name[0], original_chord_name[1:], True

        if not parsed:  # Could not parse, keep original
            transposed_chords_dict[degree] = original_chord_name
            continue
        try:
            original_root_idx = MusicTheoryUtils.get_note_index(original_chord_root_str)
        except ValueError:  # Could not parse root of this specific chord
            transposed_chords_dict[degree] = original_chord_name
            continue

        new_root_idx = (original_root_idx + transposition_interval) % 12
        use_flats_for_new_key = 'b' in new_scale_tonic_str.upper() or \
                                new_scale_tonic_str.upper() in ["F", "Bb", "Eb", "Ab", "Db", "Gb"]
        new_root_name = MusicTheoryUtils.get_note_name(new_root_idx, use_flats_for_new_key)
        transposed_chords_dict[degree] = new_root_name + chord_suffix
    return transposed_chords_dict


# -----------------------------------------------------------------------------
# Class ChordGenerator
# -----------------------------------------------------------------------------
class ChordGenerator:
    def __init__(self, theory: MusicTheory):
        self.theory = theory

    def generate_scale_chords(self, scale_tonic_str: str, scale_info: Dict[str, Any],
                              extension_level: int = 2, inversion: int = 0
                              ) -> Tuple[Dict[str, str], Dict[str, List[str]], Dict[str, List[int]], Dict[str, str]]:
        generated_chords: Dict[str, str] = {}
        notes_per_chord_names: Dict[str, List[str]] = {}
        notes_per_chord_midi: Dict[str, List[int]] = {}
        generated_base_qualities: Dict[str, str] = {}

        try:
            scale_tonic_index = MusicTheoryUtils.get_note_index(scale_tonic_str)
        except ValueError as e:
            print(f"\033[31mError: Invalid scale tonic '{scale_tonic_str}': {e}\033[0m")
            return {}, {}, {}, {}

        scale_degrees_info = scale_info["degrees"]

        for degree_roman, degree_definition in scale_degrees_info.items():
            chord_root_abs_idx = (scale_tonic_index + degree_definition["root_interval"]) % 12
            chord_root_name = MusicTheoryUtils.get_note_name(chord_root_abs_idx)
            base_quality = degree_definition["base_quality"]
            degree_display_suffix = degree_definition["display_suffix"]
            chord_type_to_use = degree_definition["full_quality"]  # Default to full quality (e.g., 7ths)

            # Adjust chord type and suffix based on selected extension level
            if extension_level == 0:  # Triads
                triad_map = {"major": "major", "minor": "minor", "diminished": "diminished", "augmented": "augmented"}
                chord_type_to_use = triad_map.get(base_quality, base_quality)
                degree_display_suffix = {"major": "", "minor": "m", "diminished": "dim", "augmented": "aug"}.get(
                    base_quality, "")
            elif extension_level == 1:  # Sixths (or default 7ths if 6th doesn't fit well)
                if chord_type_to_use == "maj7":  # Typically Major scale I, IV
                    chord_type_to_use = "major6"
                    degree_display_suffix = "6"
                elif chord_type_to_use == "min7":  # Typically Major scale ii, iii, vi
                    chord_type_to_use = "minor6"
                    degree_display_suffix = "m6"
                # For other cases (e.g., V7, vii°), keep their 7th quality or base triad if 6th is odd
            elif extension_level >= 3:  # Ninths, Elevenths, Thirteenths
                extension_map_dict = {
                    "dom7": {3: "dom9", 4: "dom11", 5: "dom13"},
                    "maj7": {3: "maj9", 4: "maj11", 5: "maj13"},
                    "min7": {3: "min9", 4: "min11", 5: "min13"}
                }
                suffix_map_dict = {
                    "dom9": "9", "dom11": "11", "dom13": "13",
                    "maj9": "maj9", "maj11": "maj11", "maj13": "maj13",
                    "min9": "m9", "min11": "m11", "min13": "m13"
                }
                if chord_type_to_use in extension_map_dict and \
                        extension_level in extension_map_dict[chord_type_to_use]:
                    new_type = extension_map_dict[chord_type_to_use][extension_level]
                    if new_type in self.theory.CHORD_STRUCTURES:
                        chord_type_to_use = new_type
                        degree_display_suffix = suffix_map_dict.get(chord_type_to_use, degree_display_suffix)

            # Get intervals for the determined chord type
            chord_intervals_relative = list(
                self.theory.CHORD_STRUCTURES.get(chord_type_to_use, self.theory.CHORD_STRUCTURES.get(base_quality, [])))
            if not chord_intervals_relative:  # Fallback if type is unknown
                print(
                    f"\033[33mWarning: Chord structure for '{chord_type_to_use}' or '{base_quality}' not found. Skipping chord for degree {degree_roman}.\033[0m")
                continue

            final_chord_display_name = chord_root_name + degree_display_suffix

            # Apply inversion
            if 0 < inversion < len(chord_intervals_relative):
                temp_intervals = list(chord_intervals_relative)  # Make a mutable copy
                for _ in range(inversion):
                    if not temp_intervals: break
                    bass_relative_interval = temp_intervals.pop(0)
                    temp_intervals.append(bass_relative_interval + 12)  # Add to top, an octave higher
                chord_intervals_relative = sorted(list(set(temp_intervals)))  # Remove duplicates and sort

            # Generate MIDI notes for the chord
            current_midi_notes: List[int] = []
            unique_sorted_intervals = sorted(list(set(chord_intervals_relative)))
            last_added_midi_note = -1  # To ensure ascending notes in voicing

            # Determine a base octave offset to keep chords roughly around C4
            initial_octave_offset = 0
            if unique_sorted_intervals:
                # Estimate position of the first note if placed directly
                first_note_in_octave_relative = (chord_root_abs_idx + unique_sorted_intervals[0]) % 12
                tentative_first_midi_note = self.theory.MIDI_BASE_OCTAVE + first_note_in_octave_relative

                # If the first note is too low and it's a root/low interval, shift up
                if tentative_first_midi_note < self.theory.MIDI_BASE_OCTAVE - 6 and unique_sorted_intervals[0] >= 0:
                    initial_octave_offset = 12
                # If the first note is too high for a root/low interval, shift down (less common for root)
                elif tentative_first_midi_note > self.theory.MIDI_BASE_OCTAVE + 6 and unique_sorted_intervals[
                    0] <= 7:  # Heuristic
                    initial_octave_offset = -12

            for rel_interval in unique_sorted_intervals:
                interval_octave_offset = (
                                                     rel_interval // 12) * 12  # Octave from interval itself (e.g., M9 is R + 14 semitones)
                candidate_midi_note = (self.theory.MIDI_BASE_OCTAVE + initial_octave_offset +
                                       ((chord_root_abs_idx + rel_interval) % 12) + interval_octave_offset)

                # Ensure notes are generally ascending for a simple voicing
                while last_added_midi_note != -1 and candidate_midi_note <= last_added_midi_note:
                    candidate_midi_note += 12

                # MIDI range adjustments (heuristic to keep notes within a playable/sensible range)
                if candidate_midi_note > 108: candidate_midi_note -= 12  # Too high, try octave lower
                if candidate_midi_note < 21: candidate_midi_note += 12  # Too low, try octave higher

                # For wider chords, try to keep upper notes from going excessively high if a lower octave is available
                if len(unique_sorted_intervals) > 4 and \
                        candidate_midi_note > self.theory.MIDI_BASE_OCTAVE + 24 + initial_octave_offset:  # Roughly 2 octaves above C4
                    if (candidate_midi_note - 12) > last_added_midi_note or last_added_midi_note == -1:
                        candidate_midi_note -= 12

                if 0 <= candidate_midi_note <= 127:  # Valid MIDI note
                    current_midi_notes.append(candidate_midi_note)
                    last_added_midi_note = candidate_midi_note

            current_midi_notes = sorted(list(set(current_midi_notes)))  # Final sort and unique
            current_chord_note_names = [MusicTheoryUtils.get_note_name(n) for n in current_midi_notes]

            generated_chords[degree_roman] = final_chord_display_name
            notes_per_chord_names[degree_roman] = current_chord_note_names
            notes_per_chord_midi[degree_roman] = current_midi_notes
            generated_base_qualities[degree_roman] = base_quality

        return generated_chords, notes_per_chord_names, notes_per_chord_midi, generated_base_qualities


# -----------------------------------------------------------------------------
# Class TablatureGenerator
# -----------------------------------------------------------------------------
class TablatureGenerator:
    def __init__(self, theory: MusicTheory):
        self.theory = theory
        # Standard guitar tuning, MIDI notes
        self.GUITAR_OPEN_STRINGS_MIDI: Dict[str, int] = {"e1": 64, "B2": 59, "G3": 55, "D4": 50, "A5": 45, "E6": 40}
        self.TAB_STRING_NAMES: List[str] = ["e1", "B2", "G3", "D4", "A5", "E6"]  # High e to Low E

    def _assign_fret_to_string(self, chord_note_midi: int, open_string_midi: int, max_frets: int) -> Optional[int]:
        """Helper to find fret for a note on a string."""
        if chord_note_midi >= open_string_midi:
            fret = chord_note_midi - open_string_midi
            if 0 <= fret <= max_frets:
                return fret
        return None

    def generate_simple_tab(self, chord_display_name: str, chord_midi_notes: List[int]) -> List[str]:
        # This is a very basic tablature generator, prioritizing lower frets and one note per string.
        frets_on_strings = {name: "-" for name in self.TAB_STRING_NAMES}
        sorted_midi_notes = sorted(list(set(chord_midi_notes)))  # Ascending MIDI notes
        notes_placed_in_tab = [False] * len(sorted_midi_notes)
        max_allowable_frets = 15  # Arbitrary limit for simplicity

        # Iterate from highest string (e1) to lowest (E6) to try and place notes
        for string_name in reversed(self.TAB_STRING_NAMES):  # e.g. E6, A5, D4, G3, B2, e1
            open_string_note_midi = self.GUITAR_OPEN_STRINGS_MIDI[string_name]
            # Try to place an unplaced chord note on this string
            for i, chord_note in enumerate(sorted_midi_notes):
                if notes_placed_in_tab[i]:
                    continue  # This note is already placed

                fret = self._assign_fret_to_string(chord_note, open_string_note_midi, max_allowable_frets)
                if fret is not None and frets_on_strings[string_name] == "-":  # If string is available
                    frets_on_strings[string_name] = str(fret)
                    notes_placed_in_tab[i] = True
                    break  # Move to the next string once a note is placed on this one

        tab_lines: List[str] = [f"Chord: {chord_display_name} (simple tab)"]
        for string_name in self.TAB_STRING_NAMES:  # Display from e1 (high) to E6 (low)
            fret_display = frets_on_strings[string_name]
            tab_lines.append(f"{string_name.ljust(2)}|--{fret_display.rjust(2, '-')}--|")
        return tab_lines


# -----------------------------------------------------------------------------
# Class MidiGenerator
# -----------------------------------------------------------------------------
class MidiGenerator:
    def __init__(self, theory: MusicTheory):
        self.theory = theory

    def generate_midi_file(self, chords_to_process: List[Dict[str, Any]], output_filename: str,
                           midi_options: Dict[str, Any]) -> None:
        ticks_per_beat = 480  # Standard resolution
        midi_file = MidiFile(ticks_per_beat=ticks_per_beat)

        # Chord Track
        chord_track = MidiTrack()
        midi_file.tracks.append(chord_track)
        chord_track.append(MetaMessage('track_name', name='Chords Track', time=0))
        chord_track.append(Message('program_change', program=midi_options["chord_instrument"], channel=0, time=0))
        chord_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(midi_options["bpm"]), time=0))

        # Bass Track (optional)
        bass_track: Optional[MidiTrack] = None
        if midi_options["add_bass_track"]:
            bass_track = MidiTrack()
            midi_file.tracks.append(bass_track)
            bass_track.append(MetaMessage('track_name', name='Bass Track', time=0))
            bass_track.append(Message('program_change', program=midi_options["bass_instrument"], channel=1, time=0))
            # Bass track also needs tempo if it's the first event-producing track for it
            bass_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(midi_options["bpm"]), time=0))

        for i_chord, chord_data in enumerate(chords_to_process):
            chord_midi_notes = chord_data["notas_midi"]
            if not chord_midi_notes:
                continue

            chord_duration_beats = chord_data["duracion_beats"]
            chord_duration_ticks = int(chord_duration_beats * ticks_per_beat)

            # --- Bass Track ---
            if bass_track and midi_options["add_bass_track"]:
                # Find the lowest note of the chord for the bass, then drop it to a bass register
                bass_note_midi = min(chord_midi_notes)
                while bass_note_midi > self.theory.MIDI_BASE_OCTAVE - 12:  # Ensure it's below C3
                    bass_note_midi -= 12
                if bass_note_midi < 21:  # Ensure it's not too low (below E0)
                    bass_note_midi += 12

                # Slightly higher velocity for bass, or make it configurable
                bass_velocity = max(0, min(127, midi_options["base_velocity"] + 10))

                # Bass note starts with the chord (time=0 relative to previous bass event)
                bass_track.append(Message('note_on', note=bass_note_midi, velocity=bass_velocity, channel=1, time=0))
                # Bass note lasts for the full duration of the chord
                bass_track.append(
                    Message('note_off', note=bass_note_midi, velocity=0, channel=1, time=chord_duration_ticks))

            # --- Chord Track ---
            # All events for a given chord start at time=0 relative to the end of the previous chord's events on this track.
            # Mido handles advancing the track's internal time counter with each message's `time` attribute.

            if midi_options["arpeggio_style"]:
                arp_notes_sequence = list(chord_midi_notes)  # Copy
                if midi_options["arpeggio_style"] == "down":
                    arp_notes_sequence.reverse()
                elif midi_options["arpeggio_style"] == "updown":
                    # e.g., [1,2,3,4] -> [1,2,3,4,3,2] (excluding first and last if len > 1)
                    if len(arp_notes_sequence) > 1:
                        arp_notes_sequence += arp_notes_sequence[len(arp_notes_sequence) - 2::-1]

                arp_note_indiv_duration_ticks = int(midi_options["arpeggio_note_duration_beats"] * ticks_per_beat)
                num_arp_notes = len(arp_notes_sequence)

                if num_arp_notes > 0:
                    for idx, note_val in enumerate(arp_notes_sequence):
                        velocity = max(0, min(127, midi_options["base_velocity"] + random.randint(
                            -midi_options["velocity_randomization_range"] // 2,
                            midi_options["velocity_randomization_range"] // 2)))

                        # Each arpeggio note_on starts right after the previous one ends.
                        # So, delta time for note_on is 0 (relative to previous note_off).
                        chord_track.append(Message('note_on', note=note_val, velocity=velocity, channel=0, time=0))

                        current_arp_note_actual_duration = arp_note_indiv_duration_ticks
                        if idx == num_arp_notes - 1:  # This is the last note of the arpeggio sequence
                            # Calculate total time taken by previous arpeggio notes in this chord
                            time_taken_by_prev_arp_notes = (num_arp_notes - 1) * arp_note_indiv_duration_ticks
                            # Remaining duration for this last arpeggio note to fill the chord slot
                            remaining_slot_time = chord_duration_ticks - time_taken_by_prev_arp_notes
                            current_arp_note_actual_duration = max(0, remaining_slot_time)

                            if arp_note_indiv_duration_ticks > 0 and \
                                    num_arp_notes * arp_note_indiv_duration_ticks > chord_duration_ticks + (
                                    arp_note_indiv_duration_ticks / 2):  # Allow some slack
                                print(f"\033[33mWarning: Arpeggio for chord '{chord_data.get('nombre', '')}' "
                                      f"({num_arp_notes} notes * {arp_note_indiv_duration_ticks} ticks) "
                                      f"may exceed chord slot duration ({chord_duration_ticks} ticks). "
                                      f"Last note duration adjusted to {current_arp_note_actual_duration}.\033[0m")

                        chord_track.append(Message('note_off', note=note_val, velocity=0, channel=0,
                                                   time=current_arp_note_actual_duration))

            else:  # Block chords (with optional strum)
                time_offset_for_strum_completion = 0  # Time from first note_on to last note_on in strum

                # Add all note_on messages first, with strum delays
                for idx, note_val in enumerate(chord_midi_notes):
                    velocity = max(0, min(127, midi_options["base_velocity"] + random.randint(
                        -midi_options["velocity_randomization_range"] // 2,
                        midi_options["velocity_randomization_range"] // 2)))

                    delta_t_for_this_note_on = 0
                    if idx > 0 and midi_options["strum_delay_ms"] > 0:
                        # Calculate strum delay in ticks
                        strum_delay_seconds = midi_options["strum_delay_ms"] / 1000.0
                        strum_delay_beats = strum_delay_seconds * (midi_options["bpm"] / 60.0)
                        strum_delay_ticks = int(strum_delay_beats * ticks_per_beat)
                        delta_t_for_this_note_on = strum_delay_ticks
                        time_offset_for_strum_completion += strum_delay_ticks

                    # First note_on of the block chord has time=0 (relative to previous chord's end)
                    # Subsequent note_on events in the strum have their respective strum_delay_ticks
                    chord_track.append(Message('note_on', note=note_val, velocity=velocity, channel=0,
                                               time=delta_t_for_this_note_on if idx > 0 else 0))

                # Now add all note_off messages. They should all end effectively at the same time.
                # The duration for the first note_off will be the total chord duration minus the time taken by the strum.
                duration_for_first_note_off = chord_duration_ticks - time_offset_for_strum_completion
                if duration_for_first_note_off < 0:
                    # This means strum is longer than chord duration, which is problematic.
                    print(f"\033[33mWarning: Strum effect for chord '{chord_data.get('nombre', '')}' "
                          f"is longer than the chord's duration. Adjusting.\033[0m")
                    duration_for_first_note_off = 0  # Or some small positive value

                for idx, note_val in enumerate(chord_midi_notes):
                    # The first note_off consumes the main duration.
                    # Subsequent note_offs have time=0, meaning they happen at the same "absolute" time
                    # as the end of the first note_off, relative to their own note_on.
                    chord_track.append(Message('note_off', note=note_val, velocity=0, channel=0,
                                               time=duration_for_first_note_off if idx == 0 else 0))
        try:
            output_directory = os.path.dirname(output_filename)
            if output_directory and not os.path.exists(output_directory):
                os.makedirs(output_directory, exist_ok=True)
                print(f"\033[32mDirectory '{output_directory}' created.\033[0m")
            midi_file.save(output_filename)
            print(f"\033[32mMIDI file '{output_filename}' generated successfully.\033[0m")
        except Exception as e:
            print(f"\033[31mError saving MIDI file '{output_filename}': {e}\033[0m")
            import traceback
            traceback.print_exc()


# -----------------------------------------------------------------------------
# Main Program Logic
# -----------------------------------------------------------------------------
def _generate_midi_filename_helper(tonic: str, scale_info: Dict[str, Any], base_dir: str, prefix: str = "prog_") -> str:
    safe_tonic = tonic.replace('#', 'sharp').replace('b', 'flat')
    safe_scale_name = scale_info['name'].replace(' ', '_').replace('(', '').replace(')', '')
    filename = f"{prefix}{safe_tonic}_{safe_scale_name}.mid"
    return os.path.join(base_dir, filename)


def main():
    theory = MusicTheory()
    ui = UIManager(theory)
    chord_builder = ChordGenerator(theory)
    tab_builder = TablatureGenerator(theory)
    midi_builder = MidiGenerator(theory)

    print_welcome_message()
    home_directory = os.path.expanduser("~")
    midi_export_default_dir = os.path.join(home_directory, "chord_generator_midi_exports")

    while True:
        print("\n" + "=" * 70)
        selected_scale_tonic, selected_scale_info = ui.select_tonic_and_scale()
        if selected_scale_tonic is None or selected_scale_info is None:
            print("\033[32mExiting program.\033[0m")
            break

        chord_settings_tuple = get_chord_settings()
        if chord_settings_tuple is None:
            continue  # User cancelled
        selected_extension_lvl, selected_inversion_idx = chord_settings_tuple

        # Generate chords for the selected scale
        gen_chord_names, gen_note_names, gen_midi_notes, gen_base_qualities = \
            chord_builder.generate_scale_chords(
                selected_scale_tonic, selected_scale_info,
                selected_extension_lvl, selected_inversion_idx
            )

        if not gen_chord_names:
            print(f"\033[31mCould not generate chords for {selected_scale_tonic}.\033[0m")
            continue

        print(
            f"\n\033[32mChords generated for the scale of {selected_scale_tonic} ({selected_scale_info['name']}):\033[0m")
        # You could add more info about extension/inversion here if desired

        tab_display_filter_key = get_tablature_filter()

        for degree, chord_name_display in gen_chord_names.items():
            # Determine color for display based on quality (example)
            base_qual = gen_base_qualities.get(degree)
            color_code = "\033[32m"  # Default green
            if base_qual == "minor":
                color_code = "\033[34m"  # Blue
            elif base_qual == "diminished" or "ø" in chord_name_display or "m7b5" in chord_name_display:
                color_code = "\033[35m"  # Magenta
            elif base_qual == "augmented" or "+" in chord_name_display:
                color_code = "\033[33m"  # Yellow
            reset_color_code = "\033[0m"

            note_names_str = ", ".join(gen_note_names.get(degree, []))
            midi_notes_str = ", ".join(map(str, gen_midi_notes.get(degree, [])))
            print(
                f"  {degree.ljust(5)}: {color_code}{chord_name_display.ljust(15)}{reset_color_code} "
                f"(Notes: {note_names_str.ljust(25)}) (MIDI: {midi_notes_str})")

            # Tablature display logic
            show_this_tab = False
            if tab_display_filter_key == "8":  # None
                pass
            elif tab_display_filter_key == "1":  # All
                show_this_tab = True
            else:  # Specific filters
                if tab_display_filter_key == "2" and base_qual == "minor":
                    show_this_tab = True
                elif tab_display_filter_key == "3" and "7" in chord_name_display:
                    show_this_tab = True  # Simple check
                elif tab_display_filter_key == "4" and "9" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "5":  # Sixth chords (e.g., C6, Am6)
                    # This check could be more robust by parsing the suffix properly
                    if chord_name_display.endswith("6") and not chord_name_display.endswith("m7b6"):  # Avoid confusion
                        show_this_tab = True
                elif tab_display_filter_key == "6" and "11" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "7" and "13" in chord_name_display:
                    show_this_tab = True

            if show_this_tab and gen_midi_notes.get(degree):
                tab_lines_list = tab_builder.generate_simple_tab(chord_name_display, gen_midi_notes[degree])
                for tab_line in tab_lines_list:
                    print(f"    {tab_line}")

        # --- MIDI Generation / Progression ---
        print("\n\033[36m--- MIDI Generation Options ---\033[0m")
        chords_for_midi_processing: List[Dict[str, Any]] = []
        if get_yes_no_answer(
                "Define a chord progression for MIDI? (If no, all diatonic chords will be used sequentially)"):
            progression_input_str = input(
                "Enter progression (degrees separated by '-', e.g., I-V-vi-IV). "
                "Optional duration in beats (e.g., I:4-V:2-vi:2-IV:4 ): "
            ).strip().upper()
            progression_items = progression_input_str.split('-')
            for item_str in progression_items:
                item_str = item_str.strip()
                if not item_str: continue

                current_prog_degree, current_beats_duration = item_str, 4.0  # Default duration
                if ":" in item_str:
                    parts = item_str.split(':', 1)
                    current_prog_degree = parts[0].strip()
                    try:
                        current_beats_duration = float(parts[1].strip())
                        if current_beats_duration <= 0: current_beats_duration = 4.0
                    except ValueError:
                        print(f"\033[31mInvalid duration for '{current_prog_degree}', using 4.0 beats.\033[0m")

                if current_prog_degree in gen_chord_names:
                    chords_for_midi_processing.append({
                        "grado": current_prog_degree,
                        "nombre": gen_chord_names[current_prog_degree],
                        "notas_midi": gen_midi_notes[current_prog_degree],
                        "duracion_beats": current_beats_duration
                    })
                else:
                    print(f"\033[31mDegree '{current_prog_degree}' not found in generated chords. Skipping.\033[0m")
        else:  # Default to all diatonic chords
            for degree_key in selected_scale_info["degrees"].keys():  # Iterate in defined order
                if degree_key in gen_chord_names:
                    chords_for_midi_processing.append({
                        "grado": degree_key,
                        "nombre": gen_chord_names[degree_key],
                        "notas_midi": gen_midi_notes[degree_key],
                        "duracion_beats": 2.0  # Default duration for sequential diatonic
                    })

        if not chords_for_midi_processing:
            print("\033[31mNo chords selected for MIDI processing.\033[0m")
            continue

        advanced_midi_opts = ui.get_advanced_midi_options()

        # Sanitize file names
        suggested_midi_path = _generate_midi_filename_helper(selected_scale_tonic, selected_scale_info, midi_export_default_dir)

        output_midi_filename = input(f"Enter MIDI filename [default: {suggested_midi_path}]: ").strip()
        if not output_midi_filename:
            output_midi_filename = suggested_midi_path

        midi_builder.generate_midi_file(chords_for_midi_processing, output_midi_filename, advanced_midi_opts)

        # --- Transposition ---
        if get_yes_no_answer("Transpose these chord names to another scale tonic?"):
            print("\n\033[36m--- Transposition ---\033[0m")
            new_tonic, new_scale_data = ui.select_tonic_and_scale()
            if new_tonic and new_scale_data:
                transposed_chord_display_names = transpose_chord_names(gen_chord_names, selected_scale_tonic, new_tonic)
                if transposed_chord_display_names:
                    print(f"\n\033[32mChord names transposed to the tonic of {new_tonic}:\033[0m")
                    for degree, trans_name in transposed_chord_display_names.items():
                        print(f"  {degree.ljust(5)}: {trans_name}")

                    if get_yes_no_answer("Generate MIDI for these chords in the NEW key/scale?"):
                        # Regenerate MIDI notes for the new key, using original extension/inversion
                        trans_chord_names_actual, _, trans_midi_notes_actual, _ = \
                            chord_builder.generate_scale_chords(
                                new_tonic, new_scale_data,
                                selected_extension_lvl, selected_inversion_idx
                            )
                        if trans_chord_names_actual:
                            transposed_chords_for_midi: List[Dict[str, Any]] = []
                            # Use the same progression structure (degrees and durations) as the original
                            for original_prog_item_data in chords_for_midi_processing:
                                original_degree = original_prog_item_data["grado"]
                                original_duration = original_prog_item_data["duracion_beats"]
                                if original_degree in trans_chord_names_actual:
                                    transposed_chords_for_midi.append({
                                        "grado": original_degree,
                                        "nombre": trans_chord_names_actual[original_degree],
                                        "notas_midi": trans_midi_notes_actual[original_degree],
                                        "duracion_beats": original_duration
                                    })
                            if transposed_chords_for_midi:
                                sugg_trans_path = _generate_midi_filename_helper(new_tonic, new_scale_data, midi_export_default_dir, prefix="prog_TRANSP_")

                                trans_midi_fname_out = input(
                                    f"Enter transposed MIDI filename [default: {sugg_trans_path}]: ").strip()
                                if not trans_midi_fname_out:
                                    trans_midi_fname_out = sugg_trans_path
                                midi_builder.generate_midi_file(transposed_chords_for_midi, trans_midi_fname_out,
                                                                advanced_midi_opts)  # Reuse original MIDI options

        if not get_yes_no_answer("Perform another operation?"):
            print("\033[32mThank you for using the Advanced Chord Generator. Goodbye!\033[0m")
            break


if __name__ == "__main__":
    main()