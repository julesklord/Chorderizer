import os
import random # Keep for now, might be used in main logic not yet fully reviewed
from typing import List, Dict, Tuple, Optional, Any, Union # Keep Union for transpose_chord_names if needed

# Imports from new modules
from .theory_utils import MusicTheory, MusicTheoryUtils
from .ui import (
    UIManager,
    print_welcome_message,
    print_operation_cancelled, # Added as it's used in get_numbered_option, which might be used in main
    get_yes_no_answer,
    get_numbered_option, # Though UIManager uses it, main might call it directly too
    get_chord_settings,
    get_tablature_filter
)
from .generators import ChordGenerator, TablatureGenerator, MidiGenerator

# Mido imports are primarily in generators.py now.
# If main() itself directly manipulates mido objects, some might be needed here.
# For now, assuming they are encapsulated in MidiGenerator.


# -----------------------------------------------------------------------------
# Chord Transposition Function (Remains in chorderizer.py for now)
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
# Main Program Logic (Remains in chorderizer.py)
# -----------------------------------------------------------------------------
def _generate_midi_filename_helper(tonic: str, scale_info: Dict[str, Any], base_dir: str, prefix: str = "prog_") -> str:
    safe_tonic = tonic.replace('#', 'sharp').replace('b', 'flat')
    safe_scale_name = scale_info['name'].replace(' ', '_').replace('(', '').replace(')', '')
    filename = f"{prefix}{safe_tonic}_{safe_scale_name}.mid"
    return os.path.join(base_dir, filename)


def main():
    theory = MusicTheory()
    ui = UIManager(theory) # UIManager now imported
    chord_builder = ChordGenerator(theory) # ChordGenerator now imported
    tab_builder = TablatureGenerator(theory) # TablatureGenerator now imported
    midi_builder = MidiGenerator(theory) # MidiGenerator now imported

    print_welcome_message() # Imported from ui.py
    home_directory = os.path.expanduser("~")
    midi_export_default_dir = os.path.join(home_directory, "chord_generator_midi_exports")

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

        tab_display_filter_key = get_tablature_filter()

        for degree, chord_name_display in gen_chord_names.items():
            base_qual = gen_base_qualities.get(degree)
            color_code = "\033[32m"
            if base_qual == "minor":
                color_code = "\033[34m"
            elif base_qual == "diminished" or "ø" in chord_name_display or "m7b5" in chord_name_display:
                color_code = "\033[35m"
            elif base_qual == "augmented" or "+" in chord_name_display:
                color_code = "\033[33m"
            reset_color_code = "\033[0m"

            note_names_str = ", ".join(gen_note_names.get(degree, []))
            midi_notes_str = ", ".join(map(str, gen_midi_notes.get(degree, [])))
            print(
                f"  {degree.ljust(5)}: {color_code}{chord_name_display.ljust(15)}{reset_color_code} "
                f"(Notes: {note_names_str.ljust(25)}) (MIDI: {midi_notes_str})")

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
                    if chord_name_display.endswith("6") and not chord_name_display.endswith("m7b6"):
                        show_this_tab = True
                elif tab_display_filter_key == "6" and "11" in chord_name_display:
                    show_this_tab = True
                elif tab_display_filter_key == "7" and "13" in chord_name_display:
                    show_this_tab = True

            if show_this_tab and gen_midi_notes.get(degree):
                tab_lines_list = tab_builder.generate_simple_tab(chord_name_display, gen_midi_notes[degree])
                for tab_line in tab_lines_list:
                    print(f"    {tab_line}")

        print("\n\033[36m--- MIDI Generation Options ---\033[0m")
        chords_for_midi_processing: List[Dict[str, Any]] = []
        if get_yes_no_answer( # Imported from ui.py
                "Define a chord progression for MIDI? (If no, all diatonic chords will be used sequentially)"):
            progression_input_str = input(
                "Enter progression (degrees separated by '-', e.g., I-V-vi-IV). "
                "Optional duration in beats (e.g., I:4-V:2-vi:2-IV:4 ): "
            ).strip().upper()
            progression_items = progression_input_str.split('-')
            for item_str in progression_items:
                item_str = item_str.strip()
                if not item_str: continue

                current_prog_degree, current_beats_duration = item_str, 4.0
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
        else:
            for degree_key in selected_scale_info["degrees"].keys():
                if degree_key in gen_chord_names:
                    chords_for_midi_processing.append({
                        "grado": degree_key,
                        "nombre": gen_chord_names[degree_key],
                        "notas_midi": gen_midi_notes[degree_key],
                        "duracion_beats": 2.0
                    })

        if not chords_for_midi_processing:
            print("\033[31mNo chords selected for MIDI processing.\033[0m")
            continue

        advanced_midi_opts = ui.get_advanced_midi_options()

        suggested_midi_path = _generate_midi_filename_helper(selected_scale_tonic, selected_scale_info, midi_export_default_dir)

        output_midi_filename = input(f"Enter MIDI filename [default: {suggested_midi_path}]: ").strip()
        if not output_midi_filename:
            output_midi_filename = suggested_midi_path

        midi_builder.generate_midi_file(chords_for_midi_processing, output_midi_filename, advanced_midi_opts)

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
                        trans_chord_names_actual, _, trans_midi_notes_actual, _ = \
                            chord_builder.generate_scale_chords(
                                new_tonic, new_scale_data,
                                selected_extension_lvl, selected_inversion_idx
                            )
                        if trans_chord_names_actual:
                            transposed_chords_for_midi: List[Dict[str, Any]] = []
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
                                                                advanced_midi_opts)

        if not get_yes_no_answer("Perform another operation?"):
            print("\033[32mThank you for using the Advanced Chord Generator. Goodbye!\033[0m")
            break


if __name__ == "__main__":
    main()