with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

import re
pattern = r'\}\n\s*\}\s*\n\s*\}\s*\n\s*\}\s*\n\s*\}\s*\n\s*if \(reschedulingSchedule != null\)'
replacement = "}\n    }\n    }\n    if (reschedulingSchedule != null)"

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
