import sys
import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
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

# Update TimelineRuler
content = content.replace("fun TimelineRuler() {", "fun TimelineRuler(use24HourFormat: Boolean) {")
content = content.replace("TimelineRuler()", "TimelineRuler(uiState.use24HourFormat)")
content = content.replace("text = String.format(\"%02d:00\", hour),", "text = formatTime(hour, 0, use24HourFormat),")

# Update ScheduleBlock
content = content.replace("coloredCategoriesEnabled: Boolean,", "coloredCategoriesEnabled: Boolean,\n    use24HourFormat: Boolean,")
content = content.replace("coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,", "coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,\n                                use24HourFormat = uiState.use24HourFormat,")
content = content.replace(
    'val startStr = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))',
    'val startStr = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), use24HourFormat)'
)
content = content.replace(
    'val endStr = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))',
    'val endStr = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), use24HourFormat)'
)

# Update ScheduleCreateSheet
content = content.replace("fun ScheduleCreateSheet(\n    draft: com.example.data.DailyScheduleDraft,", "fun ScheduleCreateSheet(\n    draft: com.example.data.DailyScheduleDraft,\n    use24HourFormat: Boolean,")
content = content.replace("ScheduleCreateSheet(\n                        draft = uiState.dailyScheduleDraft,", "ScheduleCreateSheet(\n                        draft = uiState.dailyScheduleDraft,\n                        use24HourFormat = uiState.use24HourFormat,")

content = content.replace(
    'val startText = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))',
    'val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), use24HourFormat)'
)
content = content.replace(
    'val endText = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))',
    'val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), use24HourFormat)'
)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
