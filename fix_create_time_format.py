import sys

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

helper_fn = """
fun formatTime(hourOfDay: Int, minute: Int, use24HourFormat: Boolean): String {
    return if (use24HourFormat) {
        String.format("%02d:%02d", hourOfDay, minute)
    } else {
        val hour = if (hourOfDay == 0) 12 else if (hourOfDay > 12) hourOfDay - 12 else hourOfDay
        val amPm = if (hourOfDay >= 12) "PM" else "AM"
        String.format("%02d:%02d %s", hour, minute, amPm)
    }
}
"""

if "fun formatTime(" not in content:
    content = content + "\n" + helper_fn

content = content.replace(
    'val startText = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))',
    'val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), uiState.use24HourFormat)'
)
content = content.replace(
    'val endText = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))',
    'val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), uiState.use24HourFormat)'
)

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)
