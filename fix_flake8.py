with open("src/chorderizer/theory_utils.py", "r") as f:
    text = f.read()

text = text.replace("from typing import Any, Dict, List, Mapping, Optional, Tuple, Union", "from typing import Any, Dict, List, Optional, Tuple")

with open("src/chorderizer/theory_utils.py", "w") as f:
    f.write(text)

with open("tests/test_theory.py", "r") as f:
    text = f.read()
text = text.replace("from chorderizer.theory_utils import MusicTheory, MusicTheoryUtils", "from chorderizer.theory_utils import MusicTheoryUtils")
with open("tests/test_theory.py", "w") as f:
    f.write(text)

with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()
text = text.replace("import colorama\n", "")
text = text.replace('f"Option: "', '"Option: "')
text = text.replace('f"Choice: "', '"Choice: "')
with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)

with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()
text = text.replace('f"\\n\\033[36m---', '"\\n\\033[36m---')
with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)
