import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# I need to restore the original pointerInput logic but move it to overlays.
# First, let's remove the broken pointerInput from the parent Box entirely.

target = """                    .pointerInput(Unit) {
                        androidx.compose.foundation.gestures.awaitEachGesture {
                            val down = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                            var isOverscrolling = false
                            
                            while (true) {
                                val event = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                                if (event.changes.isEmpty() || event.changes.all { !it.pressed }) {
                                    if (isOverscrolling) {
                                        if (overscrollOffset > threshold) {
                                            selectedDateMillis -= 24 * 60 * 60 * 1000L
                                        } else if (overscrollOffset < -threshold) {
                                            selectedDateMillis += 24 * 60 * 60 * 1000L
                                        }
                                        overscrollOffset = 0f
                                        hasVibrated = false
                                    }
                                    break
                                }
                                
                                val change = event.changes.first()
                                val dragAmount = change.position.x - change.previousPosition.x
                                
                                if (horizontalScrollState.value == 0 && (dragAmount > 0 || overscrollOffset > 0)) {
                                    isOverscrolling = true
                                    overscrollOffset += dragAmount * 0.2f
                                    change.consume()
                                } else if (horizontalScrollState.value == horizontalScrollState.maxValue && (dragAmount < 0 || overscrollOffset < 0)) {
                                    isOverscrolling = true
                                    overscrollOffset += dragAmount * 0.2f
                                    change.consume()
                                }
                                
                                if (isOverscrolling) {
                                    if (kotlin.math.abs(overscrollOffset) >= threshold && !hasVibrated) {
                                        haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                        hasVibrated = true
                                    } else if (kotlin.math.abs(overscrollOffset) < threshold) {
                                        hasVibrated = false
                                    }
                                }
                            }
                        }
                    }"""

if target in content:
    content = content.replace(target, "")
else:
    print("Could not find the awaitEachGesture block to remove")

# Now, we need to inject the overlay boxes.
# Find the start of the Box body:
#            val threshold = 150f
#            
#            Box(
#                modifier = Modifier
#                    .weight(1f)
#                    .fillMaxWidth()
#            ) {
#                // Add visual overscroll indicator

overlay_injection = """
                // Left Edge Swipe Zone
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterStart)
                        .width(24.dp)
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
                        .width(24.dp)
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

box_start = """            val threshold = 150f
            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {"""

if box_start in content:
    content = content.replace(box_start, box_start + overlay_injection)
else:
    print("Could not find Box start to inject overlays")

# Also need to import zIndex if it's not imported.
if "import androidx.compose.ui.zIndex" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.zIndex.zIndex")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Finished")
