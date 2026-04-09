## 2024-04-04 - Handle CLI interruptions gracefully
**Learning:** KeyboardInterrupt (Ctrl+C) or EOFError (Ctrl+D) in command line input prompts normally crash the program and print ugly tracebacks. Wrapping the `input()` call in a `try...except` block with a cancellation message improves the user experience significantly.
**Action:** Always wrap `input()` prompts in a `try...except` block to gracefully handle early exit signals.

## 2024-05-18 - Terminal Color Contrast
**Learning:** Standard terminal blue (`Fore.BLUE` from colorama) often has poor contrast against dark backgrounds commonly used by developers, making text hard to read.
**Action:** Prefer `Fore.CYAN` or lighter shades for blue-related highlights in terminal outputs to ensure better readability and accessibility.
