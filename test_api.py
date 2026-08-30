with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

import re
print("Found SwipeToDismissBoxState usages:")
for line in content.splitlines():
    if "dismissState." in line:
        print(line.strip())
