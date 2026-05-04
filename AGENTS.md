# AGENTS.md — Chorderizer

## Quick orientation

- **Language**: Python 3.8+ (tested on 3.8–3.12)
- **Framework**: Textual TUI (reactive dashboard) + classic prompt-based terminal flow
- **Package layout**: `src/chorderizer/` (setuptools, `where = ["src"]`)
- **Entry point**: `python -m chorderizer.chorderizer` or `chorderizer` CLI (exposed via `pyproject.toml`)
- **Music data**: `src/chorderizer/data/scales.json` (loaded at runtime, not generated)

## Module map

| Module | Role |
|--------|------|
| `theory_utils.py` | MusicTheory constants + MusicTheoryUtils pure functions |
| `generators.py` | ChordGenerator (with `_chord_cache`), MidiGenerator, TablatureGenerator |
| `chorderizer.py` | Orchestration coordinator + dashboard launcher |
| `ui.py` | Classic terminal UI (UIManager, colorama + rich) |
| `tui_app.py` | Textual app shell (ChorderizerApp) |
| `tui_widgets.py` | PianoWidget, FretboardWidget, GuitarTabWidget, ProgressionPanel |

## Developer commands

```bash
pip install -e ".[dev]"   # dev setup (adds pytest, pytest-cov, ruff)
pytest                        # run all tests
pytest tests/test_theory.py   # run a single test file
ruff check src/ tests/        # lint
ruff format src/ tests/       # format
```

## Verification order

CI runs: install → `pytest` (no separate lint step in CI; ruff is local-only via Trunk).

Local recommended order: `ruff format` → `ruff check` → `pytest`

## Tooling quirks

- **Ruff**: Configured in `pyproject.toml` (not `ruff.toml`). Target Python 3.8, line-length 100, double quotes.
- **Trunk**: Used for local quality gate (see `user_trunk.yaml`). Wraps ruff, black, isort, bandit, trufflehog. Not required for CI.
- **setuptools**: Uses `setup.cfg`-less config — all in `pyproject.toml`.
- **Package data**: `data/*.json` included via `[tool.setuptools.package-data]`.

## Testing notes

- Tests live in `tests/` (separate from `src/`).
- Test modules: `test_theory.py`, `test_generators.py`, `test_chorderizer.py`, `test_ui.py`, `test_security.py`.
- No special fixtures or services required — pure unit tests with `pytest`.
- Security tests (`test_security.py`) cover file handling boundaries.

## Repository conventions

- Two UIs maintained: classic terminal flow + Textual dashboard (shared theory/generator layer).
- TUI Dual-Mode: `tui_app.py` manages `Compose` and `Jam` views via `ContentSwitcher`.
- MIDI exports go to `~/chord_generator_midi_exports/` (hardcoded in `generators.py`).
- Chord voicing heuristic: keeps notes near C4 (MIDI 60) using `last_added_midi_note` strategy in `ChordGenerator`.
- Responsive TUI: `FretboardWidget` adapts horizontally (12-24 frets) and vertically.
- Maintenance docs: `DECISIONS.md` (repo changes), `TECHNICAL_DEBT.md` (deferred work), `FAILURES.md` (broken assumptions).

## Docs-as-code

- Architecture: `Docs/ARCHITECTURE.md`
- API reference: `Docs/API_REFERENCE.md`
- User guide: `Docs/USER_GUIDE.md`
- Specs: `.specsmd/` (specs-as-code, processed by GitHub agent prompts in `.github/prompts/`)
