import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Remove onDragCancel completely
import re
content = re.sub(r'onDragCancel\s*=\s*\{\s*overscrollOffset\s*=\s*0f\s*hasVibrated\s*=\s*false\s*\},', '', content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
