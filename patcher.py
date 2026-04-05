import re

with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()

# Replace def main() with def run_interactive(...)
text = text.replace("def main():", "def run_interactive(theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir):")

# In the original file, the lines right after def main() initialize things:
#     # Initialize colorama for cross-platform color support
#     colorama.init()
#
#     theory = MusicTheory()
#     ui = UIManager(theory)
#     chord_builder = ChordGenerator(theory)
#     tab_builder = TablatureGenerator(theory)
#     midi_builder = MidiGenerator(theory)
#
#     print_welcome_message()
#     home_directory = os.path.expanduser("~")
#     # Improved directory creation logic is handled inside MidiGenerator.generate_midi_file
#     midi_export_default_dir = os.path.join(home_directory, "chord_generator_midi_exports")

# We want to remove this initialization from `run_interactive`
init_str = """    # Initialize colorama for cross-platform color support
    colorama.init()

    theory = MusicTheory()
    ui = UIManager(theory)
    chord_builder = ChordGenerator(theory)
    tab_builder = TablatureGenerator(theory)
    midi_builder = MidiGenerator(theory)

    print_welcome_message()
    home_directory = os.path.expanduser("~")
    # Improved directory creation logic is handled inside MidiGenerator.generate_midi_file
    midi_export_default_dir = os.path.join(home_directory, "chord_generator_midi_exports")"""

text = text.replace(init_str, "    pass")

# Now append CLI logic and a new main() at the bottom
new_bottom = """
def run_cli(args, theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir):
    tonic = args.tonic.capitalize() if args.tonic else 'C'
    scale_type_map = {
        "major": "1", "natural_minor": "2", "harmonic_minor": "3", "melodic_minor": "4",
        "major_pentatonic": "5", "minor_pentatonic": "6"
    }

    scale_key = scale_type_map.get(args.scale.lower() if args.scale else "major", "1")
    if scale_key not in theory.SCALES:
        print(f"\\033[31mInvalid scale type.\\033[0m")
        return

    scale_info = theory.SCALES[scale_key]
    extension = int(args.extension)
    inversion = int(args.inversion)

    gen_chord_names, gen_note_names, gen_midi_notes, gen_base_qualities = \\
        chord_builder.generate_scale_chords(tonic, scale_info, extension, inversion)

    if not gen_chord_names:
        print(f"\\033[31mCould not generate chords for {tonic}.\\033[0m")
        return

    print(f"\\n{Fore.GREEN}Chords generated for the scale of {tonic} ({scale_info['name']}):{Style.RESET_ALL}")

    for degree, chord_name_display in gen_chord_names.items():
        base_qual = gen_base_qualities.get(degree)
        color_code = Fore.GREEN
        if base_qual == "minor":
            color_code = Fore.BLUE
        elif base_qual == "diminished" or "ø" in chord_name_display or "m7b5" in chord_name_display:
            color_code = Fore.MAGENTA
        elif base_qual == "augmented" or "+" in chord_name_display:
            color_code = Fore.YELLOW

        note_names_str = ", ".join(gen_note_names.get(degree, []))
        midi_notes_str = ", ".join(map(str, gen_midi_notes.get(degree, [])))
        print(
            f"  {degree.ljust(5)}: {color_code}{chord_name_display.ljust(15)}{Style.RESET_ALL} "
            f"(Notes: {note_names_str.ljust(25)}) (MIDI: {midi_notes_str})")

    chords_for_midi_processing = []

    if args.progression:
        progression_items = args.progression.upper().split('-')
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
                    print(f"\\033[31mInvalid duration for '{current_prog_degree}', using 4.0 beats.\\033[0m")

            if current_prog_degree in gen_chord_names:
                chords_for_midi_processing.append({
                    "grado": current_prog_degree,
                    "nombre": gen_chord_names[current_prog_degree],
                    "notas_midi": gen_midi_notes[current_prog_degree],
                    "duracion_beats": current_beats_duration
                })
            else:
                print(f"\\033[31mDegree '{current_prog_degree}' not found in generated chords. Skipping.\\033[0m")
    else:
        for degree_key in scale_info["degrees"].keys():
            if degree_key in gen_chord_names:
                chords_for_midi_processing.append({
                    "grado": degree_key,
                    "nombre": gen_chord_names[degree_key],
                    "notas_midi": gen_midi_notes[degree_key],
                    "duracion_beats": 2.0
                })

    if not chords_for_midi_processing:
        print("\\033[31mNo chords selected for MIDI processing.\\033[0m")
        return

    # Basic defaults for CLI args
    advanced_midi_opts = {
        'bpm': 120,
        'base_velocity': 80,
        'humanize_velocity': True,
        'instrument_chords': 0,
        'add_bass': True,
        'instrument_bass': 33,
        'bass_velocity': 90,
        'arpeggio_style': 'none',
        'strum_delay': 0.0
    }

    output_path = args.output
    if not output_path:
        output_path = _generate_midi_filename_helper(tonic, scale_info, midi_export_default_dir)

    midi_builder.generate_midi_file(chords_for_midi_processing, output_path, advanced_midi_opts)
    print(f"\\n\\033[32mMIDI successfully generated to {output_path}\\033[0m")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Chorderizer: Advanced Chord Generator & MIDI Exporter")
    parser.add_argument('--tonic', type=str, help="Tonic note (e.g. C, D#, Gb)")
    parser.add_argument('--scale', type=str, choices=["major", "natural_minor", "harmonic_minor", "melodic_minor", "major_pentatonic", "minor_pentatonic"], help="Scale type")
    parser.add_argument('--extension', type=int, choices=[1, 2, 3, 4, 5, 6], default=3, help="Extension level (1: Triads, 3: 7ths, etc.)")
    parser.add_argument('--inversion', type=int, choices=[0, 1, 2, 3], default=0, help="Inversion (0: Root, 1: First, etc.)")
    parser.add_argument('--progression', type=str, help="Chord progression (e.g. I-V-vi-IV or I:4-V:2-vi:2-IV:4)")
    parser.add_argument('--output', type=str, help="Output MIDI file path")

    args, unknown = parser.parse_known_args()

    colorama.init()
    theory = MusicTheory()
    ui = UIManager(theory)
    chord_builder = ChordGenerator(theory)
    tab_builder = TablatureGenerator(theory)
    midi_builder = MidiGenerator(theory)

    home_directory = os.path.expanduser("~")
    midi_export_default_dir = os.path.join(home_directory, "chord_generator_midi_exports")

    if args.tonic or args.scale or args.progression:
        if not args.tonic or not args.scale:
            print("Error: Both --tonic and --scale are required in CLI mode.")
            sys.exit(1)
        run_cli(args, theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir)
    else:
        print_welcome_message()
        run_interactive(theory, ui, chord_builder, tab_builder, midi_builder, midi_export_default_dir)
"""

text = text.replace('if __name__ == "__main__":', new_bottom + '\nif __name__ == "__main__":')

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)
