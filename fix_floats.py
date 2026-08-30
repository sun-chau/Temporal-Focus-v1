import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("dragAmount > 0)", "dragAmount > 0f)")
content = content.replace("dragAmount < 0)", "dragAmount < 0f)")
content = content.replace("overscrollOffset > 0", "overscrollOffset > 0f")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
