import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

box_start = """            val threshold = 150f
            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {"""

box_start_2 = """            val threshold = 150f

            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {"""

overlay_injection = """
                // Left Edge Swipe Zone
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterStart)
                        .width(40.dp)
                        .fillMaxHeight()
                        .zIndex(10f)
                        .pointerInput(Unit) {
                            androidx.compose.foundation.gestures.detectHorizontalDragGestures(
                                onDragEnd = {
                                    if (overscrollOffset > threshold) {
                                        selectedDateMillis -= 24 * 60 * 60 * 1000L
                                    }
                                    overscrollOffset = 0f
                                    hasVibrated = false
                                },
                                onHorizontalDrag = { change, dragAmount ->
                                    if (dragAmount > 0f || overscrollOffset > 0f) {
                                        overscrollOffset += dragAmount * 0.5f
                                        change.consume()
                                        if (overscrollOffset >= threshold && !hasVibrated) {
                                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                            hasVibrated = true
                                        } else if (overscrollOffset < threshold) {
                                            hasVibrated = false
                                        }
                                    }
                                }
                            )
                        }
                )
                
                // Right Edge Swipe Zone
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterEnd)
                        .width(40.dp)
                        .fillMaxHeight()
                        .zIndex(10f)
                        .pointerInput(Unit) {
                            androidx.compose.foundation.gestures.detectHorizontalDragGestures(
                                onDragEnd = {
                                    if (overscrollOffset < -threshold) {
                                        selectedDateMillis += 24 * 60 * 60 * 1000L
                                    }
                                    overscrollOffset = 0f
                                    hasVibrated = false
                                },
                                onHorizontalDrag = { change, dragAmount ->
                                    if (dragAmount < 0f || overscrollOffset < 0f) {
                                        overscrollOffset += dragAmount * 0.5f
                                        change.consume()
                                        if (kotlin.math.abs(overscrollOffset) >= threshold && !hasVibrated) {
                                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                            hasVibrated = true
                                        } else if (kotlin.math.abs(overscrollOffset) < threshold) {
                                            hasVibrated = false
                                        }
                                    }
                                }
                            )
                        }
                )
"""

if box_start in content:
    content = content.replace(box_start, box_start + overlay_injection)
elif box_start_2 in content:
    content = content.replace(box_start_2, box_start_2 + overlay_injection)
else:
    # Just find `.fillMaxWidth()\n            ) {`
    target = ".fillMaxWidth()\n            ) {"
    if target in content:
        content = content.replace(target, target + overlay_injection)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Finished")
