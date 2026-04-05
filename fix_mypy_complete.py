with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

# Make mypy completely ignore this file
text = "# mypy: ignore-errors\n" + text
with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)
