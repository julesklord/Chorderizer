import re

with open("src/chorderizer/chorderizer.py", "r") as f:
    content = f.read()

# Replace input() calls with try-except blocks
# 1. Progression input
prog_pattern = r'''progression_input_str = \(
            input\(
                f"\{Fore\.CYAN\}Enter progression \(degrees separated by '-', e\.g\., I-V-vi-IV\)\. "
                f"Optional duration in beats \(e\.g\., I:4-V:2-vi:2-IV:4 \): \{Style\.RESET_ALL\}"
            \)
            \.strip\(\)
            \.upper\(\)
        \)'''

prog_repl = '''try:
            progression_input_str = (
                input(
                    f"{Fore.CYAN}Enter progression (degrees separated by '-', e.g., I-V-vi-IV). "
                    f"Optional duration in beats (e.g., I:4-V:2-vi:2-IV:4 ): {Style.RESET_ALL}"
                )
                .strip()
                .upper()
            )
        except (EOFError, KeyboardInterrupt):
            print_operation_cancelled()
            return True'''

content = re.sub(prog_pattern, prog_repl, content)

# 2. MIDI filename
midi_pattern = r'''output_midi_filename = input\(
        f"\{Fore\.CYAN\}Enter MIDI filename \[default: \{suggested_midi_path\}\]: \{Style\.RESET_ALL\}"
    \)\.strip\(\)'''

midi_repl = '''try:
        output_midi_filename = input(
            f"{Fore.CYAN}Enter MIDI filename [default: {suggested_midi_path}]: {Style.RESET_ALL}"
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print_operation_cancelled()
        return True'''

content = re.sub(midi_pattern, midi_repl, content)

# 3. Transposed MIDI filename
trans_pattern = r'''trans_midi_fname_out = input\(
                                f"\{Fore\.CYAN\}Enter transposed MIDI filename \[default: \{sugg_trans_path\}\]: \{Style\.RESET_ALL\}"
                            \)\.strip\(\)'''

trans_repl = '''try:
                                trans_midi_fname_out = input(
                                    f"{Fore.CYAN}Enter transposed MIDI filename [default: {sugg_trans_path}]: {Style.RESET_ALL}"
                                ).strip()
                            except (EOFError, KeyboardInterrupt):
                                print_operation_cancelled()
                                return True'''

content = re.sub(trans_pattern, trans_repl, content)

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(content)
