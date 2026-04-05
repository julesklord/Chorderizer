import os
from typing import Any, Dict, List

import colorama
from colorama import Fore, Style

from .generators import ChordGenerator, MidiGenerator, TablatureGenerator
# Imports from new modules
from .theory_utils import MusicTheory, MusicTheoryUtils
from .ui import (UIManager, get_chord_settings, get_tablature_filter,
                 get_yes_no_answer, print_welcome_message)

# Mido imports are primarily in generators.py now.
# If main() itself directly manipulates mido objects, some might be needed here.
# For now, assuming they are encapsulated in MidiGenerator.


# Transposition logic moved to theory_utils.py


# -----------------------------------------------------------------------------
# Main Program Logic (Remains in chorderizer.py)
# -----------------------------------------------------------------------------
def _generate_midi_filename_helper(
    tonic: str, scale_info: Dict[str, Any], base_dir: str, prefix: str = "prog_"
) -> str:
    # Cleaner filename: keep the b/sharp symbols but make them filename-safe if needed
    # or use 'b' and '#' directly as most modern OS handle them fine.
    # Let's keep it simple and clean.
    clean_tonic = tonic.replace(" ", "_")
    safe_scale_name = (
        scale_info["name"].replace(" ", "_").replace("(", "").replace(")", "")
    )
    filename = f"{prefix}{clean_tonic}_{safe_scale_name}.mid"
    return os.path.join(base_dir, filename)


def run_interactive(
    theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir
):
    pass

    while True:
        print("\n" + "=" * 70)
        selected_scale_tonic, selected_scale_info = ui.select_tonic_and_scale()
        if selected_scale_tonic is None or selected_scale_info is None:
            print("\033[32mExiting program.\033[0m")
            break

        # get_chord_settings and get_tablature_filter are imported from ui.py
        chord_settings_tuple = get_chord_settings()
        if chord_settings_tuple is None:
            continue  # User cancelled
        selected_extension_lvl, selected_inversion_idx = chord_settings_tuple

        # Generate chords for the selected scale
        gen_chord_names, gen_note_names, gen_midi_notes, gen_base_qualities = (
            chord_builder.generate_scale_chords(
                selected_scale_tonic,
                selected_scale_info,
                selected_extension_lvl,
                selected_inversion_idx,
            )
        )

        if not gen_chord_names:
            print(
                f"\033[31mCould not generate chords for {selected_scale_tonic}.\033[0m"
            )
            continue

        print(
            f"\n{Fore.GREEN}Chords generated for the scale of {selected_scale_tonic} ({selected_scale_info['name']}):{Style.RESET_ALL}"
        )

        tab_display_filter_key = get_tablature_filter()

        for degree, chord_name_display in gen_chord_names.items():
            base_qual = gen_base_qualities.get(degree)
            color_code = Fore.GREEN
            if base_qual == "minor":
                color_code = Fore.BLUE
            elif (
                base_qual == "diminished"
                or "ø" in chord_name_display
                or "m7b5" in chord_name_display
            ):
                color_code = Fore.MAGENTA
            elif base_qual == "augmented" or "+" in chord_name_display:
                color_code = Fore.YELLOW

            note_names_str = ", ".join(gen_note_names.get(degree, []))
            midi_notes_str = ", ".join(map(str, gen_midi_notes.get(degree, [])))
            print(
                f"  {degree.ljust(5)}: {color_code}{chord_name_display.ljust(15)}{Style.RESET_ALL} "
                f"(Notes: {note_names_str.ljust(25)}) (MIDI: {midi_notes_str})"
            )

            show_this_tab = False
            if tab_display_filter_key == "8":
                pass
            elif tab_display_filter_key == "1":
                show_this_tab = True
            else:
                if tab_display_filter_key == "2" and base_qual == "minor":
                    show_this_tab = True
                elif tab_display_filter_key == "3" and "7" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "4" and "9" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "5":
                    if chord_name_display.endswith(
                        "6"
                    ) and not chord_name_display.endswith("m7b6"):
                        show_this_tab = True
                elif tab_display_filter_key == "6" and "11" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "7" and "13" in chord_name_display:
                    show_this_tab = True

            if show_this_tab and gen_midi_notes.get(degree):
                tab_lines_list = tab_builder.generate_simple_tab(
                    chord_name_display, gen_midi_notes[degree]
                )
                for tab_line in tab_lines_list:
                    print(f"    {tab_line}")

        print("\n\033[36m--- MIDI Generation Options ---\033[0m")
        chords_for_midi_processing: List[Dict[str, Any]] = []
        if get_yes_no_answer(  # Imported from ui.py
            "Define a chord progression for MIDI? (If no, all diatonic chords will be used sequentially)"
        ):
            progression_input_str = (
                input(
                    "Enter progression (degrees separated by '-', e.g., I-V-vi-IV). "
                    "Optional duration in beats (e.g., I:4-V:2-vi:2-IV:4 ): "
                )
                .strip()
                .upper()
            )
            progression_items = progression_input_str.split("-")
            for item_str in progression_items:
                item_str = item_str.strip()
                if not item_str:
                    continue

                current_prog_degree, current_beats_duration = item_str, 4.0
                if ":" in item_str:
                    parts = item_str.split(":", 1)
                    current_prog_degree = parts[0].strip()
                    try:
                        current_beats_duration = float(parts[1].strip())
                        if current_beats_duration <= 0:
                            current_beats_duration = 4.0
                    except ValueError:
                        print(
                            f"\033[31mInvalid duration for '{current_prog_degree}', using 4.0 beats.\033[0m"
                        )

                if current_prog_degree in gen_chord_names:
                    chords_for_midi_processing.append(
                        {
                            "grado": current_prog_degree,
                            "nombre": gen_chord_names[current_prog_degree],
                            "notas_midi": gen_midi_notes[current_prog_degree],
                            "duracion_beats": current_beats_duration,
                        }
                    )
                else:
                    print(
                        f"\033[31mDegree '{current_prog_degree}' not found in generated chords. Skipping.\033[0m"
                    )
        else:
            for degree_key in selected_scale_info["degrees"].keys():
                if degree_key in gen_chord_names:
                    chords_for_midi_processing.append(
                        {
                            "grado": degree_key,
                            "nombre": gen_chord_names[degree_key],
                            "notas_midi": gen_midi_notes[degree_key],
                            "duracion_beats": 2.0,
                        }
                    )

        if not chords_for_midi_processing:
            print("\033[31mNo chords selected for MIDI processing.\033[0m")
            continue

        advanced_midi_opts = ui.get_advanced_midi_options()

        suggested_midi_path = _generate_midi_filename_helper(
            selected_scale_tonic, selected_scale_info, midi_export_default_dir
        )

        output_midi_filename = input(
            f"Enter MIDI filename [default: {suggested_midi_path}]: "
        ).strip()
        if not output_midi_filename:
            output_midi_filename = suggested_midi_path

        midi_builder.generate_midi_file(
            chords_for_midi_processing, output_midi_filename, advanced_midi_opts
        )

        if get_yes_no_answer("Transpose these chord names to another scale tonic?"):
            print(f"\n{Fore.CYAN}--- Transposition ---{Style.RESET_ALL}")
            new_tonic, new_scale_data = ui.select_tonic_and_scale()
            if new_tonic and new_scale_data:
                transposed_chord_display_names = MusicTheoryUtils.transpose_chords(
                    gen_chord_names, selected_scale_tonic, new_tonic
                )
                if transposed_chord_display_names:
                    print(
                        f"\n{Fore.GREEN}Chord names transposed to the tonic of {new_tonic}:{Style.RESET_ALL}"
                    )
                    for degree, trans_name in transposed_chord_display_names.items():
                        print(f"  {degree.ljust(5)}: {trans_name}")

                    if get_yes_no_answer(
                        "Generate MIDI for these chords in the NEW key/scale?"
                    ):
                        trans_chord_names_actual, _, trans_midi_notes_actual, _ = (
                            chord_builder.generate_scale_chords(
                                new_tonic,
                                new_scale_data,
                                selected_extension_lvl,
                                selected_inversion_idx,
                            )
                        )
                        if trans_chord_names_actual:
                            transposed_chords_for_midi: List[Dict[str, Any]] = []
                            for original_prog_item_data in chords_for_midi_processing:
                                original_degree = original_prog_item_data["grado"]
                                original_duration = original_prog_item_data[
                                    "duracion_beats"
                                ]
                                if original_degree in trans_chord_names_actual:
                                    transposed_chords_for_midi.append(
                                        {
                                            "grado": original_degree,
                                            "nombre": trans_chord_names_actual[
                                                original_degree
                                            ],
                                            "notas_midi": trans_midi_notes_actual[
                                                original_degree
                                            ],
                                            "duracion_beats": original_duration,
                                        }
                                    )
                            if transposed_chords_for_midi:
                                sugg_trans_path = _generate_midi_filename_helper(
                                    new_tonic,
                                    new_scale_data,
                                    midi_export_default_dir,
                                    prefix="prog_TRANSP_",
                                )

                                trans_midi_fname_out = input(
                                    f"Enter transposed MIDI filename [default: {sugg_trans_path}]: "
                                ).strip()
                                if not trans_midi_fname_out:
                                    trans_midi_fname_out = sugg_trans_path
                                midi_builder.generate_midi_file(
                                    transposed_chords_for_midi,
                                    trans_midi_fname_out,
                                    advanced_midi_opts,
                                )

        if not get_yes_no_answer("Perform another operation?"):
            print(
                f"{Fore.GREEN}Thank you for using the Advanced Chord Generator. Goodbye!{Style.RESET_ALL}"
            )
            break


def run_cli(
    args, theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir
):
    tonic = args.tonic.capitalize() if args.tonic else "C"
    scale_type_map = {
        "major": "1",
        "natural_minor": "2",
        "harmonic_minor": "3",
        "melodic_minor": "4",
        "major_pentatonic": "5",
        "minor_pentatonic": "6",
    }

    scale_key = scale_type_map.get(args.scale.lower() if args.scale else "major", "1")
    if scale_key not in theory.SCALES:
        print("\033[31mInvalid scale type.\033[0m")
        return

    scale_info = theory.SCALES[scale_key]
    extension = int(args.extension)
    inversion = int(args.inversion)

    gen_chord_names, gen_note_names, gen_midi_notes, gen_base_qualities = (
        chord_builder.generate_scale_chords(tonic, scale_info, extension, inversion)
    )

    if not gen_chord_names:
        print(f"\033[31mCould not generate chords for {tonic}.\033[0m")
        return

    print(
        f"\n{Fore.GREEN}Chords generated for the scale of {tonic} ({scale_info['name']}):{Style.RESET_ALL}"
    )

    for degree, chord_name_display in gen_chord_names.items():
        base_qual = gen_base_qualities.get(degree)
        color_code = Fore.GREEN
        if base_qual == "minor":
            color_code = Fore.BLUE
        elif (
            base_qual == "diminished"
            or "ø" in chord_name_display
            or "m7b5" in chord_name_display
        ):
            color_code = Fore.MAGENTA
        elif base_qual == "augmented" or "+" in chord_name_display:
            color_code = Fore.YELLOW

        note_names_str = ", ".join(gen_note_names.get(degree, []))
        midi_notes_str = ", ".join(map(str, gen_midi_notes.get(degree, [])))
        print(
            f"  {degree.ljust(5)}: {color_code}{chord_name_display.ljust(15)}{Style.RESET_ALL} "
            f"(Notes: {note_names_str.ljust(25)}) (MIDI: {midi_notes_str})"
        )

    chords_for_midi_processing = []

    if args.progression:
        progression_items = args.progression.upper().split("-")
        for item_str in progression_items:
            item_str = item_str.strip()
            if not item_str:
                continue

            current_prog_degree, current_beats_duration = item_str, 4.0
            if ":" in item_str:
                parts = item_str.split(":", 1)
                current_prog_degree = parts[0].strip()
                try:
                    current_beats_duration = float(parts[1].strip())
                    if current_beats_duration <= 0:
                        current_beats_duration = 4.0
                except ValueError:
                    print(
                        f"\033[31mInvalid duration for '{current_prog_degree}', using 4.0 beats.\033[0m"
                    )

            if current_prog_degree in gen_chord_names:
                chords_for_midi_processing.append(
                    {
                        "grado": current_prog_degree,
                        "nombre": gen_chord_names[current_prog_degree],
                        "notas_midi": gen_midi_notes[current_prog_degree],
                        "duracion_beats": current_beats_duration,
                    }
                )
            else:
                print(
                    f"\033[31mDegree '{current_prog_degree}' not found in generated chords. Skipping.\033[0m"
                )
    else:
        for degree_key in scale_info["degrees"].keys():
            if degree_key in gen_chord_names:
                chords_for_midi_processing.append(
                    {
                        "grado": degree_key,
                        "nombre": gen_chord_names[degree_key],
                        "notas_midi": gen_midi_notes[degree_key],
                        "duracion_beats": 2.0,
                    }
                )

    if not chords_for_midi_processing:
        print("\033[31mNo chords selected for MIDI processing.\033[0m")
        return

    # Basic defaults for CLI args
    advanced_midi_opts = {
        "bpm": 120,
        "base_velocity": 80,
        "humanize_velocity": True,
        "instrument_chords": 0,
        "add_bass": True,
        "instrument_bass": 33,
        "bass_velocity": 90,
        "arpeggio_style": "none",
        "strum_delay": 0.0,
    }

    output_path = args.output
    if not output_path:
        output_path = _generate_midi_filename_helper(
            tonic, scale_info, midi_export_default_dir
        )

    midi_builder.generate_midi_file(
        chords_for_midi_processing, output_path, advanced_midi_opts
    )
    print(f"\n\033[32mMIDI successfully generated to {output_path}\033[0m")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Chorderizer: Advanced Chord Generator & MIDI Exporter"
    )
    parser.add_argument("--tonic", type=str, help="Tonic note (e.g. C, D#, Gb)")
    parser.add_argument(
        "--scale",
        type=str,
        choices=[
            "major",
            "natural_minor",
            "harmonic_minor",
            "melodic_minor",
            "major_pentatonic",
            "minor_pentatonic",
        ],
        help="Scale type",
    )
    parser.add_argument(
        "--extension",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        default=3,
        help="Extension level (1: Triads, 3: 7ths, etc.)",
    )
    parser.add_argument(
        "--inversion",
        type=int,
        choices=[0, 1, 2, 3],
        default=0,
        help="Inversion (0: Root, 1: First, etc.)",
    )
    parser.add_argument(
        "--progression",
        type=str,
        help="Chord progression (e.g. I-V-vi-IV or I:4-V:2-vi:2-IV:4)",
    )
    parser.add_argument("--output", type=str, help="Output MIDI file path")

    args, unknown = parser.parse_known_args()

    colorama.init()
    theory = MusicTheory()
    ui = UIManager(theory)
    chord_builder = ChordGenerator(theory)
    tab_builder = TablatureGenerator(theory)
    midi_builder = MidiGenerator(theory)

    home_directory = os.path.expanduser("~")
    midi_export_default_dir = os.path.join(
        home_directory, "chord_generator_midi_exports"
    )

    if args.tonic or args.scale or args.progression:
        if not args.tonic or not args.scale:
            print("Error: Both --tonic and --scale are required in CLI mode.")
            exit(1)
        run_cli(
            args,
            theory,
            ui,
            chord_builder,
            tab_builder,
            midi_builder,
            midi_export_default_dir,
        )
    else:
        print_welcome_message()
        run_interactive(
            theory,
            ui,
            chord_builder,
            tab_builder,
            midi_builder,
            midi_export_default_dir,
        )


if __name__ == "__main__":
    main()
