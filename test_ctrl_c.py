import pexpect
import sys

child = pexpect.spawn("python3 -m chorderizer.chorderizer", encoding='utf-8', env={"PYTHONPATH": "src"})
child.expect("Choose an option number:")
child.sendintr() # Send Ctrl+C
child.expect("Operation cancelled by the user.") # Should ask again
print("Ctrl+C works fine!")
child.sendcontrol('d')
