import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add enableRadioMenu to ScheduleBlock
old_sig = """fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,
    coloredCategoriesEnabled: Boolean,
    use24HourFormat: Boolean,"""

new_sig = """fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,
    coloredCategoriesEnabled: Boolean,
    use24HourFormat: Boolean,
    enableRadioMenu: Boolean = true,"""

content = content.replace(old_sig, new_sig)

# Change clickable behavior
old_click = """.clickable { showStatusMenu = true },"""
new_click = """.clickable { 
                        if (enableRadioMenu) {
                            showStatusMenu = true 
                        } else {
                            val nextStatus = if (status == ScheduleStatus.NOT_DONE) ScheduleStatus.COMPLETED else ScheduleStatus.NOT_DONE
                            onStatusChange(nextStatus)
                        }
                    },"""

content = content.replace(old_click, new_click)

# Pass the property in the two ScheduleBlock usages
old_usage_1 = """                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                pageDateMillis = pageDateMillis,
                                modifier = Modifier"""

new_usage_1 = """                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                enableRadioMenu = uiState.enableDailyScheduleRadioMenu,
                                pageDateMillis = pageDateMillis,
                                modifier = Modifier"""
content = content.replace(old_usage_1, new_usage_1)

old_usage_2 = """                    schedule = schedule,
                    coloredCategoriesEnabled = true,
                    use24HourFormat = true,
                    isBleedLeft = isBleedLeft,"""

new_usage_2 = """                    schedule = schedule,
                    coloredCategoriesEnabled = true,
                    use24HourFormat = true,
                    enableRadioMenu = true,
                    isBleedLeft = isBleedLeft,"""
content = content.replace(old_usage_2, new_usage_2)


with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
