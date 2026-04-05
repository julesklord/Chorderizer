## 2024-04-04 - Handle CLI interruptions gracefully
**Learning:** KeyboardInterrupt (Ctrl+C) or EOFError (Ctrl+D) in command line input prompts normally crash the program and print ugly tracebacks. Wrapping the `input()` call in a `try...except` block with a cancellation message improves the user experience significantly.
**Action:** Always wrap `input()` prompts in a `try...except` block to gracefully handle early exit signals.
