import os
import random
from typing import List, Dict, Tuple, Optional, Any

from mido import MidiFile, MidiTrack, Message, bpm2tempo, MetaMessage

from .theory_utils import MusicTheory, MusicTheoryUtils

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
