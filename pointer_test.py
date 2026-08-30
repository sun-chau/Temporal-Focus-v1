import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

print("nestedScrollConnection present:", "nestedScrollConnection" in content)
