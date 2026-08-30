import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# We need to reach depth 0. We currently are at -2. So we need to REMOVE two closing braces before `if (reschedulingSchedule != null)`
pattern = r'\}\n\s*\}\s*\n\s*if \(reschedulingSchedule != null\)'
content = re.sub(pattern, r'\n    if (reschedulingSchedule != null)', content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
