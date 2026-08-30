import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()
content = content.replace("Int.MAX_VALUE / 2", "50000").replace("Int.MAX_VALUE", "100000")
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
