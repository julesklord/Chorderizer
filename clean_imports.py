with open("src/chorderizer/chorderizer.py", "r") as f:
    text = f.read()

text = text.replace("import random\n", "")
text = text.replace("from typing import Any, Dict, List, Optional, Tuple", "from typing import Any, Dict, List")
text = text.replace("    get_numbered_option,\n", "")
text = text.replace("    print_operation_cancelled,\n", "")

with open("src/chorderizer/chorderizer.py", "w") as f:
    f.write(text)
