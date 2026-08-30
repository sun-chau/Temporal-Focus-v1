import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

loop_start_pattern = r"for \(schedule in schedulesForDate\) \{"
loop_start_replace = """for (schedule in schedulesForDate) {
                            val isDragging = dragTaskId == schedule.id
                            
                            val lane = if (isDragging) dragLaneIndex else schedule.laneIndex
                            val effectiveStartTime = if (isDragging) dragStartTimeMillis else schedule.startTime
                            val effectiveEndTime = if (isDragging) dragEndTimeMillis else schedule.endTime
                            
                            val actualStart = maxOf(startOfDay, effectiveStartTime)
                            val actualEnd = minOf(endOfDay + 1, effectiveEndTime)
                            
                            val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                            val startMinutes = if (effectiveStartTime < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            
                            val endMinutes = if (effectiveEndTime > endOfDay) 24 * 60 else {
                                val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                                endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                            }
                            
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            
                            val xOffset = (startMinutes * 1.5f).dp
                            val yOffset = (lane * 80 + 4).dp
                            val width = (durationMinutes * 1.5f).dp
                            
                            val isBleedLeft = effectiveStartTime < startOfDay
                            val isBleedRight = effectiveEndTime > endOfDay
                            
                            val isWarning = isDragging && isDragColliding && dragLaneIndex == dragOriginalLane
                            """

# We need to replace everything from `val lane = schedule.laneIndex` up to `val isBleedRight = schedule.endTime > endOfDay`
# Because I'll just write a script to replace the whole block manually to avoid regex errors.
