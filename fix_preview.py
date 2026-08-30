import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {}
                )"""
replacement = """                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {},
                    onReschedule = {}
                )"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
