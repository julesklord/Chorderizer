# Chorderizer: Advanced Chord Generator & MIDI Exporter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/julesklord/Chorderizer)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/julesklord/Chorderizer/issues)

Chorderizer is a Python-based command-line tool designed for music enthusiasts, composers, and students. It empowers you to explore diatonic chords within various musical scales, customize chord voicings with extensions and inversions, view simple guitar tablatures, and export your chord progressions as MIDI files.

## Features

* **Versatile Scale Support:** Generate diatonic chords for multiple scales including Major, Natural Minor, Harmonic Minor, Melodic Minor (Ascending), Major Pentatonic, and Minor Pentatonic.
* **Chord Customization:**
  * **Extensions:** Tailor chord complexity with levels from simple Triads, 6ths, 7ths (scale default), 9ths, 11ths, up to 13ths.
  * **Inversions:** Apply Root Position, 1st, 2nd, or 3rd inversions to your chords.
* **Detailed Chord Information:** View generated chord names, their constituent notes (e.g., C, E, G), and corresponding MIDI note numbers.
* **Basic Guitar Tablatures:** Display simple guitar tablatures for the generated chords (standard tuning).
* **Custom Chord Progressions:** Define your own chord progressions using Roman numeral degrees (e.g., I-V-vi-IV) with optional beat durations per chord.
* **Advanced MIDI Export:**
  * Set custom BPM (tempo) and base note velocity.
  * Introduce velocity randomization for a more human feel.
  * Choose from a wide range of General MIDI instruments for chord and optional bass tracks.
  * Add an automated bassline playing the root notes.
  * Apply arpeggio styles (up, down, up-down) with configurable note durations.
  * Simulate a strumming effect for block chords with adjustable delay.
* **Transposition:** Easily transpose generated chord names and entire MIDI progressions to different keys while retaining original extension levels and inversions.
* **Interactive CLI:** User-friendly command-line interface guides you through the process.

## Installation

### Prerequisites

* Python 3.7 or higher.
* `pip` (Python package installer).

### From PyPI (Recommended)

Chorderizer is available on the Python Package Index (PyPI). You can install it using pip:
```bash
pip install chorderizer
```

*(Note: This package is not yet available on PyPI. This is a placeholder for future publication.)*

### From Source (Current Method)

1. **Clone the repository:**

    ```bash
    git clone https://your-repo-url/Chorderizer.git
    cd Chorderizer
    ```

    If you are running directly from source, ensure it's in a dedicated directory.

2. **Install dependencies:**
    Chorderizer relies on the `mido` library for MIDI manipulation.

    ```bash
    pip install mido
    ```
    To run it from the source directory (after navigating to the root of the project):
    ```bash
    python -m src.chorderizer.chorderizer
    ```

## Project Structure

The project code is organized into several modules within the `src/chorderizer` directory, including:
*   `chorderizer.py`: Main script with the `main()` function and overall orchestration.
*   `theory_utils.py`: Handles core music theory logic (scales, chords, intervals).
*   `generators.py`: Contains classes for generating chords, tablatures, and MIDI files.
*   `ui.py`: Manages command-line user interactions.

## Quick Start

1. **Navigate to the script's directory:**

    ```bash
    cd path/to/Chorderizer
    ```

2. **Run the script:**

    If you have installed the package, you can run:
    ```bash
    chorderizer
    ```
    Alternatively, to run it from the source directory (after navigating to the root of the project):
    ```bash
    python -m src.chorderizer.chorderizer
    ```

3. **Follow on-screen prompts:**
    * Select a tonic note for your scale.
    * Choose a scale type.
    * Define chord extension level and inversion.
    * View the generated chords and optional tablatures.
    * Optionally, define a chord progression.
    * Configure MIDI export settings (BPM, instruments, arpeggios, etc.).
    * Save your progression as a MIDI file.
    * Optionally, transpose your progression to a new key and export again.

## Usage

For detailed step-by-step instructions on using all features of Chorderizer, please refer to the GUIDE_OF_USE.md.

## Dependencies

* mido: A Python library for working with MIDI messages and files.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request on the project's repository (if applicable).

Some areas for potential contributions include:
*   Adding a comprehensive suite of automated unit tests to ensure code quality and facilitate easier refactoring.
*   Expanding the range of supported musical scales or chord types.
*   Enhancing the tablature generation with more sophisticated options.
*   Developing a graphical user interface (GUI).

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
