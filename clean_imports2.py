import re

with open("src/chorderizer/chorderizer.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'print_operation_cancelled' in line or 'get_numbered_option' in line:
        continue
    new_lines.append(line)

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.writelines(new_lines)
