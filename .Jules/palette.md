## 2024-05-14 - Missing Button Handlers and Tooltips in Textual TUI
**Learning:** Found that visual buttons in Textual (`yield Button(...)`) may be disconnected from their underlying actions if not explicitly wired via `on_button_pressed` or `@on(Button.Pressed)`. Adding tooltips explaining not just the action but the keyboard shortcut significantly improves discoverability in keyboard-heavy interfaces.
**Action:** When adding buttons to Textual apps, always ensure they are wired up in an event handler and have a descriptive tooltip, especially if there's a corresponding keyboard binding.
