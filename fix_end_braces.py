import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# We need to add one more brace right before `if (reschedulingSchedule != null)`
pattern = r'(\s*)\}\n\s*if \(reschedulingSchedule != null\)'
content = re.sub(pattern, r'\1}\n\1}\n    if (reschedulingSchedule != null)', content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

