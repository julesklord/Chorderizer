import os
import sys

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

from chorderizer.theory_utils import MusicTheory
from chorderizer.generators import ChordGenerator, MidiGenerator


def verify():
    theory = MusicTheory()
    chord_gen = ChordGenerator(theory)
    midi_gen = MidiGenerator(theory)

    # 1. Test Chord Generation
    scale_info = theory.AVAILABLE_SCALES["1"]  # Major
    tonic = "C"

    print("Testing chord generation...")
    chords, names, midis, quals = chord_gen.generate_scale_chords(
        tonic, scale_info, extension_level=2, inversion=1
    )

    assert "I" in chords
    assert names["I"] == [
        "E",
        "G",
        "B",
        "C",
    ]  # First inversion of Cmaj7 (C E G B) -> (E G B C)
    print("Chord generation (inversion 1) OK")

    # 2. Test MIDI Generation (headless)
    print("Testing MIDI generation...")
    chords_to_process = [
        {
            "grado": "I",
            "nombre": chords["I"],
            "notas_midi": midis["I"],
            "duracion_beats": 4.0,
        }
    ]

    midi_opts = {
        "bpm": 120,
        "chord_instrument": 1,
        "add_bass_track": True,
        "bass_instrument": 33,
        "base_velocity": 80,
        "velocity_randomization_range": 10,
        "arpeggio_style": None,
        "strum_delay_ms": 20,
    }

    output_path = "scratch/test_output.mid"
    os.makedirs("scratch", exist_ok=True)

    try:
        midi_gen.generate_midi_file(chords_to_process, output_path, midi_opts)
        print(f"MIDI generation OK. Saved to {output_path}")
    except Exception as e:
        print(f"MIDI generation FAILED: {e}")
        return

    print("Verification complete!")


if __name__ == "__main__":
    verify()
