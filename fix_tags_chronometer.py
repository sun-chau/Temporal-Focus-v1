import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

content = re.sub(
r'Text\(tag\.trim\(\), color = Color\.White, fontSize = 10\.sp\)',
r'Text(tag.split("|")[0].trim(), color = Color.White, fontSize = 10.sp)', content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
