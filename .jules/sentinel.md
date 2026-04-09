## 2024-05-16 - Prevent Stack Trace Leakage in Error Handling
**Vulnerability:** The application was catching raw exceptions during MIDI file generation and printing the full internal stack trace to stdout using `traceback.print_exc()`.
**Learning:** This is a classic information disclosure vulnerability (CWE-209: Generation of Error Message Containing Sensitive Information). It leaks internal application state, file paths, and dependency structure which can be used by attackers to map the application for further exploitation.
**Prevention:** Catch specific exceptions where possible, and always fail securely. Log detailed errors to a secure internal logging system, but only show generic, safe, and helpful error messages to the user without exposing stack traces.
