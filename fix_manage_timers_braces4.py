import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

content = content.replace("        }}\n@Composable", "        }\n    }\n}\n\n@Composable")
content = content.replace("        }}@Composable", "        }\n    }\n}\n\n@Composable")

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
