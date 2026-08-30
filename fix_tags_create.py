import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

content = content.replace('label = { Text(tag) }', 'label = { Text(tag.split("|")[0]) }')

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
