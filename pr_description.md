🎯 What
Added missing tests for the `get_tablature_filter` function in `src/chorderizer/ui.py`. The function is used to capture the user's tablature filter preferences, which previously had no unit test coverage.

📊 Coverage
Created `tests/test_ui.py` with mock implementations to cover both the happy path and edge cases without executing actual IO bound calls:
- Tested valid choice selection (e.g. selection '3').
- Tested the default/cancel functionality correctly reverting to '8' (No tablatures).
All `chorderizer/ui.py` behavior inside `get_tablature_filter` is now covered.

✨ Result
Improved overall reliability and test suite coverage by validating that standard user interactions within `get_tablature_filter` generate the expected return values.
