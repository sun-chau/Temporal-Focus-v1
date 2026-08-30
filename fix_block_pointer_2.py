import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

pattern = r"for \(schedule in schedulesForDate\) \{[\s\S]*?val isBleedRight = schedule\.endTime > endOfDay"
replacement = """for (schedule in schedulesForDate) {
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
                            
                            val isWarning = isDragging && isDragColliding && dragLaneIndex == dragOriginalLane"""

content = re.sub(pattern, replacement, content)

# Now inject pointerInput into ScheduleBlock
schedule_block_pattern = r"ScheduleBlock\(\s*isBleedLeft = isBleedLeft,\s*isBleedRight = isBleedRight,\s*schedule = schedule,\s*coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,\s*use24HourFormat = uiState.use24HourFormat,\s*modifier = Modifier\s*\.offset\(x = xOffset, y = yOffset\)\s*\.height\(72\.dp\),"

schedule_block_replacement = """ScheduleBlock(
                                isWarning = isWarning,
                                elevation = if (isDragging) 8.dp else 0.dp,
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,
                                schedule = schedule,
                                coloredCategoriesEnabled = uiState.coloredCategoriesEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                modifier = Modifier
                                    .offset(x = xOffset, y = yOffset)
                                    .height(72.dp)
                                    .pointerInput(schedule.id) {
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { _ ->
                                                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                                dragTaskId = schedule.id
                                                dragStartTimeMillis = schedule.startTime
                                                dragEndTimeMillis = schedule.endTime
                                                dragLaneIndex = schedule.laneIndex
                                                dragOriginalLane = schedule.laneIndex
                                                accumulatedDragX = 0f
                                                accumulatedDragY = 0f
                                                isDragColliding = false
                                            },
                                            onDrag = { _, dragAmount ->
                                                accumulatedDragX += dragAmount.x
                                                accumulatedDragY += dragAmount.y
                                                
                                                val pxPerMinute = 1.5f * density.density
                                                val dragMinutes = (accumulatedDragX / pxPerMinute).toInt()
                                                val snappedDragMinutes = (dragMinutes / 15) * 15
                                                
                                                dragStartTimeMillis = schedule.startTime + snappedDragMinutes * 60000L
                                                dragEndTimeMillis = schedule.endTime + snappedDragMinutes * 60000L
                                                
                                                val laneHeightPx = 80.dp.toPx()
                                                val dragLanes = (accumulatedDragY / laneHeightPx).toInt()
                                                dragLaneIndex = maxOf(0, dragOriginalLane + dragLanes)
                                                
                                                isDragColliding = schedulesForDate.any { 
                                                    it.id != schedule.id && 
                                                    it.laneIndex == dragLaneIndex && 
                                                    it.startTime < dragEndTimeMillis && 
                                                    it.endTime > dragStartTimeMillis 
                                                }
                                            },
                                            onDragEnd = {
                                                if (dragTaskId != null) {
                                                    if (dragLaneIndex == dragOriginalLane && isDragColliding) {
                                                        // Invalid drop
                                                    } else {
                                                        // Valid drop
                                                        val updated = schedule.copy(
                                                            startTime = dragStartTimeMillis,
                                                            endTime = dragEndTimeMillis,
                                                            laneIndex = dragLaneIndex
                                                        )
                                                        viewModel.updateDailySchedule(updated)
                                                    }
                                                    dragTaskId = null
                                                }
                                            },
                                            onDragCancel = {
                                                dragTaskId = null
                                            }
                                        )
                                    },"""

content = re.sub(schedule_block_pattern, schedule_block_replacement, content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
