with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

text = text.replace('f"Enter instrument number (0-127) for CHORDS"', '"Enter instrument number (0-127) for CHORDS"')
text = text.replace('f"Enter instrument number (0-127) for BASS"', '"Enter instrument number (0-127) for BASS"')

with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)
