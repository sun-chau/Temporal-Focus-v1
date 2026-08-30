import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Replace all occurrences of 1.5f with 2.0f
content = content.replace("1.5f", "2.0f")
# Replace occurrences of 1.5 with 2.0
content = content.replace("* 1.5)", "* 2.0)")
content = content.replace("* 1.5 ", "* 2.0 ")
content = content.replace("1.5 *", "2.0f *")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Scale updated!")
