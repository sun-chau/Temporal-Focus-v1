import re

with open("app/src/main/java/com/example/data/AppDatabase.kt", "r") as f:
    content = f.read()

content = re.sub(r'version = \d+', 'version = 6', content)

with open("app/src/main/java/com/example/data/AppDatabase.kt", "w") as f:
    f.write(content)
