with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_call_1 = """                            ScheduleBlock(
                                alignTextEnd = alignTextEnd,
                                isWarning = isWarning,
                                elevation = if (isDragging) 8.dp else 0.dp,
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,
                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                modifier = Modifier"""

new_call_1 = """                            ScheduleBlock(
                                alignTextEnd = alignTextEnd,
                                isWarning = isWarning,
                                elevation = if (isDragging) 8.dp else 0.dp,
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,
                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                pageDateMillis = pageDateMillis,
                                modifier = Modifier"""

if old_call_1 in content:
    content = content.replace(old_call_1, new_call_1)
    print("Replaced!")
else:
    print("Not found!")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
