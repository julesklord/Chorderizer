import re

with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

text = text.replace('f"Enter instrument number (0-127) for CHORDS [default', '"Enter instrument number (0-127) for CHORDS [default')
text = text.replace('f"Enter instrument number (0-127) for BASS [default', '"Enter instrument number (0-127) for BASS [default')

with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)

with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()

text = text.replace('f"\\n\\033[32mMIDI successfully generated to {output_path}\\033[0m"', 'f"\\n\\033[32mMIDI successfully generated to {output_path}\\033[0m"')
text = text.replace("import sys\n", "") # removed earlier when replaced but let's check sys usages

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)
