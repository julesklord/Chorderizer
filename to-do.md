# Chorderizer: Active Tasks & TODOs

Master list of technical tasks and feature refinements to track progress beyond the strategic roadmap.

## 🚀 High Priority (Current Sprint)

- [ ] **TUI Migration (Phase 2.1)**
  - [ ] Initialize `Textual` app structure.
  - [ ] Design "Chord Dashboard" layout.
  - [ ] Implement reactive state for Scale/Key selection.
  - [ ] Add real-time log/preview window.
- [ ] **Audio Engine Research (Phase 2.2)**
  - [ ] Evaluate `pyaudio` vs `fluidsynth` for cross-platform MIDI playback.
  - [ ] Create a prototype `AudioPreview` helper class.

## 🛠️ Refactor & Maintenance

- [ ] **Docstrings & Type Hints**: Complete type hinting for private methods in `generators.py`.
- [ ] **Test Coverage**: Increase coverage to 90%+ (focus on edge cases in `VoiceLeader`).
- [ ] **Configuration File**: Move hardcoded defaults (BPM, Instruments) to a customizable `config.yaml`.

## 📈 Improvement Ideas

- [ ] **Scale Expansion**: Add Japanese scales (Akebono, Hirajoshi).
- [ ] **MIDI Drag-and-Drop**: (Research) Is it possible to implement a "drag to DAW" placeholder in a TUI?
- [ ] **Chord Progressions DB**: Add a catalog of famous progressions (e.g., "The Axis Progression", "Rhythm Changes").

---
*Created: 2026-04-10*
