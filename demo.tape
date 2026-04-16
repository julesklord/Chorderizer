# VHS tape script for Chorderizer PRO Demo
Output demo.gif

Set Shell "pwsh"
Set FontSize 16
Set Width 1200
Set Height 800
Set Padding 20
Set Theme "Catppuccin Mocha"

# Start the app
Type ".venv\Scripts\python.exe -m chorderizer.chorderizer"
Enter
Sleep 3s

# Welcome message should be visible in the console
# Navigate Sidebar
Tab 2
Sleep 500ms
Type "j"
Sleep 500ms
Enter
Sleep 1s

# Change Scale
Tab
Type "jj" 
Sleep 500ms
Enter
Sleep 1s

# Toggle Extensions
Tab
Type " " # Select 6ths
Sleep 500ms
Type "j"
Sleep 200ms
Type " " # Select 7ths
Sleep 1s

# Navigate to Chord Table
Tab 8
Sleep 500ms
Type "j"
Sleep 500ms
Type "j"
Sleep 1s

# Visualizers (Piano/Fretboard) should be updating
# Add to progression
Type "a"
Sleep 800ms
Type "j"
Type "a"
Sleep 800ms
Type "j"
Type "a"
Sleep 1s

# Export MIDI
Type "e"
Sleep 2s

# Show Manual
Type "h"
Sleep 3s
Type "escape"
Sleep 1s

# Exit
Type "q"
Sleep 1s
