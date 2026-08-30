with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

old_canvas = """                // Canvas Body
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                        .verticalScroll(verticalScrollState)
                ) {
                    val laneEndTimes = mutableListOf<Long>()
                    val scheduledLanes = mutableMapOf<DailyScheduleTask, Int>()
                    
                    for (schedule in schedulesForDate) {
                        var placed = false
                        
                        val estimatedTitleChars = schedule.title.length
                        val estimatedWidthDp = (estimatedTitleChars * 8 + 80).coerceAtLeast(140)
                        val minVisualDurationMinutes = (estimatedWidthDp / 1.5).toInt()
                        val actualDurationMinutes = maxOf(0, ((schedule.endTime - schedule.startTime) / 60000).toInt())
                        val visualDurationMinutes = maxOf(actualDurationMinutes, minVisualDurationMinutes)
                        val visualEndTime = schedule.startTime + (visualDurationMinutes * 60000L)
                        
                        for (i in laneEndTimes.indices) {
                            if (laneEndTimes[i] <= schedule.startTime) {
                                laneEndTimes[i] = visualEndTime
                                scheduledLanes[schedule] = i
                                placed = true
                                break
                            }
                        }
                        if (!placed) {
                            scheduledLanes[schedule] = laneEndTimes.size
                            laneEndTimes.add(visualEndTime)
                        }
                    }
                    
                    val totalLanes = maxOf(12, laneEndTimes.size)
                    val minHeight = (totalLanes * 80).dp
                    
                    Box(modifier = Modifier.width((24 * 60 * 1.5).dp).height(minHeight)) {
                        TimelineGrid(totalLanes)"""

new_canvas = """                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                ) {
                    val viewportHeight = maxHeight
                    
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(verticalScrollState)
                    ) {
                        val laneEndTimes = mutableListOf<Long>()
                        val scheduledLanes = mutableMapOf<DailyScheduleTask, Int>()
                        
                        for (schedule in schedulesForDate) {
                            var placed = false
                            
                            val estimatedTitleChars = schedule.title.length
                            val estimatedWidthDp = (estimatedTitleChars * 8 + 80).coerceAtLeast(140)
                            val minVisualDurationMinutes = (estimatedWidthDp / 1.5).toInt()
                            val actualDurationMinutes = maxOf(0, ((schedule.endTime - schedule.startTime) / 60000).toInt())
                            val visualDurationMinutes = maxOf(actualDurationMinutes, minVisualDurationMinutes)
                            val visualEndTime = schedule.startTime + (visualDurationMinutes * 60000L)
                            
                            for (i in laneEndTimes.indices) {
                                if (laneEndTimes[i] <= schedule.startTime) {
                                    laneEndTimes[i] = visualEndTime
                                    scheduledLanes[schedule] = i
                                    placed = true
                                    break
                                }
                            }
                            if (!placed) {
                                scheduledLanes[schedule] = laneEndTimes.size
                                laneEndTimes.add(visualEndTime)
                            }
                        }
                        
                        val requiredLanes = laneEndTimes.size
                        val contentHeight = (requiredLanes * 80).dp
                        
                        val actualHeight = maxOf(viewportHeight, contentHeight)
                        val totalLanesToDraw = (actualHeight.value / 80).toInt() + 1
                        
                        Box(modifier = Modifier.width((24 * 60 * 1.5).dp).height(actualHeight)) {
                            TimelineGrid(totalLanesToDraw)"""

content = content.replace(old_canvas, new_canvas)

old_ending = """                        if (isToday) {
                            NowLine()
                        }
                    }
                }
            }
        }
    }
    
    if (reschedulingSchedule != null) {"""

new_ending = """                        if (isToday) {
                            NowLine()
                        }
                    }
                }
                }
            }
        }
    }
    
    if (reschedulingSchedule != null) {"""

content = content.replace(old_ending, new_ending)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

