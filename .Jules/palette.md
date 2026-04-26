## 2024-04-20 - Helpful Empty States in Textual
**Learning:** Textual TUI widgets greatly benefit from explicit empty states, especially lists and panels, to guide the user on how to interact with the dashboard. The `display: none;` CSS property toggled via `.add_class("hidden")` and `.remove_class("hidden")` works perfectly for this.
**Action:** Always implement empty states for data containers in TUI applications to enhance onboarding and user guidance.
