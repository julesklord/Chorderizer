import re

with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()

# Fix f-string without placeholders
text = text.replace('f"\\n\\033[36m---', '"\\n\\033[36m---')
text = text.replace('f"\\033[31mInvalid scale type.\\033[0m"', '"\\033[31mInvalid scale type.\\033[0m"')

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)

with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()
text = text.replace('f"Invalid choice. Please select an option from the menu."', '"Invalid choice. Please select an option from the menu."')
text = text.replace('f"Please select an option corresponding to a scale type."', '"Please select an option corresponding to a scale type."')
with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)
