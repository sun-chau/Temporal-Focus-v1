import sys

# 1. Make formatTime private in DailyScheduleScreen.kt
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("fun formatTime(", "private fun formatTime(")

# 2. Add use24HourFormat to ScheduleCreateSheet in DailyScheduleScreen.kt
# Original:
# fun ScheduleCreateSheet(
#     initialSchedule: DailyScheduleTask?,
#     initialDateMillis: Long,

content = content.replace(
    "fun ScheduleCreateSheet(\n    initialSchedule: DailyScheduleTask?,",
    "fun ScheduleCreateSheet(\n    use24HourFormat: Boolean,\n    initialSchedule: DailyScheduleTask?,"
)

# And when called:
# ScheduleCreateSheet(
#     initialSchedule = scheduleToEdit,

content = content.replace(
    "ScheduleCreateSheet(\n                    initialSchedule = scheduleToEdit,",
    "ScheduleCreateSheet(\n                    use24HourFormat = uiState.use24HourFormat,\n                    initialSchedule = scheduleToEdit,"
)
content = content.replace(
    "ScheduleCreateSheet(\n                    initialSchedule = null,",
    "ScheduleCreateSheet(\n                    use24HourFormat = uiState.use24HourFormat,\n                    initialSchedule = null,"
)


with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

# 3. Make formatTime private in CreateDailyScheduleScreen.kt
with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("fun formatTime(", "private fun formatTime(")

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content2)

