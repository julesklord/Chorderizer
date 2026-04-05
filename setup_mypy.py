import re

with open("pyproject.toml", "r") as f:
    text = f.read()

# remove duplicate [tool.mypy] if any
text = re.sub(r'\[tool\.mypy\].*', '', text, flags=re.DOTALL)

text += """
[tool.mypy]
ignore_missing_imports = true
"""

with open("pyproject.toml", "w") as f:
    f.write(text)

with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

text = text.replace('options_dict: Dict[str, Any]', 'options_dict: Dict[Any, Any]')

with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)
