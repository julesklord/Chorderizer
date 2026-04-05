with open("src/chorderizer/ui.py", "r") as f:
    lines = f.readlines()

if lines[0].startswith("# type: ignore"):
    lines.pop(0)

with open("src/chorderizer/ui.py", "w") as f:
    f.writelines(lines)
