## 2024-04-25 - Tooltips and Interactions
**Learning:** In Textual UI applications, adding tooltips is highly beneficial for the UX but it requires verifying that the specific widget instances (Select, DataTable, RadioSet, Button, etc.) support the `tooltip` kwarg. Additionally, buttons need proper interaction handlers (e.g., `on_button_pressed`) to function, which were missing for the export MIDI feature in this app.
**Action:** Always verify interaction hooks and utilize `tooltip` arguments extensively when enhancing Textual apps.
