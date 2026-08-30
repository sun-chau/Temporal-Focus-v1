import re

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "r") as f:
    content = f.read()

bad_str = '''                        )
                } else {'''

good_str = '''                        )
                    }
                } else {'''

content = content.replace(bad_str, good_str)

with open("app/src/main/java/com/example/ui/screens/LoginScreen.kt", "w") as f:
    f.write(content)
