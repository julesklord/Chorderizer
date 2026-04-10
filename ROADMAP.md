# Project Roadmap: Chorderizer

Project roadmap and future vision for Chorderizer.

## Phase 1: Stabilization & Documentation (Current)

* [x] **Refactor Core Logic**: Complete extraction of helper methods in `generators.py`.
* [x] **Logic Verification**: Ensure 100% pass rate in unit tests and verify core features.
* [x] **Technical Documentation**: Establish official `ARCHITECTURE.md`, `DEVELOPER_GUIDE.md`, and `API_REFERENCE.md`.
* [ ] **Version Alignment**: Standardize versioning across `pyproject.toml`, `ui.py`, and documentation.

## Phase 2: User Experience & Theory

* [ ] **Modern TUI (Terminal User Interface)**: Transition from basic sequential prompts to an interactive dashboard using `Textual`.
* [ ] **Voice Leading Algorithm**: Implement "minimum motion" voice leading to create professional-sounding chord transitions.
* [ ] **In-App Preview**: Basic audio playback of generated chords using `fluidsynth` or `pyaudio`.
* [ ] **Visual Feedback**: Real-time piano/guitar visualization of chords in the terminal.

## Phase 3: Advanced Features & Ecosystem

* [ ] **Modal Interchange & Borrowed Chords**: Smart suggestions for advanced progressions.
* [ ] **Plugin System**: External loading of custom scales and chord structures via YAML/JSON.
* [ ] **AI-Assisted Composition**: Integration with lightweight LLMs for style-based progression generation.
* [ ] **Export Expansion**: Support for MusicXML and MIDI 2.0.

---

*Last updated: 2026-04-09*
