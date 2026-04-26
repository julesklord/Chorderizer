## 2024-05-19 - Textual TUI Empty States
**Learning:** In the Textual framework, managing empty states in lists (like `ListView`) requires explicitly toggling the `.display` property (boolean) between the empty indicator widget (e.g. `Label`) and the list widget itself. Textual doesn't have a built-in "empty placeholder" for iterables that handles this automatically yet.
**Action:** Always create a companion widget for the empty state with `display: none` in CSS initially, and manually toggle `self.query_one("#widget-id").display = False/True` in the methods that add/remove items.
