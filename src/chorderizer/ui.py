"""
ui.py — Premium TUI for Chorderizer
====================================
A lightweight, responsive terminal UI built on prompt_toolkit.
Provides clean visual design, inline validation, and a streamlined
4-phase workflow.
"""

import shutil
from typing import Any, Dict, List, Optional, Tuple, Union

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import clear, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator

from .theory_utils import MusicTheory
from .translations import Translations

# ─── App Metadata ─────────────────────────────────────────────────────────────
VERSION = "1.2.0"

# ─── Color Palette ────────────────────────────────────────────────────────────
STYLE = Style.from_dict(
    {
        # Brand
        "banner": "#b57bee bold",
        "banner-sub": "#888888",
        "version": "#ffaf00",
        # Sections
        "section": "#5fd7ff bold",
        "rule": "#333333",
        # Menu items
        "key": "#ffaf00 bold",
        "value": "#d7d7d7",
        "hint": "#666666 italic",
        "cancel": "#ff5f5f",
        # Chord quality colours
        "major": "#5fd787 bold",
        "minor": "#87afff bold",
        "diminished": "#d787ff bold",
        "augmented": "#ffd75f bold",
        # Feedback
        "success": "#5fd787 bold",
        "error": "#ff5f5f bold",
        "warn": "#ffd75f bold",
        # Table
        "th": "#5fd7ff bold",
        "border": "#444444",
        "degree": "#888888",
        "midi-val": "#666666",
        # Prompt arrow
        "arrow": "#b57bee bold",
    }
)

# ─── Box Drawing ──────────────────────────────────────────────────────────────
# Heavy (banner)
H = {
    "tl": "╔",
    "tr": "╗",
    "bl": "╚",
    "br": "╝",
    "h": "═",
    "v": "║",
    "ml": "╠",
    "mr": "╣",
    "mt": "╦",
    "mb": "╩",
    "x": "╬",
}
# Light (tables)
L = {
    "tl": "┌",
    "tr": "┐",
    "bl": "└",
    "br": "┘",
    "h": "─",
    "v": "│",
    "ml": "├",
    "mr": "┤",
    "mt": "┬",
    "mb": "┴",
    "x": "┼",
}

# ─── Helpers ──────────────────────────────────────────────────────────────────


def _width() -> int:
    """Returns the current terminal width, capped at 120."""
    return min(shutil.get_terminal_size((80, 24)).columns, 120)


def _pp(html: str) -> None:
    """Print styled HTML text via prompt_toolkit."""
    print_formatted_text(HTML(html), style=STYLE)


def _raw(text: str) -> None:
    """Print plain text (no markup)."""
    print(text)


def _escape(text: str) -> str:
    """Escape HTML special chars so they print literally inside _pp()."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ─── Layout Components ────────────────────────────────────────────────────────


def render_banner() -> None:
    """Render the Chorderizer application banner."""
    clear()
    w = min(_width(), 62)
    inner = w - 2
    title = Translations.t("legacy_welcome")
    sub = f"{Translations.t('legacy_sub')}  ·  v{VERSION}"

    _pp(f"<banner>{H['tl']}{H['h'] * inner}{H['tr']}</banner>")
    _pp(f"<banner>{H['v']}</banner><banner>{title.center(inner)}</banner><banner>{H['v']}</banner>")
    _pp(
        f"<banner>{H['v']}</banner>"
        f"<banner-sub>{sub.center(inner)}</banner-sub>"
        f"<banner>{H['v']}</banner>"
    )
    _pp(f"<banner>{H['bl']}{H['h'] * inner}{H['br']}</banner>")
    _raw("")


def render_section(title: str) -> None:
    """Render a labelled section separator."""
    w = _width()
    _raw("")
    _pp(f"<section>  ◆  {title}</section>")
    _pp(f"<rule>  {'─' * (w - 4)}</rule>")


def render_success(msg: str) -> None:
    _pp(f"<success>  ✓  {_escape(msg)}</success>")


def render_error(msg: str) -> None:
    _pp(f"<error>  ✗  {_escape(msg)}</error>")


def render_warn(msg: str) -> None:
    _pp(f"<warn>  ⚠  {_escape(msg)}</warn>")


def render_cancelled() -> None:
    _pp(f"\n<warn>  ⊘  {Translations.t('legacy_op_cancelled')}</warn>")


# ─── Chord Table ──────────────────────────────────────────────────────────────


def render_chord_table(
    chord_names: Dict[str, str],
    note_names: Dict[str, List[str]],
    midi_notes: Dict[str, List[int]],
    base_qualities: Dict[str, str],
    tonic: str,
    scale_name: str,
) -> None:
    """Render a premium chord table with box-drawing borders."""
    w = _width()

    # Determine column widths dynamically
    col_deg = max(8, max((len(d) for d in chord_names), default=4) + 2)
    col_chord = max(18, max((len(n) for n in chord_names.values()), default=6) + 4)
    col_notes = max(24, min(30, w - col_deg - col_chord - 20))
    col_midi = max(14, w - col_deg - col_chord - col_notes - 4)

    def hline(left, mid, right, bold="h"):
        seg = L[bold]
        return (
            f"{left}{seg * col_deg}"
            f"{mid}{seg * col_chord}"
            f"{mid}{seg * col_notes}"
            f"{mid}{seg * col_midi}{right}"
        )

    def cell(deg, chord, notes, midi_v):
        return (
            f"<border>{L['v']}</border>"
            f"{deg.center(col_deg)}"
            f"<border>{L['v']}</border>"
            f"{chord:<{col_chord}}"
            f"<border>{L['v']}</border>"
            f"{notes:<{col_notes}}"
            f"<border>{L['v']}</border>"
            f"{midi_v:<{col_midi}}"
            f"<border>{L['v']}</border>"
        )

    _raw("")
    _pp(f"  <section>{_escape(tonic)} — {_escape(scale_name)}</section>")
    _raw("")
    _pp(f"<border>  {hline(L['tl'], L['mt'], L['tr'])}</border>")
    _pp(
        "  "
        + cell(
            f"<th>{Translations.t('degree').center(col_deg)}</th>",
            f"<th>{Translations.t('name'):<{col_chord}}</th>",
            f"<th>{'Notes':<{col_notes}}</th>",
            f"<th>{Translations.t('midi'):<{col_midi}}</th>",
        )
    )
    _pp(f"<border>  {hline(L['ml'], L['x'], L['mr'])}</border>")

    QUALITY_TAG = {
        "major": "major",
        "minor": "minor",
        "diminished": "diminished",
        "augmented": "augmented",
    }

    for degree, chord_name in chord_names.items():
        qual = base_qualities.get(degree, "major")
        tag = QUALITY_TAG.get(qual, "value")
        notes_str = ", ".join(note_names.get(degree, []))
        midi_str = ", ".join(str(n) for n in midi_notes.get(degree, []))

        # Truncate long strings to fit column
        notes_str = (notes_str[: col_notes - 2] + "…") if len(notes_str) > col_notes else notes_str
        midi_str = (midi_str[: col_midi - 2] + "…") if len(midi_str) > col_midi else midi_str

        _pp(
            "  "
            + cell(
                f"<degree>{_escape(degree).center(col_deg)}</degree>",
                f"<{tag}>{_escape(chord_name):<{col_chord}}</{tag}>",
                f"<value>{_escape(notes_str):<{col_notes}}</value>",
                f"<midi-val>{_escape(midi_str):<{col_midi}}</midi-val>",
            )
        )

    _pp(f"<border>  {hline(L['bl'], L['mb'], L['br'])}</border>")
    _raw("")


def render_guitar_tab(chord_name: str, tab_lines: List[str]) -> None:
    """Render guitar tab block with styling."""
    _pp(f"    <dim>  ┌─ {_escape(chord_name)} ──────</dim>")
    for line in tab_lines[1:]:  # skip the header line from generator
        _pp(f"    <dim>  │  {_escape(line)}</dim>")
    _raw("")


# ─── Interactive Prompts ──────────────────────────────────────────────────────


def _prompt_raw(default: str = "", completer=None, validator=None) -> str:
    """Internal: display the styled › prompt and return input."""
    return prompt(
        HTML("<arrow>  › </arrow>"),
        style=STYLE,
        default=default,
        completer=completer,
        validator=validator,
        validate_while_typing=True,
    ).strip()


def prompt_menu(
    title: str,
    options: Dict[Union[str, int], Any],
    allow_cancel: bool = True,
    cancel_key: str = "0",
) -> Optional[str]:
    """
    Display a numbered list menu and return the chosen key,
    or None if the user cancels.
    """
    display = {str(k): v for k, v in options.items()}
    max_kw = max((len(k) for k in display), default=1)
    if allow_cancel:
        max_kw = max(max_kw, len(cancel_key))

    _pp(f"\n<section>  {_escape(title)}</section>")
    for k, v in display.items():
        name = v.get("name", v) if isinstance(v, dict) else str(v)
        _pp(f"  <key>{k.rjust(max_kw)}.</key>  <value>{_escape(name)}</value>")
    if allow_cancel:
        _pp(
            f"  <cancel>{cancel_key.rjust(max_kw)}.</cancel>  <hint>← {Translations.t('legacy_skip')}</hint>"
        )
    _pp(f"  <hint>{'─' * 30}</hint>")

    valid = set(display.keys())
    if allow_cancel:
        valid.add(cancel_key)
    completer = WordCompleter(sorted(valid), sentence=True)

    while True:
        try:
            answer = _prompt_raw(completer=completer)
        except (EOFError, KeyboardInterrupt) as err:
            raise KeyboardInterrupt from err

        if not answer:
            continue
        if allow_cancel and answer == cancel_key:
            return None
        if answer in display:
            return answer
        render_error(f"'{answer}' is not a valid option.")


def prompt_text(
    title: str,
    default: str = "",
    validator: Optional[Validator] = None,
    completer=None,
    hint: str = "",
) -> str:
    """Display a styled text input prompt."""
    _pp(f"\n<section>  {_escape(title)}</section>")
    if hint:
        _pp(f"  <hint>{_escape(hint)}</hint>")
    try:
        return _prompt_raw(default=default, validator=validator, completer=completer)
    except (EOFError, KeyboardInterrupt):
        raise KeyboardInterrupt from None


def prompt_confirm(message: str, default: bool = False) -> bool:
    """Display a yes/no confirmation prompt."""
    tag = "[Y/n]" if default else "[y/N]"
    _pp(f"\n  <value>{_escape(message)}</value>  <hint>{tag}</hint>")
    try:
        ans = _prompt_raw().lower()
        if not ans:
            return default
        return ans in ("y", "yes", "si", "s")
    except (EOFError, KeyboardInterrupt):
        raise KeyboardInterrupt from None


# ─── Validators ───────────────────────────────────────────────────────────────


class RangeValidator(Validator):
    """Validates that input is a number within [low, high]."""

    def __init__(self, low: float, high: float, allow_empty: bool = True):
        self.low = low
        self.high = high
        self.allow_empty = allow_empty

    def validate(self, document):
        text = document.text.strip()
        if not text:
            if not self.allow_empty:
                raise ValidationError(
                    message=f"Required. Enter a number between {self.low} and {self.high}."
                )
            return
        try:
            val = float(text)
        except ValueError as err:
            raise ValidationError(message="Must be a number.") from err
        if not (self.low <= val <= self.high):
            raise ValidationError(message=f"Must be between {self.low} and {self.high}.")


# ─── UIManager ────────────────────────────────────────────────────────────────


class UIManager:
    """Manages all user interaction for the Chorderizer workflow."""

    def __init__(self, theory: MusicTheory):
        self.theory = theory

    # ── Phase 1: Scale Configuration ─────────────────────────────────────────

    def select_scale_config(
        self,
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Phase 1 — Unified tonic + scale selection.
        Returns (full_tonic_name, scale_info_dict) or (None, None) on cancel.
        """
        render_section(Translations.t("legacy_phase1"))

        tonic_opts = {str(i + 1): note for i, note in enumerate(self.theory.CHROMATIC_NOTES)}
        tonic_key = prompt_menu(Translations.t("legacy_select_tonic"), tonic_opts)
        if tonic_key is None:
            return None, None
        tonic = tonic_opts[tonic_key]

        scale_key = prompt_menu(Translations.t("legacy_select_scale"), self.theory.AVAILABLE_SCALES)
        if scale_key is None:
            return None, None
        scale_info = self.theory.AVAILABLE_SCALES[scale_key]

        full_tonic = tonic + scale_info["tonic_suffix"]
        render_success(f"Scale set to  {full_tonic}  ({scale_info['name']})")
        return full_tonic, scale_info

    # ── Phase 2: Chord Configuration ─────────────────────────────────────────

    def select_chord_config(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Phase 2 — Extension level and inversion in one compact section.
        Returns (extension_level, inversion_index) or (None, None) on cancel.
        """
        render_section(Translations.t("legacy_phase2"))

        ext_map = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5}
        ext_opts = {
            "1": f"{Translations.t('ext_triads')}            (3 notes — clean & simple)",
            "2": f"{Translations.t('ext_6ths')}            (4 notes — rich colour)",
            "3": f"{Translations.t('ext_7ths')}          (4 notes — jazz / default)",
            "4": f"{Translations.t('ext_9ths')}            (5 notes — lush)",
            "5": f"{Translations.t('ext_11ths')}         (6 notes — dense, modern)",
            "6": f"{Translations.t('ext_13ths')}       (7 notes — full harmonic stack)",
        }
        ext_key = prompt_menu(Translations.t("legacy_chord_ext"), ext_opts)
        if ext_key is None:
            return None, None
        ext_level = ext_map[ext_key]

        inv_opts = {
            "1": f"{Translations.t('inv_root')} Position     (standard)",
            "2": f"{Translations.t('inv_1st')} Inversion     (3rd in bass)",
            "3": f"{Translations.t('inv_2nd')} Inversion     (5th in bass)",
            "4": f"{Translations.t('inv_3rd')} Inversion     (7th in bass — 7ths+)",
        }
        inv_key = prompt_menu(Translations.t("legacy_chord_inv"), inv_opts)
        if inv_key is None:
            return None, None
        inv_idx = int(inv_key) - 1

        return ext_level, inv_idx

    # ── Phase 3: Tablature Filter ─────────────────────────────────────────────

    def prompt_tablature_filter(self) -> str:
        """Return a tab filter key, defaulting to '8' (none)."""
        tab_opts = {
            "1": Translations.t("legacy_all_chords"),
            "2": "Minor chords only",
            "3": "Seventh chords only",
            "4": "Ninth chords only",
            "5": "Sixth chords only",
            "6": "Eleventh chords only",
            "7": "Thirteenth chords only",
            "8": Translations.t("legacy_skip"),
        }
        choice = prompt_menu(Translations.t("legacy_tab_filter"), tab_opts, allow_cancel=True)
        return choice if choice is not None else "8"

    # ── Phase 4a: Progression Input ───────────────────────────────────────────

    def prompt_progression(self, chord_names: Dict[str, str]) -> Optional[str]:
        """
        Prompt the user to enter a chord progression string.
        Returns the raw string, or None to use all diatonic chords.
        """
        degrees = list(chord_names.keys())
        completer = WordCompleter(degrees, sentence=False, ignore_case=True)

        example = ""
        if len(degrees) >= 5:
            example = f"{degrees[0]}:4-{degrees[4]}:2-{degrees[5] if len(degrees) > 5 else degrees[-1]}:4-{degrees[3]}:2"

        raw = prompt_text(
            Translations.t("legacy_prog_prompt"),
            hint=f"Degrees: {' '.join(degrees)} · Example: {example}",
            completer=completer,
        )
        return raw.strip() if raw.strip() else None

    # ── Phase 4b: MIDI Options ────────────────────────────────────────────────

    def get_midi_options(self) -> Dict[str, Any]:
        """
        Phase 4 — Collect all MIDI export options in a compact, guided form.
        Returns options dict consumed by MidiGenerator.
        """
        render_section(Translations.t("legacy_phase4"))

        options: Dict[str, Any] = {
            "bpm": 120,
            "base_velocity": 70,
            "velocity_randomization_range": 0,
            "chord_instrument": 0,
            "add_bass_track": False,
            "bass_instrument": 33,
            "arpeggio_style": None,
            "arpeggio_note_duration_beats": 0.25,
            "strum_delay_ms": 0,
            "voice_leading": False,
        }

        # — Tempo
        bpm_raw = prompt_text(
            "Tempo (BPM):",
            default=str(options["bpm"]),
            validator=RangeValidator(20, 300),
            hint="20 – 300 · press Enter to keep default",
        )
        if bpm_raw:
            try:
                options["bpm"] = max(20, min(300, int(float(bpm_raw))))
            except ValueError:
                pass

        # — Velocity
        vel_raw = prompt_text(
            "Base Velocity (0–127):",
            default=str(options["base_velocity"]),
            validator=RangeValidator(0, 127),
            hint="0 = silent  ·  127 = maximum",
        )
        if vel_raw:
            try:
                options["base_velocity"] = max(0, min(127, int(vel_raw)))
            except ValueError:
                pass

        # — Humanize velocity
        if prompt_confirm("Add slight velocity humanization?"):
            rand_raw = prompt_text(
                "Humanization range (+/-):",
                default="5",
                validator=RangeValidator(0, 20),
            )
            try:
                options["velocity_randomization_range"] = max(0, min(20, int(rand_raw or "5")))
            except ValueError:
                pass

        # — Chord instrument
        instr_key = prompt_menu(
            "Chord Instrument:",
            self.theory.MIDI_PROGRAMS,
            allow_cancel=False,
        )
        if instr_key is not None:
            options["chord_instrument"] = int(instr_key)

        # — Bass track
        if prompt_confirm("Add bass track (root notes)?"):
            options["add_bass_track"] = True
            bass_key = prompt_menu(
                "Bass Instrument:",
                self.theory.MIDI_PROGRAMS,
                allow_cancel=False,
            )
            if bass_key is not None:
                options["bass_instrument"] = int(bass_key)

        # — Playback style: Arpeggio or Block
        if prompt_confirm("Arpeggiate chords? (otherwise block chords)"):
            arp_styles = {"1": "up", "2": "down", "3": "updown"}
            sk = prompt_menu("Arpeggio Direction:", arp_styles, allow_cancel=True)
            if sk:
                options["arpeggio_style"] = arp_styles[sk]
                dur_raw = prompt_text(
                    "Note duration per arpeggio step (beats):",
                    default="0.25",
                    validator=RangeValidator(0.01, 8.0),
                )
                try:
                    options["arpeggio_note_duration_beats"] = float(dur_raw or "0.25")
                except ValueError:
                    pass
        else:
            if prompt_confirm("Add strum delay to block chords?"):
                strum_raw = prompt_text(
                    "Strum delay (ms):",
                    default="15",
                    validator=RangeValidator(0, 100),
                    hint="0 = instant  ·  100 ms = slow strum",
                )
                try:
                    options["strum_delay_ms"] = max(0, min(100, int(strum_raw or "15")))
                except ValueError:
                    pass

        # — Voice leading
        options["voice_leading"] = prompt_confirm(
            "Apply voice leading? (smooth note motion between chords)"
        )

        return options

    # ── Legacy aliases (kept for backward compat with tests) ─────────────────

    def select_tonic_and_scale(
        self,
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """Alias for select_scale_config() — kept for backward compatibility."""
        return self.select_scale_config()

    def get_advanced_midi_options(self) -> Dict[str, Any]:
        """Alias for get_midi_options() — kept for backward compatibility."""
        return self.get_midi_options()


# ─── Standalone helpers (used by chorderizer.py) ──────────────────────────────


def print_welcome_message() -> None:
    render_banner()


def print_operation_cancelled() -> None:
    render_cancelled()


def get_yes_no_answer(prompt_msg: str) -> bool:
    return prompt_confirm(prompt_msg)


def get_numbered_option(
    title: str,
    options: Dict[Union[str, int], Any],
    allow_cancel: bool = True,
    cancel_key: str = "0",
) -> Optional[str]:
    return prompt_menu(title, options, allow_cancel=allow_cancel, cancel_key=cancel_key)


def get_chord_settings() -> Tuple[Optional[int], Optional[int]]:
    """Standalone chord config — delegates to a temporary UIManager."""
    # Imported here to avoid circular; theory only needed for UIManager
    theory = MusicTheory()
    ui = UIManager(theory)
    return ui.select_chord_config()


def get_tablature_filter() -> str:
    theory = MusicTheory()
    ui = UIManager(theory)
    return ui.prompt_tablature_filter()
