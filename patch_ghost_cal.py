import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                        if (isCreatingGhost) {
                            val startMinutes = ((ghostStartTimeMillis - startOfDay) / 60000L).toInt()
                            val endMinutes = ((ghostEndTimeMillis - startOfDay) / 60000L).toInt()
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)"""

replacement = """                        if (isCreatingGhost) {
                            val startMinutes = ((ghostStartTimeMillis - startOfDay) / 60000L).toInt()
                            val endMinutes = ((ghostEndTimeMillis - startOfDay) / 60000L).toInt()
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            val startCal = Calendar.getInstance().apply { timeInMillis = ghostStartTimeMillis }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
