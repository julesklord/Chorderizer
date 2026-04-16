# VHS tape script for Chorderizer PRO Demo
Output demo.gif

Set Shell "pwsh"
Set FontSize 18
Set Width 1200
Set Height 900
Set Padding 30
Set Theme "Catppuccin Mocha"

# Start the app
Type ".venv\Scripts\python.exe -m chorderizer.chorderizer"
Enter
Sleep 4s

# Welcome message should be visible in the console
# Navigate Sidebar to change Tonic
Tab 2
Sleep 500ms
Type "j"
Sleep 500ms
Enter
Sleep 1s

# Change Scale (Down to Dorian)
Tab
Type "jjjj" 
Sleep 500ms
Enter
Sleep 1s

# Toggle Extensions (Down to 7ths)
Tab
Type "jj"
Type " "
Sleep 1s

# Navigate to Chord Table (Select and Add)
Tab 8
Sleep 800ms
Type "j"
Sleep 500ms
Type "a"
Sleep 800ms
Type "j"
Type "a"
Sleep 800ms
Type "j"
Type "a"
Sleep 1.5s

# Show Manual
Type "h"
Sleep 3s
Type "escape"
Sleep 1s

# Export MIDI
Type "e"
Sleep 2s

# Exit
Type "q"
Sleep 1s
