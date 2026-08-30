with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

idx1 = content.find("val laneEndTimes = mutableListOf<Long>()")
idx2 = content.find("val contentHeight = (requiredLanes * 80).dp")

if idx1 != -1 and idx2 != -1:
    new_logic = "val requiredLanes = schedulesForDate.maxOfOrNull { it.laneIndex + 1 } ?: 0\n                        "
    content = content[:idx1] + new_logic + content[idx2:]

content = content.replace("val lane = scheduledLanes[schedule] ?: 0", "val lane = schedule.laneIndex")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
