from typing import Optional, Tuple, Dict, Any, Union # Union was in the original get_numbered_option
from .theory_utils import MusicTheory # Mapping was also used but not defined here, let's use Dict for now.

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
