import re

with open("src/chorderizer/ui.py", "r") as f:
    content = f.read()

# Already handled in ui.py:
# get_yes_no_answer (has try...except)
# get_numbered_option (has try...except)

# Needs try-except inside get_advanced_midi_options:
# 1. BPM input
bpm_pattern = r'''bpm_in = input\(
                f"\{Fore\.CYAN\}BPM \(tempo\) for MIDI \[default: \{options\['bpm'\]\}\]: \{Style\.RESET_ALL\}"
            \)\.strip\(\)'''

bpm_repl = '''try:
                bpm_in = input(
                    f"{Fore.CYAN}BPM (tempo) for MIDI [default: {options['bpm']}]: {Style.RESET_ALL}"
                ).strip()
            except (EOFError, KeyboardInterrupt):
                print_operation_cancelled()
                import sys
                sys.exit(0)'''
content = re.sub(bpm_pattern, bpm_repl, content)

# 2. Velocity input
vel_pattern = r'''vel_in = input\(
                f"\{Fore\.CYAN\}Base note velocity \(0-127\) \[default: \{options\['base_velocity'\]\}\]: \{Style\.RESET_ALL\}"
            \)\.strip\(\)'''

vel_repl = '''try:
                vel_in = input(
                    f"{Fore.CYAN}Base note velocity (0-127) [default: {options['base_velocity']}]: {Style.RESET_ALL}"
                ).strip()
            except (EOFError, KeyboardInterrupt):
                print_operation_cancelled()
                import sys
                sys.exit(0)'''
content = re.sub(vel_pattern, vel_repl, content)

# 3. Randomization range
rand_pattern = r'''rand_in = input\(
                    f"\{Fore\.CYAN\}Randomization range \(\+/-\) \[default: 5\]: \{Style\.RESET_ALL\}"
                \)\.strip\(\)'''

rand_repl = '''try:
                    rand_in = input(
                        f"{Fore.CYAN}Randomization range (+/-) [default: 5]: {Style.RESET_ALL}"
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    print_operation_cancelled()
                    import sys
                    sys.exit(0)'''
content = re.sub(rand_pattern, rand_repl, content)

# 4. Arp duration
arp_pattern = r'''arp_dur_in = input\(
                        f"\{Fore\.CYAN\}Duration of each arpeggio note in beats \[default: \{options\['arpeggio_note_duration_beats'\]\}\]: \{Style\.RESET_ALL\}"
                    \)\.strip\(\)'''

arp_repl = '''try:
                        arp_dur_in = input(
                            f"{Fore.CYAN}Duration of each arpeggio note in beats [default: {options['arpeggio_note_duration_beats']}]: {Style.RESET_ALL}"
                        ).strip()
                    except (EOFError, KeyboardInterrupt):
                        print_operation_cancelled()
                        import sys
                        sys.exit(0)'''
content = re.sub(arp_pattern, arp_repl, content)

# 5. Strum delay
strum_pattern = r'''strum_in = input\(
                    f"\{Fore\.CYAN\}Strum delay between notes \(milliseconds\) \[default: 15ms\]: \{Style\.RESET_ALL\}"
                \)\.strip\(\)'''

strum_repl = '''try:
                    strum_in = input(
                        f"{Fore.CYAN}Strum delay between notes (milliseconds) [default: 15ms]: {Style.RESET_ALL}"
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    print_operation_cancelled()
                    import sys
                    sys.exit(0)'''
content = re.sub(strum_pattern, strum_repl, content)

with open("src/chorderizer/ui.py", "w") as f:
    f.write(content)
