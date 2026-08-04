<table border="0">
  <tr>
    <td width="200" align="center" valign="top">
      <img src="docs/wiki/assets/logo.svg" width="180" alt="Chorderizer logo">
    </td>
    <td valign="top">
      <h1>Chorderizer</h1>
      <p><strong>Chord Orchestration & MIDI Analysis Dashboard</strong><br/>
      <em>Terminal-native workstation for harmonic analysis.</em></p>
      <p>
        <a href="https://badge.fury.io/py/chorderizer"><img src="https://badge.fury.io/py/chorderizer.svg" alt="PyPI version"></a>
        <a href="LICENSE.md"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
        <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
        <a href="https://textual.textualize.io/"><img src="https://img.shields.io/badge/framework-Textual-0094d2.svg" alt="Framework: Textual"></a>
      </p>
    </td>
  </tr>
</table>

---

<p align="center">
  <img src="docs/wiki/assets/demo.gif" alt="Chorderizer Dashboard Overview" width="900" />
</p>

---

## Overview

Chorderizer provides an interactive TUI dashboard for chord progression prototyping. It ensures adherence to diatonic principles and ergonomic voice leading.

## Scope

Chorderizer supports:
- Harmonic exploration for composers and producers.
- Diatonic and modal chord generation.
- MIDI export and tablature support.
- Terminal-based workflows using Textual.

It does not support:
- DAW functionality.
- General-purpose notation editing.
- Custom guitar fingering or non-standard tunings.
- Non-Western microtonal scales.
- Plugin hosting or real-time MIDI routing.

## Capabilities

### Harmonic Engine

The engine supports 11 scales for Western and contemporary harmony:
- **Diatonic**: Major (Ionian), Natural Minor (Aeolian).
- **Modes**: Dorian, Phrygian, Lydian, Mixolydian, Locrian.
- **Advanced**: Harmonic Minor, Melodic Minor (Ascending).
- **Pentatonic**: Major and Minor variations.

### TUI Dashboard

The interface uses the Textual framework for real-time visualization:
- **Piano Visualizer**: 2-octave keyboard rendering active MIDI notes.
- **Guitar Fretboard**: 12-fret interactive display highlighting scale tonics and chord positions.
- **Guitar Tab Generator**: Converts MIDI voicings into tablature notation.
- **Diatonic Table**: Calculates chord names, degrees, and MIDI note arrays.

### MIDI Engine

The engine (via mido) generates organic MIDI sequences:
- **Extensions**: Support for Triads, 6ths, 7ths, 9ths, 11ths, and 13ths.
- **Inversions**: Support for 1st, 2nd, and 3rd inversions.
- **Humanization**: Randomizes velocity and micro-timing.
- **Basslines**: Optional generation of root-based bass tracks.

## Installation

### Prerequisites
- Python 3.8+.
- Terminal with true color and UTF-8 support.

### Setup
Install via PyPI:

```bash
pip install chorderizer
```

### From Source

```bash
git clone https://github.com/TropicalDev/chorderizer.git
cd chorderizer
make dev
```

After bootstrapping, activate the environment and run tests:
```bash
source .venv/bin/activate
pytest
```

If you prefer to do it manually, use Python 3.10.19:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Execution

```bash
python -m chorderizer.chorderizer
```

## Interface Guide

- **[A] Add Chord**: Commits the highlighted chord to the progression list.
- **[X] Clear List**: Flushes the progression buffer.
- **[E] Export MIDI**: Saves the progression as a MIDI file in `~/chord_generator_midi_exports`.
- **[H] Manual**: Displays the operation manual.
- **[Q] Quit**: Closes the application.

## Quality Standards

The codebase follows PEP 8 standards:
- **Linting**: Managed via Ruff and Trunk.
- **Testing**: Unit tests use `pytest` for the theory engine and MIDI generation.
- **Architecture**: Modular design separates theory logic, MIDI generation, and the Textual dashboard.

## Documentation

The **[Wiki](docs/wiki/index.md)** contains technical specifications and guides.

*   **[Technical Architecture](docs/wiki/ARCHITECTURE.md)**
*   **[User Guide](docs/wiki/USER_GUIDE.md)**
*   **[Developer Guide](docs/wiki/DEVELOPER_GUIDE.md)**
*   **[Agent SOP](docs/AGENT.md)**

## License

MIT License. See LICENSE.md.

---
*Developed by TropicalDev.*

