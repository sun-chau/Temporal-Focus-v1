import sys
import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Filter update
old_filter = """            val schedulesForDate = uiState.dailySchedules.filter {
                getStartOfDayMillis(it.startTime) == selectedDateMillis
            }.sortedBy { it.startTime }"""

new_filter = """            val startOfDay = selectedDateMillis
            val endOfDay = selectedDateMillis + 24 * 60 * 60 * 1000L - 1L

            val schedulesForDate = uiState.dailySchedules.filter {
                it.startTime <= endOfDay && it.endTime > startOfDay
            }.sortedBy { it.startTime }"""

content = content.replace(old_filter, new_filter)

# Calculation update for lane placement
old_lane_placement = """                        val scheduledLanes = mutableMapOf<DailyScheduleTask, Int>()
                        
                        for (schedule in schedulesForDate) {
                            var placed = false
                            
                            val estimatedTitleChars = schedule.title.length
                            val estimatedWidthDp = (estimatedTitleChars * 8 + 80).coerceAtLeast(140)
                            val minVisualDurationMinutes = (estimatedWidthDp / 1.5).toInt()
                            val actualDurationMinutes = maxOf(0, ((schedule.endTime - schedule.startTime) / 60000).toInt())
                            val visualDurationMinutes = maxOf(actualDurationMinutes, minVisualDurationMinutes)
                            val visualEndTime = schedule.startTime + (visualDurationMinutes * 60000L)"""

new_lane_placement = """                        val scheduledLanes = mutableMapOf<DailyScheduleTask, Int>()
                        
                        for (schedule in schedulesForDate) {
                            var placed = false
                            
                            val estimatedTitleChars = schedule.title.length
                            val estimatedWidthDp = (estimatedTitleChars * 8 + 80).coerceAtLeast(140)
                            val minVisualDurationMinutes = (estimatedWidthDp / 1.5).toInt()
                            
                            val actualStart = maxOf(startOfDay, schedule.startTime)
                            val actualEnd = minOf(endOfDay + 1, schedule.endTime)
                            val actualDurationMinutes = maxOf(0, ((actualEnd - actualStart) / 60000).toInt())
                            val visualDurationMinutes = maxOf(actualDurationMinutes, minVisualDurationMinutes)
                            val visualEndTime = actualStart + (visualDurationMinutes * 60000L)"""

content = content.replace(old_lane_placement, new_lane_placement)

# Update drawing loop
old_drawing = """                        for (schedule in schedulesForDate) {
                            val lane = scheduledLanes[schedule] ?: 0
                            val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
                            val startMinutes = startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            val durationMinutes = maxOf(10, ((schedule.endTime - schedule.startTime) / 60000).toInt())
                            
                            val xOffset = (startMinutes * 1.5f).dp
                            val yOffset = (lane * 80 + 4).dp
                            val width = (durationMinutes * 1.5f).dp
                            
                            ScheduleBlock("""

new_drawing = """                        for (schedule in schedulesForDate) {
                            val lane = scheduledLanes[schedule] ?: 0
                            val actualStart = maxOf(startOfDay, schedule.startTime)
                            val actualEnd = minOf(endOfDay + 1, schedule.endTime)
                            
                            val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                            val startMinutes = if (schedule.startTime < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            
                            val endMinutes = if (schedule.endTime > endOfDay) 24 * 60 else {
                                val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                                endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                            }
                            
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            
                            val xOffset = (startMinutes * 1.5f).dp
                            val yOffset = (lane * 80 + 4).dp
                            val width = (durationMinutes * 1.5f).dp
                            
                            val isBleedLeft = schedule.startTime < startOfDay
                            val isBleedRight = schedule.endTime > endOfDay
                            
                            ScheduleBlock(
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,"""

content = content.replace(old_drawing, new_drawing)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
