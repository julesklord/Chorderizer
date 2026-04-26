"""
tui_app.py — Premium Harmony Station Dashboard
"""

import os
from datetime import datetime

from rich.markup import escape
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Label,
    RadioButton,
    RadioSet,
    RichLog,
    Select,
    Static,
)

from .generators import ChordGenerator, MidiGenerator, TablatureGenerator
from .theory_utils import MusicTheory
from .tui_widgets import FretboardWidget, GuitarTabWidget, PianoWidget, ProgressionPanel


class ManualScreen(ModalScreen):
    """Full-page manual with professional styling."""

    DEFAULT_CSS = """
    ManualScreen {
        align: center middle;
        background: rgba(0, 0, 0, 0.85);
    }
    #manual-container {
        width: 85%;
        max-width: 110;
        background: $surface;
        border: thick $accent;
        padding: 2 4;
    }
    .manual-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 2;
        border-bottom: solid $accent;
    }
    .manual-section {
        color: $accent;
        text-style: bold;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="manual-container"):
            yield Label("CHORDERIZER PRO — OPERATIONS MANUAL", classes="manual-title")
            yield Static(
                "[bold cyan]VISUALIZERS[/bold cyan]\n"
                "• [bold green]PIANO:[/bold green] 2-octave keyboard. Active notes in cyan.\n"
                "• [bold yellow]FRETBOARD:[/bold yellow] 12-fret guitar neck.\n"
                "  - [yellow]●[/yellow] : Scale tonic.\n"
                "  - [bright_cyan]●[/bright_cyan] : Selected chord position.\n\n"
                "[bold cyan]CORE SHORTCUTS[/bold cyan]\n"
                "• [white][A][/white] Add chord to progression (Right Sidebar).\n"
                "• [white][X][/white] Clear progression list.\n"
                "• [white][E][/white] Export current composition to MIDI.\n"
                "• [white][H][/white] or [white][F1][/white] View this manual.\n"
                "• [white][Q][/white] Quit application.\n\n"
                "[dim italic]Press any key or Esc to return to dashboard...[/]",
                markup=True,
            )

    def on_key(self) -> None:
        self.app.pop_screen()

    def on_click(self) -> None:
        self.app.pop_screen()


class ChorderizerApp(App):
    """Premium Adaptive Dashboard."""

    TITLE = "Chorderizer PRO"
    SUB_TITLE = "Harmonic Workstation"
    BINDINGS = [
        Binding("h", "push_screen('manual')", "Manual", show=True),
        Binding("f1", "push_screen('manual')", "Manual", show=False),
        Binding("q", "quit", "Quit", show=True),
        Binding("a", "add_to_progression", "Add Chord", show=True),
        Binding("x", "clear_progression", "Clear List", show=True),
        Binding("e", "export_midi", "Export MIDI", show=True),
    ]

    CSS = """
    Screen {
        background: transparent;
    }
    #sidebar {
        width: 30;
        background: transparent;
        border-right: tall $primary;
        padding: 1 1;
    }
    #progression-sidebar {
        width: 32;
        background: transparent;
    }
    .config-label {
        margin-top: 1;
        text-style: bold;
        color: $accent;
    }
    #center-col {
        width: 1fr;
        background: transparent;
    }

    PianoWidget {
        height: 8;
        margin-bottom: 0;
    }
    FretboardWidget {
        height: 9;
        border: none;
        margin-bottom: 1;
    }

    #data-row-container {
        height: 1fr;
        min-height: 8;
        margin-bottom: 0;
    }
    DataTable {
        width: 1fr;
        border: round $primary;
        margin: 0;
    }
    GuitarTabWidget {
        width: 1fr;
        margin-left: 0;
    }

    #status-log {
        height: 12;
        border: double $accent;
        background: $boost;
        color: $text-secondary;
        padding: 0 1;
    }

    DataTable > .datatable--cursor {
        background: $accent;
        color: $text-primary;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theory = MusicTheory()
        self.chord_gen = ChordGenerator(self.theory)
        self.midi_gen = MidiGenerator(self.theory)
        self.tab_gen = TablatureGenerator(self.theory)
        self.current_chords = {}
        self.current_midi = {}
        self.scale_notes_pc = set()
        self.tonic_pc = 0
        self.selected_row_data = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("TONIC", classes="config-label")
                yield Select(
                    [(n, n) for n in self.theory.CHROMATIC_NOTES],
                    id="tonic-select",
                    value="C",
                    tooltip="Select tonic note",
                )
                yield Label("SCALE", classes="config-label")
                yield Select(
                    [(v["name"], k) for k, v in self.theory.AVAILABLE_SCALES.items()],
                    id="scale-select",
                    value="1",
                    tooltip="Select musical scale",
                )
                yield Label("EXTENSIONS", classes="config-label")
                with RadioSet(id="extension-set", tooltip="Select chord extensions"):
                    yield RadioButton("Triads", value=True)
                    yield RadioButton("6ths")
                    yield RadioButton("7ths")
                    yield RadioButton("9ths")
                    yield RadioButton("11ths")
                    yield RadioButton("13ths")
                yield Label("INVERSION", classes="config-label")
                with RadioSet(id="inversion-set", tooltip="Select chord inversion"):
                    yield RadioButton("Root", value=True)
                    yield RadioButton("1st")
                    yield RadioButton("2nd")
                    yield RadioButton("3rd")
                yield Button(
                    "EXPORT MIDI",
                    variant="primary",
                    id="btn-export",
                    classes="mt-2",
                    tooltip="Export current progression to MIDI file",
                )

            with Vertical(id="center-col"):
                yield PianoWidget(id="piano")
                yield FretboardWidget(id="fretboard")
                with Horizontal(id="data-row-container"):
                    yield DataTable(id="chord-table", tooltip="Click a row to add to progression")
                    yield GuitarTabWidget(id="guitar-tab")
                yield RichLog(id="status-log", markup=True)

            yield ProgressionPanel(id="progression-sidebar")
        yield Footer()

    def log_status(self, msg: str, title: str = "SYSTEM"):
        """Logs in traditional terminal style with prompt."""
        log = self.query_one("#status-log", RichLog)
        now = datetime.now().strftime("%H:%M:%S")

        prompt = Text.assemble(
            (f"[{now}] ", "dim white"),
            ("chorderizer", "bold cyan"),
            ("> ", "bold white"),
            (f"{title} ", "bold magenta"),
            Text.from_markup(f"| {msg}"),
        )
        log.write(prompt)

    def on_mount(self) -> None:
        self.install_screen(ManualScreen(), name="manual")
        table = self.query_one("#chord-table", DataTable)
        table.add_columns("Degree", "Name", "MIDI")
        table.cursor_type = "row"
        self.log_status(
            "[bold green]Station initialized.[/bold green] Load scales and tonics.", "WELCOME"
        )
        self.update_chords()

    def on_select_changed(self) -> None:
        self.update_chords()

    def on_radio_set_changed(self) -> None:
        self.update_chords()

    def on_data_table_row_selected(self) -> None:
        self.action_add_to_progression()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-export":
            self.action_export_midi()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        degree = event.row_key.value
        if degree in self.current_midi:
            midi_notes = self.current_midi[degree]
            name = self.current_chords[degree]
            self.query_one("#piano", PianoWidget).update_notes(midi_notes)
            self.query_one("#fretboard", FretboardWidget).update_view(
                self.scale_notes_pc, midi_notes, self.tonic_pc
            )
            tabs = self.tab_gen.generate_simple_tab(name, midi_notes)
            self.query_one("#guitar-tab", GuitarTabWidget).update_tab(name, tabs)
            self.selected_row_data = {
                "degree": degree,
                "name": name,
                "midi_notes": midi_notes,
                "duration_beats": 4.0,
            }

    def action_add_to_progression(self) -> None:
        if self.selected_row_data:
            self.query_one("#progression-sidebar", ProgressionPanel).add_chord(
                self.selected_row_data
            )
            self.log_status(
                f"Chord [bold cyan]{self.selected_row_data['name']}[/] added.", "COMPOSER"
            )

    def action_clear_progression(self) -> None:
        self.query_one("#progression-sidebar", ProgressionPanel).clear_prog()
        self.log_status("Progression list reset.", "COMPOSER")

    def action_export_midi(self) -> None:
        prog_panel = self.query_one("#progression-sidebar", ProgressionPanel)
        prog_data = prog_panel.get_progression_data()
        if not prog_data:
            prog_data = [
                {"degree": d, "name": n, "midi_notes": self.current_midi[d], "duration_beats": 4.0}
                for d, n in self.current_chords.items()
            ]

        home = os.path.expanduser("~")
        export_dir = os.path.join(home, "chord_generator_midi_exports")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        filename = os.path.join(export_dir, f"comp_{len(prog_data)}_chds.mid")
        midi_opts = {
            "bpm": 120,
            "base_velocity": 85,
            "velocity_randomization_range": 5,
            "chord_instrument": 0,
            "add_bass_track": True,
            "bass_instrument": 33,
            "arpeggio_style": None,
            "voice_leading": True,
        }
        self.midi_gen.generate_midi_file(prog_data, filename, midi_opts)

        filename_clean = escape(os.path.basename(filename))
        export_dir_clean = escape(export_dir)
        self.log_status(
            f"Exported: [bold green]{filename_clean}[/]\nPath: [dim]{export_dir_clean}[/]",
            "MIDI EXPORT",
        )
        self.notify("MIDI Exported")

    def update_chords(self) -> None:
        t_sel = self.query_one("#tonic-select", Select)
        s_sel = self.query_one("#scale-select", Select)
        if t_sel.value is Select.BLANK or s_sel.value is Select.BLANK:
            return

        ext = self.query_one("#extension-set", RadioSet).pressed_index
        inv = self.query_one("#inversion-set", RadioSet).pressed_index
        scale_info = self.theory.AVAILABLE_SCALES[s_sel.value]

        try:
            tonic_full = t_sel.value + scale_info["tonic_suffix"]
            res = self.chord_gen.generate_scale_chords(tonic_full, scale_info, ext, inv)
            self.current_chords, _, self.current_midi, _ = res

            tonic_idx = self.theory.note_to_midi(t_sel.value)
            self.scale_notes_pc = {
                (tonic_idx + d["root_interval"]) % 12 for d in scale_info["degrees"].values()
            }
            self.tonic_pc = tonic_idx % 12

            table = self.query_one("#chord-table", DataTable)
            table.clear()
            for deg, name in self.current_chords.items():
                table.add_row(deg, name, str(self.current_midi[deg]), key=deg)
            self.log_status(
                f"Scale [bold cyan]{t_sel.value} {scale_info['name']}[/] loaded.", "THEORY"
            )
        except Exception as e:
            self.log_status(f"[red]Error: {e}[/red]", "THEORY ERROR")


if __name__ == "__main__":
    ChorderizerApp().run()
