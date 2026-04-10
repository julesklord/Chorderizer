import sys
from typing import Optional, Tuple, Dict, Any, Union
import colorama
from colorama import Fore, Style
from .theory_utils import MusicTheory


# -----------------------------------------------------------------------------
# UI Helper Functions
# -----------------------------------------------------------------------------
def print_welcome_message() -> None:
    print(f"{Fore.GREEN}Welcome to the Advanced Chord Generator!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Modularized Version 1.2.0{Style.RESET_ALL}")


def print_operation_cancelled() -> None:
    print(f"\n{Fore.RED}Operation cancelled by the user.{Style.RESET_ALL}")


def get_yes_no_answer(prompt: str) -> bool:
    while True:
        try:
            response = (
                input(f"{Fore.CYAN}{prompt} [y/N]: {Style.RESET_ALL}").strip().lower()
            )
            if not response:
                return False
            if response in ["yes", "y", "si", "s"]:
                return True
            if response in ["no", "n"]:
                return False
            print(
                f"{Fore.RED}Invalid response. Please enter 'y' or 'n'.{Style.RESET_ALL}"
            )
        except (EOFError, KeyboardInterrupt):
            print_operation_cancelled()
            sys.exit(0)


def get_numbered_option(
    prompt: str,
    options: Dict[Union[str, int], Any],
    allow_cancel: bool = True,
    cancel_key: str = "0",
) -> Optional[str]:
    print(f"\n{Fore.CYAN}{prompt}{Style.RESET_ALL}")
    display_options = {str(k): v for k, v in options.items()}

    for key_str, value in display_options.items():
        display_name = (
            value.get("name", value) if isinstance(value, dict) else str(value)
        )
        print(f"  {key_str}. {display_name}")

    if allow_cancel:
        print(f"  {cancel_key}. {Fore.RED}Cancel / Back{Style.RESET_ALL}")

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
                print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")
        except (EOFError, KeyboardInterrupt):
            print_operation_cancelled()
            return None


def get_chord_settings() -> Tuple[Optional[int], Optional[int]]:
    print(f"\n{Fore.CYAN}--- Chord Settings ---{Style.RESET_ALL}")
    extension_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5}
    extension_options = {
        "1": "Simple Triads",
        "2": "Sixths (or sevenths if 6th doesn't apply)",
        "3": "Sevenths (scale default)",
        "4": "Ninths",
        "5": "Elevenths (can sound dense!)",
        "6": "Thirteenths (can sound very dense!)",
    }
    ext_choice_key = get_numbered_option("Chord extension level:", extension_options)
    if ext_choice_key is None:
        return None, None
    selected_extension_level = extension_map[ext_choice_key]

    inversion_options = {
        "1": "Root Position",
        "2": "1st Inversion",
        "3": "2nd Inversion",
        "4": "3rd Inversion (for 7ths+)",
    }
    inv_choice_key = get_numbered_option("Chord inversion:", inversion_options)
    if inv_choice_key is None:
        return None, None
    selected_inversion = int(inv_choice_key) - 1
    return selected_extension_level, selected_inversion


def get_tablature_filter() -> str:
    tab_filter_options = {
        "1": "All tablatures",
        "2": "Only Minor chords (minor base quality)",
        "3": "Only chords with Seventh",
        "4": "Only chords with Ninth",
        "5": "Only Sixth chords (X6, Xm6)",
        "6": "Only chords with Eleventh",
        "7": "Only chords with Thirteenth",
        "8": "No tablatures",
    }
    choice = get_numbered_option(
        "--- Filter for Displaying Tablatures ---",
        tab_filter_options,
        allow_cancel=True,
    )
    return choice if choice is not None else "8"  # Default to None if cancelled


# -----------------------------------------------------------------------------
# Class UIManager: Manages console user interface
# -----------------------------------------------------------------------------
class UIManager:
    def __init__(self, theory: MusicTheory):
        self.theory = theory

    def select_tonic_and_scale(self) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        print(f"\n{Fore.CYAN}--- Select Scale Tonic ---{Style.RESET_ALL}")
        tonic_options = {
            str(i + 1): note for i, note in enumerate(self.theory.CHROMATIC_NOTES)
        }

        tonic_choice_key = get_numbered_option(
            "Tonic:", tonic_options, allow_cancel=True, cancel_key="0"
        )
        if tonic_choice_key is None:
            return None, None
        selected_tonic = tonic_options[tonic_choice_key]

        print(f"\n{Fore.CYAN}--- Select Scale Type ---{Style.RESET_ALL}")
        scale_choice_key = get_numbered_option(
            "Scale Type:",
            self.theory.AVAILABLE_SCALES,
            allow_cancel=True,
            cancel_key="0",
        )
        if scale_choice_key is None:
            return None, None

        selected_scale_info = self.theory.AVAILABLE_SCALES[scale_choice_key]
        full_scale_tonic_name = selected_tonic + selected_scale_info["tonic_suffix"]
        return full_scale_tonic_name, selected_scale_info

    def get_advanced_midi_options(self) -> Dict[str, Any]:
        print(f"\n{Fore.CYAN}--- Advanced MIDI Options ---{Style.RESET_ALL}")
        options = {
            "bpm": 120,
            "base_velocity": 70,
            "velocity_randomization_range": 0,
            "chord_instrument": 0,
            "add_bass_track": False,
            "bass_instrument": 33,  # Acoustic Bass
            "arpeggio_style": None,
            "arpeggio_note_duration_beats": 0.25,
            "strum_delay_ms": 0,
        }

        try:
            bpm_in = input(
                f"BPM (tempo) for MIDI [default: {options['bpm']}]: "
            ).strip()
            if bpm_in:
                options["bpm"] = int(bpm_in)
            if not (20 <= options["bpm"] <= 300):  # Reasonable range
                print(
                    f"{Fore.YELLOW}Warning: BPM {options['bpm']} is outside the typical range (20-300).{Style.RESET_ALL}"
                )
            if options["bpm"] <= 0:
                options["bpm"] = 120  # Fallback
        except ValueError:
            print(f"{Fore.RED}Invalid BPM, using {options['bpm']}.{Style.RESET_ALL}")

        try:
            vel_in = input(
                f"Base note velocity (0-127) [default: {options['base_velocity']}]: "
            ).strip()
            if vel_in:
                options["base_velocity"] = int(vel_in)
            options["base_velocity"] = max(0, min(127, options["base_velocity"]))
        except ValueError:
            print(
                f"{Fore.RED}Invalid velocity, using {options['base_velocity']}.{Style.RESET_ALL}"
            )

        if get_yes_no_answer("Add slight randomization to velocity?"):
            try:
                rand_in = input(f"Randomization range (+/-) [default: 5]: ").strip()
                if rand_in:
                    options["velocity_randomization_range"] = int(rand_in)
                options["velocity_randomization_range"] = max(
                    0, min(20, options["velocity_randomization_range"])
                )
            except ValueError:
                print(f"{Fore.RED}Invalid range, using 0.{Style.RESET_ALL}")

        chord_instr_key = get_numbered_option(
            "Instrument for chords:", self.theory.MIDI_PROGRAMS, allow_cancel=False
        )  # Must select an instrument
        options["chord_instrument"] = int(chord_instr_key)

        options["add_bass_track"] = get_yes_no_answer("Add bass track (root notes)?")
        if options["add_bass_track"]:
            bass_instr_key = get_numbered_option(
                "Instrument for bass:", self.theory.MIDI_PROGRAMS, allow_cancel=False
            )
            options["bass_instrument"] = int(bass_instr_key)

        if get_yes_no_answer(
            "Arpeggiate chords? (Otherwise, they will be block chords)"
        ):
            arp_styles = {"1": "up", "2": "down", "3": "updown"}
            style_key = get_numbered_option("Arpeggio style:", arp_styles)
            if style_key:
                options["arpeggio_style"] = arp_styles[style_key]
                try:
                    arp_dur_in = input(
                        f"Duration of each arpeggio note in beats [default: {options['arpeggio_note_duration_beats']}]: "
                    ).strip()
                    if arp_dur_in:
                        options["arpeggio_note_duration_beats"] = float(arp_dur_in)
                    if options["arpeggio_note_duration_beats"] <= 0:
                        options["arpeggio_note_duration_beats"] = 0.25
                except ValueError:
                    print(
                        f"{Fore.RED}Invalid arpeggio note duration, using {options['arpeggio_note_duration_beats']}.{Style.RESET_ALL}"
                    )

        if not options["arpeggio_style"] and get_yes_no_answer(
            "Add strumming effect to block chords?"
        ):
            try:
                strum_in = input(
                    f"Strum delay between notes (milliseconds) [default: 15ms]: "
                ).strip()
                if strum_in:
                    options["strum_delay_ms"] = int(strum_in)
                options["strum_delay_ms"] = max(
                    0, min(100, options["strum_delay_ms"])
                )  # Cap delay
            except ValueError:
                print(f"{Fore.RED}Invalid strum delay, using 0.{Style.RESET_ALL}")

        options["voice_leading"] = get_yes_no_answer(
            "Apply voice leading? (smooth note motion between chords)"
        )

        return options
