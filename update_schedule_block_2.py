with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target1 = """                ScheduleBlock(
                    isWarning = false,"""

replacement1 = """                val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60

                ScheduleBlock(
                    alignTextEnd = alignTextEnd,
                    isWarning = false,"""

content = content.replace(target1, replacement1)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
