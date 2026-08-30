import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

box_pattern = r"Box\(modifier = Modifier\.width\(\(24 \* 60 \* 1\.5\)\.dp\)\.height\(actualHeight\)\) \{"

replacement = """Box(modifier = Modifier
                            .width((24 * 60 * 1.5).dp)
                            .height(actualHeight)
                            .pointerInput(selectedDateMillis) {
                                detectDragGesturesAfterLongPress(
                                    onDragStart = { offset ->
                                        if (dragTaskId != null) return@detectDragGesturesAfterLongPress // Don't create ghost if dragging block
                                        
                                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                        
                                        val pxPerMinute = 1.5f * density.density
                                        val minutes = (offset.x / pxPerMinute).toInt()
                                        val snappedMinutes = (minutes / 15) * 15
                                        
                                        val laneHeightPx = 80.dp.toPx()
                                        val lane = (offset.y / laneHeightPx).toInt()
                                        
                                        isCreatingGhost = true
                                        ghostStartTimeMillis = startOfDay + snappedMinutes * 60000L
                                        ghostEndTimeMillis = ghostStartTimeMillis + 15 * 60000L
                                        ghostLaneIndex = lane
                                        ghostInitialDragX = offset.x
                                        
                                        isGhostColliding = schedulesForDate.any { 
                                            it.laneIndex == ghostLaneIndex && 
                                            it.startTime < ghostEndTimeMillis && 
                                            it.endTime > ghostStartTimeMillis 
                                        }
                                    },
                                    onDrag = { change, _ ->
                                        if (!isCreatingGhost) return@detectDragGesturesAfterLongPress
                                        
                                        val pxPerMinute = 1.5f * density.density
                                        val touchMinutes = (change.position.x / pxPerMinute).toInt()
                                        val snappedTouchMinutes = (touchMinutes / 15) * 15
                                        val touchTimeMillis = startOfDay + snappedTouchMinutes * 60000L
                                        
                                        val initialMinutes = (ghostInitialDragX / pxPerMinute).toInt()
                                        val snappedInitialMinutes = (initialMinutes / 15) * 15
                                        val initialTimeMillis = startOfDay + snappedInitialMinutes * 60000L
                                        
                                        if (touchTimeMillis >= initialTimeMillis) {
                                            ghostStartTimeMillis = initialTimeMillis
                                            ghostEndTimeMillis = maxOf(initialTimeMillis + 15 * 60000L, touchTimeMillis + 15 * 60000L)
                                        } else {
                                            ghostEndTimeMillis = initialTimeMillis + 15 * 60000L
                                            ghostStartTimeMillis = touchTimeMillis
                                        }
                                        
                                        isGhostColliding = schedulesForDate.any { 
                                            it.laneIndex == ghostLaneIndex && 
                                            it.startTime < ghostEndTimeMillis && 
                                            it.endTime > ghostStartTimeMillis 
                                        }
                                    },
                                    onDragEnd = {
                                        if (isCreatingGhost) {
                                            if (!isGhostColliding) {
                                                viewModel.updateDailyScheduleDraft(
                                                    com.example.data.DailyScheduleDraft(
                                                        title = "",
                                                        startTime = ghostStartTimeMillis,
                                                        endTime = ghostEndTimeMillis,
                                                        tag = ""
                                                    )
                                                )
                                                viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                                            }
                                            isCreatingGhost = false
                                        }
                                    },
                                    onDragCancel = {
                                        isCreatingGhost = false
                                    }
                                )
                            }
                        ) {"""

content = content.replace(box_pattern, replacement)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
