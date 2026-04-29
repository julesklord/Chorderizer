## 2024-04-24 - Textual TUI Button Wiring
**Learning:** In the Textual TUI framework, action buttons (like "EXPORT MIDI") might only be bound to keyboard shortcuts initially. They do not automatically trigger the associated keyboard action when clicked with a mouse unless an explicit `on_button_pressed` event handler is wired up.
**Action:** Always check TUI buttons to ensure they have both keyboard bindings and proper `on_button_pressed` event handlers for mouse users, and consider adding tooltips for better interaction clarity.
