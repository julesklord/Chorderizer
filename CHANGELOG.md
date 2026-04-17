# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2026-04-17
### Added
- Created professional goodbye message on TUI exit.
### Changed
- **Trunk Standardization**: Moved `trunk.yaml` to the root directory for standard compliance.
- **Repository Sanitization**: Simplified `.gitignore` by grouping `.trunk/` internal files and removing redundant rules.
- **Documentation**: Finalized **Project Wiki** integration and cross-linked all technical documents.

## [0.2.4] - 2026-04-16
### Changed
- **Global Search & Replace**: Exhaustive standardization of all internal logic keys and UI strings to English (e.g., `grado` -> `degree`, `nombre` -> `name`).
- **User Guide**: Rewrote documentation to include VHS-generated `demo.gif` and detailed 4-phase workflow.
- **WIKI**: Initialized the project-wide documentation wiki index.

## [0.2.3] - 2026-04-16
### Fixed
- **Dependency Stabilization**: Pinned `textual`, `rich`, and `pytest` to stable major version ranges to prevent breaking API changes from automated updates.
- **CI/CD Reliability**: Resolved build failures in GitHub Actions caused by major version jumps in core dependencies.

## [0.2.2] - 2026-04-16
### Added
- **Premium TUI Dashboard**: Integrated a reactive dashboard using the Textual framework.
- **Visualizers**: 2-octave Piano board and 12-fret Guitar Fretboard widgets with real-time updates.
- **Guitar Tab Engine**: Automatic ASCII tablature generation for any chord voicing.
- **Transparency Support**: Configured TUI CSS to allow terminal-inherited background colors.
### Changed
- **Performance**: Optimized rendering of block characters for better recording compatibility (`vhs`).

## [0.2.0] - 2026-04-10
### Added
- **Core Harmonic Engine**: Support for 11+ scales including Greek Modes and Pentatonic variations.
- **MIDI Serialization**: Professional MIDI file generation with humanization, arpeggio styles, and automated bass tracks.

## [1.2.0] - 2026-03-29
*(Legacy Branch)*
### Added
- Unit tests for theory logic and MIDI range validation [0, 127].
- `colorama` integration for Windows terminal support.
### Changed
- Migrated build system to `pyproject.toml` (PEP 621).

## [1.0.1] - 2025-03-01
- **Initial Release**: Basic scale generation and MIDI export.
