import os


class IconManager:
    # Nerd Font glyphs (hex)
    NERD_GLYPHS = {
        "rocket": "\uf135",
        "book": "\uf02d",
        "plus": "\uf067",
        "broom": "\uf51a",
        "piano": "\ue624",
        "guitar": "\ue623",
        "warn": "\uf071",
        "error": "\uf00d",
        "midi": "\uf001",
        "gear": "\uf013",
        "tonic": "\uf0a4",
        "scale": "\uf0ce",
        "ext": "\uf1b2",
        "inv": "\uf021",
        "manual": "\uf128",
        "quit": "\uf011",
        "chord": "\uf001",
        "list": "\uf03a",
        "check": "\uf00c",
        "dot": "\uf111",
        "view": "\uf06e",
        "jam": "\ufb1e",
        "music": "\uf001",
    }

    # Standard fallback characters
    STANDARD_GLYPHS = {
        "rocket": ">>",
        "book": "i",
        "plus": "+",
        "broom": "x",
        "piano": "P",
        "guitar": "G",
        "warn": "!",
        "error": "X",
        "midi": "M",
        "gear": "*",
        "tonic": "T",
        "scale": "S",
        "ext": "E",
        "inv": "I",
        "manual": "?",
        "quit": "Q",
        "chord": "C",
        "list": "L",
        "check": "v",
        "dot": "●",
        "view": "V",
        "jam": "J",
        "music": "M",
    }

    _has_nerd = None

    @classmethod
    def has_nerd_font(cls):
        if cls._has_nerd is not None:
            return cls._has_nerd

        # Heuristic detection
        # 1. Check env vars
        if os.environ.get("NERD_FONTS") == "1":
            cls._has_nerd = True
            return True

        # 2. Check for modern terminal emulators that often have NF
        term = os.environ.get("TERM", "").lower()
        emul = os.environ.get("TERMINAL_EMULATOR", "").lower()
        if any(x in term for x in ["wezterm", "kitty", "alacritty", "foot"]):
            cls._has_nerd = True
            return True
        if emul == "jetbrains-cli":
            cls._has_nerd = False  # Often doesn't have it by default
            return False

        # On Windows, Windows Terminal often has it if configured, but we can't know.
        # We will default to False but allow override via env var.
        cls._has_nerd = False
        return cls._has_nerd

    @classmethod
    def get(cls, key):
        if cls.has_nerd_font():
            return cls.NERD_GLYPHS.get(key, cls.STANDARD_GLYPHS.get(key, ""))
        return cls.STANDARD_GLYPHS.get(key, "")
