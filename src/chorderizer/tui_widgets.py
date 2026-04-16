"""
tui_widgets.py — Custom Textual widgets for Chorderizer
"""

from typing import Any, Dict, List, Set

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Label, ListItem, ListView, Static


class PianoWidget(Static):
    """FAT Piano Keyboard with Note Labels."""

    DEFAULT_CSS = "PianoWidget { height: 8; width: 100%; }"

    def __init__(self, active_notes: Set[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.active_notes = active_notes or set()
        self.base_midi = 48

    def update_notes(self, notes: List[int]):
        self.active_notes = set()
        for n in notes:
            pc = n % 12
            self.active_notes.add(48 + pc)
            self.active_notes.add(60 + pc)
        self.refresh()

    def render(self) -> Panel:
        rows = [Text() for _ in range(4)]
        label_row = Text()
        white_names = ["C", "D", "E", "F", "G", "A", "B"]
        white_indices = [0, 2, 4, 5, 7, 9, 11]

        for oct in range(2):
            for i, w_idx in enumerate(white_indices):
                midi = self.base_midi + (oct * 12) + w_idx
                is_active = midi in self.active_notes
                color = "bright_cyan" if is_active else "white"

                has_black = w_idx in {0, 2, 5, 7, 9}
                black_active = (midi + 1) in self.active_notes
                black_color = "cyan" if black_active else "grey15"

                for r in range(4):
                    if r < 2 and has_black:
                        rows[r].append("██", style=color)
                        rows[r].append("█", style=black_color)
                    else:
                        rows[r].append("███", style=color)
                    rows[r].append("|", style="grey37")

                label_color = "bold cyan" if is_active else "bold white"
                label_row.append(f"{white_names[i]:^3}", style=label_color)
                label_row.append("|", style="grey37")

        full_piano = Text("\n").join(rows)
        full_piano.append("\n")
        full_piano.append(label_row)
        return Panel(
            Align.center(full_piano),
            title="[bold blue]Piano Board[/bold blue]",
            border_style="bright_blue",
        )


class FretboardWidget(Static):
    """Refined Guitar Fretboard visualizer using clean dots."""

    DEFAULT_CSS = "FretboardWidget { height: 9; width: 100%; }"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scale_notes_pc = set()
        self.chord_notes_midi = set()
        self.tonic_pc = 0
        self.strings = [64, 59, 55, 50, 45, 40]
        self.string_names = ["e", "B", "G", "D", "A", "E"]

    def update_view(self, scale_pcs: Set[int], chord_midis: List[int], tonic_pc: int):
        self.scale_notes_pc = scale_pcs
        self.chord_notes_midi = set(chord_midis)
        self.tonic_pc = tonic_pc
        self.refresh()

    def render(self) -> Panel:
        fretboard = Text()
        header = Text("      ")
        for f in range(13):
            header.append(f"{f:<4}", style="dim")
        fretboard.append(header)
        fretboard.append("\n")

        for i, start_midi in enumerate(self.strings):
            line = Text(f" {self.string_names[i]} ║")
            for fret in range(13):
                midi = start_midi + fret
                pc = midi % 12
                char = "──"
                style = "grey37"

                if midi in self.chord_notes_midi:
                    char = "● "
                    style = "bold bright_cyan"
                elif pc == self.tonic_pc:
                    char = "● "
                    style = "bold yellow"

                line.append(char, style=style)
                line.append("|", style="grey37")
            fretboard.append(line)
            fretboard.append("\n")

        return Panel(
            Align.center(fretboard),
            title="[bold yellow]Guitar Fretboard[/bold yellow]",
            border_style="yellow",
        )


class GuitarTabWidget(Static):
    """Visualizador de tablatura con Panel."""

    DEFAULT_CSS = "GuitarTabWidget { height: 100%; width: 100%; }"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chord_name = "None"
        self.tab_lines = []

    def update_tab(self, chord_name: str, tab_lines: List[str]):
        self.chord_name = chord_name
        self.tab_lines = tab_lines
        self.refresh()

    def render(self) -> Panel:
        content = Text()
        for line in self.tab_lines:
            if "|" in line:
                content.append(line.replace(" ", ""), style="bright_green")
                content.append("\n")

        return Panel(
            Align.center(content, vertical="middle"),
            title=f"[bold yellow]Tabs: {self.chord_name}[/bold yellow]",
            border_style="bright_cyan",
        )


class ProgressionItem(ListItem):
    """Representa un acorde en la lista de progresión."""

    def __init__(self, chord_data: Dict[str, Any]):
        super().__init__()
        self.chord_data = chord_data

    def compose(self) -> ComposeResult:
        yield Label(f" {self.chord_data['nombre']} [dim]({self.chord_data['grado']})[/]")


class ProgressionPanel(Static):
    """Panel lateral de la progresión de acordes."""

    DEFAULT_CSS = """
    ProgressionPanel {
        width: 32;
        border: tall $primary;
        padding: 0;
        background: $boost;
    }
    #prog-list {
        height: 1fr;
    }
    .prog-header {
        background: $accent;
        color: $text-primary;
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    #prog-help {
        text-align: center;
        padding: 1;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("PROGRESIÓN", classes="prog-header")
        yield ListView(id="prog-list")
        yield Label(" [bold][A][/bold] Add  [bold][X][/bold] Clear", id="prog-help")

    def add_chord(self, chord_data: Dict[str, Any]):
        self.query_one("#prog-list", ListView).append(ProgressionItem(chord_data))

    def clear_prog(self):
        self.query_one("#prog-list", ListView).clear()

    def get_progression_data(self) -> List[Dict[str, Any]]:
        return [
            item.chord_data
            for item in self.query_one("#prog-list", ListView).query(ProgressionItem)
        ]
