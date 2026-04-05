import re

with open("src/chorderizer/ui.py", "r") as f:
    text = f.read()

# Make get_numbered_option accept dicts of any types
text = text.replace('def get_numbered_option(prompt: str, options_dict: Dict[Any, Any],', 'def get_numbered_option(prompt: str, options_dict: Dict[Any, Any],')
text = text.replace('Dict[Union[str, int], Any]', 'Dict[Any, Any]')

# Make numbers explicit to avoid none/int comparison
text = text.replace('bpm = float(bpm_str) if bpm_str else 120.0', 'bpm: float = float(bpm_str) if bpm_str else 120.0')
text = text.replace('base_vel = int(vel_str) if vel_str else 80', 'base_vel: int = int(vel_str) if vel_str else 80')
text = text.replace('strum_delay = float(strum_str) if strum_str else 0.0', 'strum_delay: float = float(strum_str) if strum_str else 0.0')

text = text.replace('if bpm is not None and not (20 <= bpm <= 300):', 'if not (20.0 <= bpm <= 300.0):')
text = text.replace('bpm = min(max(float(bpm) if bpm is not None else 120.0, 20.0), 300.0)', 'bpm = min(max(bpm, 20.0), 300.0)')

text = text.replace('if base_vel is not None and not (0 <= base_vel <= 127):', 'if not (0 <= base_vel <= 127):')
text = text.replace('base_vel = min(max(int(base_vel) if base_vel is not None else 80, 0), 127)', 'base_vel = min(max(base_vel, 0), 127)')

text = text.replace('if strum_delay is not None and not (0.0 <= strum_delay <= 1.0):', 'if not (0.0 <= strum_delay <= 1.0):')
text = text.replace('strum_delay = min(max(float(strum_delay) if strum_delay is not None else 0.0, 0.0), 1.0)', 'strum_delay = min(max(strum_delay, 0.0), 1.0)')

text = text.replace('if not (0 <= bass_vel <= 127):', 'if bass_vel is not None and not (0 <= float(bass_vel) <= 127):')
text = text.replace('bass_vel = min(max(bass_vel, 0), 127)', 'bass_vel = min(max(int(bass_vel) if bass_vel is not None else 90, 0), 127)')

text = text.replace('int(inst_chords_opt)', 'int(inst_chords_opt if inst_chords_opt is not None else "0")')
text = text.replace('int(inst_bass_opt)', 'int(inst_bass_opt if inst_bass_opt is not None else "33")')

text = text.replace('if not (0 <= inst_chords <= 127):', 'if inst_chords is not None and not (0 <= int(inst_chords) <= 127):')
text = text.replace('if not (0 <= inst_bass <= 127):', 'if inst_bass is not None and not (0 <= int(inst_bass) <= 127):')

text = text.replace('float(arp_dur_opt)', 'float(arp_dur_opt if arp_dur_opt is not None else "0.5")')

with open("src/chorderizer/ui.py", "w") as f:
    f.write(text)
