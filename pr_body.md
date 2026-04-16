🎯 **What:** Extracted discrete chunks of input logic from `get_advanced_midi_options` in `src/chorderizer/ui.py` into smaller private helper methods (`_get_bpm`, `_get_base_velocity`, `_get_velocity_randomization`, `_get_arpeggio_settings`, and `_get_strum_delay`).

💡 **Why:** The original `get_advanced_midi_options` function was over 100 lines long, containing deeply nested try-except blocks. By moving these distinct input handlers to their own private methods, the overall cognitive load and complexity of `UIManager` are greatly reduced. This improves maintainability, making it much easier to comprehend or modify the input flow and defaults in the future.

✅ **Verification:**
- Formatted and linted `src/chorderizer/ui.py` using `black`, `isort`, and `flake8` to adhere to repository conventions.
- Executed `PYTHONPATH=src pytest tests/` which all 34 tests passed successfully, confirming functional parity was safely preserved.

✨ **Result:** `get_advanced_midi_options` has been heavily simplified, shedding nearly half its length and resolving the readability issue without compromising behavior or test stability.
