🧪 [Add tests for get_numbered_option UI helper]

🎯 **What:** The testing gap addressed
Added missing tests for the `get_numbered_option` function in `src/chorderizer/ui.py`. This function is a core UI helper for capturing user selections, and previously lacked test coverage.

📊 **Coverage:** What scenarios are now tested
The new tests in `tests/test_ui.py` cover the following scenarios:
- Valid option selection
- Canceling the prompt (when allowed)
- Canceling the prompt (when not allowed, forcing valid input)
- Invalid input followed by valid input
- Empty input followed by valid input
- Graceful handling of `KeyboardInterrupt`
- Graceful handling of `EOFError`
- Handling dictionary option values

✨ **Result:** The improvement in test coverage
The test coverage for the UI module has significantly improved, ensuring the core interaction helper behaves correctly under various normal and edge-case conditions, making future refactoring safer.
