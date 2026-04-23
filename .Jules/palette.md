## 2024-05-18 - Missing tooltips in textual Buttons
**Learning:** Some Textual buttons might be primarily designed with keyboard shortcuts in mind, but lack basic interactivity for mouse users and discoverability (tooltips) for what the button does or its associated hotkey.
**Action:** When working on Textual UIs, ensure buttons have an explicit `tooltip` to expose keyboard shortcuts, and verify the `on_button_pressed` handler is correctly wired up so the button works as a clickable element.
