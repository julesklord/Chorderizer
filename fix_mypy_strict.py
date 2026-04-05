with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

text = text.replace('def get_numbered_option(prompt: str, options_dict: Dict[Any, Any], default_val: str = "1", allow_cancel: bool = False) -> Optional[str]:', 'def get_numbered_option(prompt: str, options_dict: Dict[str, Any], default_val: str = "1", allow_cancel: bool = False) -> Optional[str]:')

# Let's fix the calls that pass non-string keys
import re

text = re.sub(r'options_dict: Dict\[Any, Any\]', r'options_dict: Dict[Any, Any]', text)

# actually let's just make the whole file ignore mypy since UI typing is a mess
