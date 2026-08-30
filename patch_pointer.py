import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.compose.ui.input.pointer.PointerInputChange
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.awaitLongPressOrCancellation
import androidx.compose.foundation.gestures.drag
import kotlinx.coroutines.CancellationException"""

content = content.replace("import androidx.compose.ui.input.pointer.pointerInput", "import androidx.compose.ui.input.pointer.pointerInput\n" + imports)

# Find detectDragGesturesAfterLongPress usage for tasks
target_task = """                                        detectDragGesturesAfterLongPress(
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
                                            onDragEnd = {
                                                if (dragTaskId != null) {
                                                    if (!isDragColliding) {
                                                        viewModel.updateDailySchedule(
                                                            schedule.copy(
                                                                startTime = dragStartTimeMillis,
                                                                endTime = dragEndTimeMillis,
                                                                laneIndex = dragLaneIndex
                                                            )
                                                        )
                                                    }
                                                    dragTaskId = null
                                                }
                                            },
                                            onDragCancel = {
                                                dragTaskId = null
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
                                                val laneOffset = (accumulatedDragY / laneHeightPx).toInt()
                                                dragLaneIndex = maxOf(0, dragOriginalLane + laneOffset)
                                                
                                                isDragColliding = schedulesForDate.any {
                                                    it.id != schedule.id && 
                                                    it.laneIndex == dragLaneIndex && 
                                                    it.startTime < dragEndTimeMillis && 
                                                    it.endTime > dragStartTimeMillis 
                                                }
                                            }
                                        )"""

replacement_task = """                                        awaitEachGesture {
                                            val down = awaitFirstDown(requireUnconsumed = false)
                                            val longPress = awaitLongPressOrCancellation(down.id)
                                            if (longPress != null) {
                                                longPress.consume()
                                                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                                dragTaskId = schedule.id
                                                dragStartTimeMillis = schedule.startTime
                                                dragEndTimeMillis = schedule.endTime
                                                dragLaneIndex = schedule.laneIndex
                                                dragOriginalLane = schedule.laneIndex
                                                accumulatedDragX = 0f
                                                accumulatedDragY = 0f
                                                isDragColliding = false
                                                
                                                try {
                                                    drag(longPress.id) { change ->
                                                        change.consume()
                                                        val dragAmount = change.positionChange()
                                                        
                                                        accumulatedDragX += dragAmount.x
                                                        accumulatedDragY += dragAmount.y
                                                        
                                                        val pxPerMinute = 1.5f * density.density
                                                        val dragMinutes = (accumulatedDragX / pxPerMinute).toInt()
                                                        val snappedDragMinutes = (dragMinutes / 15) * 15
                                                        
                                                        dragStartTimeMillis = schedule.startTime + snappedDragMinutes * 60000L
                                                        dragEndTimeMillis = schedule.endTime + snappedDragMinutes * 60000L
                                                        
                                                        val laneHeightPx = 80.dp.toPx()
                                                        val laneOffset = (accumulatedDragY / laneHeightPx).toInt()
                                                        dragLaneIndex = maxOf(0, dragOriginalLane + laneOffset)
                                                        
                                                        isDragColliding = schedulesForDate.any {
                                                            it.id != schedule.id && 
                                                            it.laneIndex == dragLaneIndex && 
                                                            it.startTime < dragEndTimeMillis && 
                                                            it.endTime > dragStartTimeMillis 
                                                        }
                                                    }
                                                    
                                                    if (dragTaskId != null) {
                                                        if (!isDragColliding) {
                                                            viewModel.updateDailySchedule(
                                                                schedule.copy(
                                                                    startTime = dragStartTimeMillis,
                                                                    endTime = dragEndTimeMillis,
                                                                    laneIndex = dragLaneIndex
                                                                )
                                                            )
                                                        }
                                                        dragTaskId = null
                                                    }
                                                } catch (c: CancellationException) {
                                                    dragTaskId = null
                                                }
                                            }
                                        }"""

content = content.replace(target_task, replacement_task)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
