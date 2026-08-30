import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                        if (isCreatingGhost) {
                            val startCal = Calendar.getInstance().apply { timeInMillis = ghostStartTimeMillis }
                            val startMinutes = if (ghostStartTimeMillis < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            val endMinutes = if (ghostEndTimeMillis > endOfDay) 24 * 60 else {
                                val endCal = Calendar.getInstance().apply { timeInMillis = ghostEndTimeMillis }
                                endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                            }
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)"""

replacement = """                        if (isCreatingGhost) {
                            val startMinutes = ((ghostStartTimeMillis - startOfDay) / 60000L).toInt()
                            val endMinutes = ((ghostEndTimeMillis - startOfDay) / 60000L).toInt()
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
