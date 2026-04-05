with open("pyproject.toml", "r") as f:
    text = f.read()

text += """
[tool.mypy]
ignore_missing_imports = true
"""

with open("pyproject.toml", "w") as f:
    f.write(text)
