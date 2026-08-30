import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("    defaultTag: String = tags.firstOrNull() ?: \"Work\",\n    tags: List<String>,", "    tags: List<String>,\n    defaultTag: String = tags.firstOrNull() ?: \"Work\",")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
