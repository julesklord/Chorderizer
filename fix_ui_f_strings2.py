with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

text = text.replace('f"Enter ARPEGGIO NOTE DURATION in beats [default:', '"Enter ARPEGGIO NOTE DURATION in beats [default:')
text = text.replace('f"Enter STRUM DELAY in seconds [default', '"Enter STRUM DELAY in seconds [default')

with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)

with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()
text = text.replace('f"\\n{Fore.GREEN}Chords generated for the scale of {tonic} ({scale_info[\'name\']}):{Style.RESET_ALL}"', 'f"\\n{Fore.GREEN}Chords generated for the scale of {tonic} ({scale_info[\'name\']}):{Style.RESET_ALL}"')
text = text.replace('f"\\033[32mExiting program.\\033[0m"', '"\\033[32mExiting program.\\033[0m"')
text = text.replace('f"\\033[31mNo chords selected for MIDI processing.\\033[0m"', '"\\033[31mNo chords selected for MIDI processing.\\033[0m"')

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)
