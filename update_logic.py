import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Add getSemanticTime function
semantic_time_func = """
fun getSemanticTime(timeMillis: Long, pageDateMillis: Long, use24HourFormat: Boolean): String {
    val cal = java.util.Calendar.getInstance().apply { timeInMillis = timeMillis }
    val hour = cal.get(java.util.Calendar.HOUR_OF_DAY)
    val minute = cal.get(java.util.Calendar.MINUTE)
    
    val timeOnly = formatTime(hour, minute, use24HourFormat)
    
    val timestampStartOfDay = getStartOfDayMillis(timeMillis)
    val pageStartOfDay = getStartOfDayMillis(pageDateMillis)
    
    val diffMillis = timestampStartOfDay - pageStartOfDay
    val delta = Math.round(diffMillis.toDouble() / (24 * 60 * 60 * 1000L)).toInt()
    
    return when (delta) {
        0 -> timeOnly
        -1 -> "$timeOnly Yesterday"
        1 -> "$timeOnly Tomorrow"
        else -> {
            val day = cal.get(java.util.Calendar.DAY_OF_MONTH)
            val suffix = when {
                day in 11..13 -> "th"
                day % 10 == 1 -> "st"
                day % 10 == 2 -> "nd"
                day % 10 == 3 -> "rd"
                else -> "th"
            }
            val month = cal.getDisplayName(java.util.Calendar.MONTH, java.util.Calendar.LONG, java.util.Locale.getDefault())
            "$timeOnly, ${day}${suffix} $month"
        }
    }
}
"""

if "fun getSemanticTime" not in content:
    content = content.replace("private fun formatTime(hourOfDay: Int, minute: Int, use24HourFormat: Boolean): String {", semantic_time_func + "\nprivate fun formatTime(hourOfDay: Int, minute: Int, use24HourFormat: Boolean): String {")
    print("Added getSemanticTime")

# 2. Update ScheduleBlock signature
old_sig = """fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,
    coloredCategoriesEnabled: Boolean,
    use24HourFormat: Boolean,
    isBleedLeft: Boolean,
    isBleedRight: Boolean,
    isWarning: Boolean = false,
    elevation: androidx.compose.ui.unit.Dp = 0.dp,
    modifier: Modifier,
    blockWidth: androidx.compose.ui.unit.Dp,"""

new_sig = """fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,
    coloredCategoriesEnabled: Boolean,
    use24HourFormat: Boolean,
    isBleedLeft: Boolean,
    isBleedRight: Boolean,
    isWarning: Boolean = false,
    elevation: androidx.compose.ui.unit.Dp = 0.dp,
    modifier: Modifier,
    blockWidth: androidx.compose.ui.unit.Dp,
    pageDateMillis: Long,"""

if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("Updated ScheduleBlock signature")

# 3. Update ScheduleBlock logic
old_block_logic = """    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), use24HourFormat)
    val endStr = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), use24HourFormat)"""

new_block_logic = """    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = getSemanticTime(schedule.startTime, pageDateMillis, use24HourFormat)
    val endStr = getSemanticTime(schedule.endTime, pageDateMillis, use24HourFormat)"""

if old_block_logic in content:
    content = content.replace(old_block_logic, new_block_logic)
    print("Updated ScheduleBlock inner logic")

# 4. Update ScheduleBlock calls
# At line 334 approx
old_call_1 = """                            ScheduleBlock(
                                alignTextEnd = alignTextEnd,
                                isWarning = isWarning,
                                elevation = if (isDragging) 8.dp else 0.dp,
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,
                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                modifier = Modifier
                                    .offset(x = xOffset, y = yOffset)
                                    .pointerInput(schedule.id) {"""

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
                                modifier = Modifier
                                    .offset(x = xOffset, y = yOffset)
                                    .pointerInput(schedule.id) {"""

if old_call_1 in content:
    content = content.replace(old_call_1, new_call_1)
    print("Updated call 1")
else:
    print("Did not find call 1, maybe formatting differs")

# At line 1367 approx
old_call_2 = """                ScheduleBlock(
                    alignTextEnd = alignTextEnd,
                    isWarning = false,
                    modifier = Modifier.offset(x = xOffset, y = yOffset),
                    schedule = schedule,
                    coloredCategoriesEnabled = true,
                    use24HourFormat = true,
                    isBleedLeft = isBleedLeft,
                    isBleedRight = isBleedRight,
                    
                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {},
                    onReschedule = {}
                )"""

new_call_2 = """                ScheduleBlock(
                    alignTextEnd = alignTextEnd,
                    isWarning = false,
                    modifier = Modifier.offset(x = xOffset, y = yOffset),
                    schedule = schedule,
                    coloredCategoriesEnabled = true,
                    use24HourFormat = true,
                    isBleedLeft = isBleedLeft,
                    isBleedRight = isBleedRight,
                    pageDateMillis = todayStart,
                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {},
                    onReschedule = {}
                )"""
if old_call_2 in content:
    content = content.replace(old_call_2, new_call_2)
    print("Updated call 2")
else:
    print("Did not find call 2")

# 5. Update ghost block text
old_ghost_text = """                                val startStr = String.format("%02d:%02d", startCal.get(java.util.Calendar.HOUR_OF_DAY), startCal.get(java.util.Calendar.MINUTE))
                                val endCal = java.util.Calendar.getInstance().apply { timeInMillis = ghostEndTimeMillis }
                                val endStr = String.format("%02d:%02d", endCal.get(java.util.Calendar.HOUR_OF_DAY), endCal.get(java.util.Calendar.MINUTE))
                                androidx.compose.material3.Text(
                                    text = "$startStr - $endStr","""

new_ghost_text = """                                val startStr = getSemanticTime(ghostStartTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                val endStr = getSemanticTime(ghostEndTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                androidx.compose.material3.Text(
                                    text = "$startStr - $endStr","""
if old_ghost_text in content:
    content = content.replace(old_ghost_text, new_ghost_text)
    print("Updated ghost block")
else:
    print("Did not find ghost block text")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

