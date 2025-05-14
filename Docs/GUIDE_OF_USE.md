# Chorderizer - Guide of Use

Welcome to the Chorderizer user guide! This document will walk you through all the features and steps to effectively use this advanced chord generation and MIDI export tool.

## 1. Running the Script

Before you begin, ensure you have:

* Python 3.7+ installed.
* Chorderizer installed (see `README.md` for installation instructions). The `mido` dependency will be installed automatically with Chorderizer.

To start Chorderizer:

1. Open your terminal or command prompt.
2. Once Chorderizer is installed, you can run it from any location in your terminal.
3. Execute the command:

    ```bash
    python chorderizer.py
    ```

## 2. Main Workflow

The script operates through a series of interactive prompts.

### 2.1. Select Scale Tonic

* **Prompt:** "Tonic:"
* **Action:** You'll see a numbered list of all 12 chromatic notes (C, C#, D, etc.).
* **Input:** Enter the number corresponding to your desired tonic note.
* **Cancel:** Enter `0` to cancel the current operation or exit if at the main menu.

### 2.2. Select Scale Type

* **Prompt:** "Scale Type:"
* **Action:** A numbered list of available scales will be displayed (e.g., Major, Natural Minor, Harmonic Minor, etc.).
* **Input:** Enter the number for your chosen scale type. The combination of tonic and scale type defines your musical key (e.g., "C Major", "A Natural Minor").
* **Cancel:** Enter `0` to go back or cancel.

### 2.3. Chord Settings

After selecting the tonic and scale, you'll define how complex the generated chords should be.

* **Prompt:** "Chord extension level:"
  * **Options:**
        1. `Simple Triads`: Basic three-note chords (root, third, fifth).
        2. `Sixths`: Adds the 6th degree to triads (or the 7th if a 6th is less conventional for that chord type).
        3. `Sevenths (scale default)`: Generates standard diatonic 7th chords (e.g., maj7, m7, dom7).
        4. `Ninths`: Extends 7th chords to include the 9th.
        5. `Elevenths`: Extends 9th chords to include the 11th (can sound dense).
        6. `Thirteenths`: Extends 11th chords to include the 13th (can sound very dense).
  * **Input:** Enter the number for your desired extension level.

* **Prompt:** "Chord inversion:"
  * **Options:**
        1. `Root Position`: The root of the chord is the lowest note.
        2. `1st Inversion`: The third of the chord is the lowest note.
        3. `2nd Inversion`: The fifth of the chord is the lowest note.
        4. `3rd Inversion`: The seventh of the chord is the lowest note (applies to 7th chords and their extensions).
  * **Input:** Enter the number for your desired inversion.

### 2.4. Viewing Generated Chords

Once settings are confirmed, Chorderizer displays the diatonic chords for your selected scale, extension level, and inversion.

* **Format:** Each chord is listed with:
  * Its Roman numeral degree (e.g., `I`, `ii`, `V`).
  * The chord name (e.g., `Cmaj7`, `Dm7`, `G7`).
  * The constituent note names (e.g., `C, E, G, B`).
  * The MIDI note numbers for each note in the chord's voicing.
* **Color Coding:** Chords are color-coded for easier identification of their quality (e.g., green for major, blue for minor).

### 2.5. Tablature Display Options

* **Prompt:** "--- Filter for Displaying Tablatures ---"
* **Action:** You can choose to display basic guitar tablatures for the generated chords.
* **Options:**
    1. `All tablatures`
    2. `Only Minor chords`
    3. `Only chords with Seventh`
    4. `Only Major chords`
     ...and other specific filters.
    8. `No tablatures`
* **Input:** Enter the number for your preferred filter.
* **Note:** Tablatures are very basic, showing one possible fingering on a standard-tuned guitar, prioritizing lower frets.

## 3. MIDI Generation

After viewing the chords, you can create a MIDI file.

### 3.1. Define a Chord Progression

* **Prompt:** "Define a chord progression for MIDI? (If no, all diatonic chords will be used sequentially) (yes/no):"
* **If 'yes':**
  * **Prompt:** "Enter progression (degrees separated by '-', e.g., I-V-vi-IV). Optional duration in beats (e.g., I:4-V:2-vi:2-IV:4 ):"
  * **Input:** Type your progression using Roman numerals.
    * Example: `I-V-vi-IV`
    * Example with custom durations: `I:4-V:2-vi:2-IV:4` (Chord I for 4 beats, V for 2 beats, etc.)
    * If no duration is specified, a default of 4 beats per chord is used.
* **If 'no':**
  * All generated diatonic chords for the scale will be used sequentially, each with a default duration (typically 2 beats).

### 3.2. Advanced MIDI Options

You'll be prompted to configure several MIDI parameters:

* **BPM (tempo):** Default is 120. Enter your desired Beats Per Minute.
* **Base note velocity (0-127):** Default is 70. Controls the "loudness" of notes.
* **Add slight randomization to velocity?:** (yes/no) If yes, specify a range (e.g., +/- 5) to add human-like variation.
* **Instrument for chords:** Choose a General MIDI instrument from a numbered list for the main chord track.
* **Add bass track (root notes)?:** (yes/no)
  * If 'yes', **Instrument for bass:** Choose a General MIDI instrument for the bassline. The bass track will play the root note of each chord in a lower octave.
* **Arpeggiate chords?:** (yes/no)
  * If 'yes':
    * **Arpeggio style:** Choose `up`, `down`, or `updown`.
    * **Duration of each arpeggio note in beats:** Default is 0.25.
    * *Warning:* If the arpeggio (number of notes * duration per note) is longer than the chord's total duration, the script will try to adjust the last note, but the result might sound rushed or truncated.
* **Add strumming effect to block chords?:** (yes/no) (Only if not arpeggiating)
  * If 'yes', **Strum delay between notes (milliseconds):** Default is 15ms. Adds a slight delay between the notes of a block chord to simulate strumming.

### 3.3. Saving the MIDI File

* **Prompt:** "Enter MIDI filename [default: ...]:"
* **Action:** A default filename is suggested (e.g., `prog_C_Major.mid`).
* **Input:** Press Enter to accept the default, or type your desired filename (including `.mid`).
* **Location:** MIDI files are saved by default in a `chord_generator_midi_exports` folder within your user's home directory (e.g., `C:\Users\YourName\chord_generator_midi_exports` or `/home/yourname/chord_generator_midi_exports`). This folder is created automatically if it doesn't exist.

## 4. Transposition

After a MIDI file is generated for the original progression:

* **Prompt:** "Transpose these chord names to another scale tonic? (yes/no):"
* **If 'yes':**
    1. You'll be prompted again to **Select Scale Tonic** and **Select Scale Type** for the *new* key.
    2. The script will display the original chord degrees with their *newly transposed chord names* (e.g., if Cmaj7 was 'I' in C Major, and you transpose to G Major, 'I' will now be Gmaj7).
    3. **Prompt:** "Generate MIDI for these chords in the NEW key/scale? (yes/no):"
        * If 'yes', a new MIDI file will be generated. This new MIDI will:
            * Use the same Roman numeral progression and beat durations as your original.
            * Apply the same chord extension level and inversion settings.
            * Use the notes appropriate for the *new* key.
            * Retain the advanced MIDI options (BPM, instruments, etc.) from the original MIDI generation.
        * You'll be prompted for a filename for this transposed MIDI file (a default like `prog_TRANSP_G_Major.mid` will be suggested).

## 5. Continuing or Exiting

* **Prompt:** "Perform another operation? (yes/no):"
* **If 'yes':** The script loops back to allow you to generate chords for a new scale.
* **If 'no':** The program will display a goodbye message and exit.

## 6. File Structure (MIDI Exports)

* **Default Export Directory:** `~/chord_generator_midi_exports/`
  * `~` represents your user's home directory.
* **Example Filenames:**
  * `prog_Csharp_Major.mid`
  * `prog_TRANSP_G_Natural_Minor.mid`

---

Enjoy using Chorderizer to explore music theory and create your own chord progressions!
