import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from chorderizer.theory_utils import MusicTheory
from chorderizer.generators import MidiGenerator

theory = MusicTheory()
midi_gen = MidiGenerator(theory)

# ii-V-I en C Mayor (7mas)
prog = [
    {
        "grado": "ii",
        "nombre": "Dm7",
        "notas_midi": [50, 53, 57, 60],
        "duracion_beats": 4.0,
    },
    {
        "grado": "V",
        "nombre": "G7",
        "notas_midi": [43, 47, 50, 53],
        "duracion_beats": 4.0,
    },
    {
        "grado": "I",
        "nombre": "Cmaj7",
        "notas_midi": [48, 52, 55, 59],
        "duracion_beats": 4.0,
    },
]

# Mini options (now safe with .get() in the library)
opts_off = {"voice_leading": False}
opts_on = {"voice_leading": True}

# Generar ambos en la carpeta de ejecución
try:
    midi_gen.generate_midi_file(prog, "ii-V-I_NO_leading.mid", opts_off)
    midi_gen.generate_midi_file(prog, "ii-V-I_WITH_leading.mid", opts_on)
    print("¡Archivos generados con éxito!")
    print(f"Directorio: {os.getcwd()}")
    print("1. ii-V-I_NO_leading.mid  (Saltos estándar)")
    print("2. ii-V-I_WITH_leading.mid (Conducción de voces suave)")
except Exception as e:
    import traceback

    print(f"Error: {e}")
    traceback.print_exc()
