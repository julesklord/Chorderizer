## 2024-05-18 - [Error Message Leakage]
**Vulnerability:** Raw exception messages were printed to user output, potentially leaking sensitive system information such as paths or OS details.
**Learning:** It is crucial to hide raw exception messages from users, providing only generic feedback, while logging the actual exception details securely for maintainers.
**Prevention:** Always use a logging module to track exact errors, and display sanitized messages to end users.
## 2024-05-24 - Gracefully Handle Interrupts to Avoid Stack Trace Leakage
**Vulnerability:** Raw `input()` calls without exception handling expose raw stack traces when users interrupt the process (e.g., via `Ctrl+C` or `Ctrl+D`), which can leak internal application structure or paths.
**Learning:** Always catch `EOFError` and `KeyboardInterrupt` specifically around CLI input prompts (or wrap them in a secure helper) to exit the application cleanly without dumping Python's internal exception stack to the console.
**Prevention:** Use a wrapper function for `input()` that catches these exceptions and calls `sys.exit(0)`, or ensure every raw `input()` block is wrapped in `try...except (EOFError, KeyboardInterrupt):`.
