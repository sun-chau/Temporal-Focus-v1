with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()
import re
if "horizontalScroll" in content:
    print("horizontalScroll is present")
