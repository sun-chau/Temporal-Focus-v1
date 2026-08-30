import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Find the wrapper of horizontalScroll
target = """            Column(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .horizontalScroll(horizontalScrollState)
            ) {"""

if target not in content:
    print("Could not find horizontalScroll target")
    sys.exit(1)

new_target = """
            var overscrollOffset by remember { mutableStateOf(0f) }
            val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
            var hasVibrated by remember { mutableStateOf(false) }
            val coroutineScope = rememberCoroutineScope()
            
            val threshold = 150f
            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .pointerInput(Unit) {
                        androidx.compose.foundation.gestures.detectHorizontalDragGestures(
                            onDragEnd = {
                                if (overscrollOffset > threshold) {
                                    // Navigate to previous day
                                    selectedDateMillis -= 24 * 60 * 60 * 1000L
                                } else if (overscrollOffset < -threshold) {
                                    // Navigate to next day
                                    selectedDateMillis += 24 * 60 * 60 * 1000L
                                }
                                overscrollOffset = 0f
                                hasVibrated = false
                            },
                            onDragCancel = {
                                overscrollOffset = 0f
                                hasVibrated = false
                            },
                            onHorizontalDrag = { change, dragAmount ->
                                if (horizontalScrollState.value == 0 && dragAmount > 0) {
                                    // Pulling from left edge
                                    overscrollOffset += dragAmount * 0.2f
                                    change.consume()
                                } else if (horizontalScrollState.value == horizontalScrollState.maxValue && dragAmount < 0) {
                                    // Pulling from right edge
                                    overscrollOffset += dragAmount * 0.2f
                                    change.consume()
                                }
                                
                                if (kotlin.math.abs(overscrollOffset) >= threshold && !hasVibrated) {
                                    haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                    hasVibrated = true
                                } else if (kotlin.math.abs(overscrollOffset) < threshold) {
                                    hasVibrated = false
                                }
                            }
                        )
                    }
            ) {
                // Add visual overscroll indicator
                if (overscrollOffset != 0f) {
                    val isLeft = overscrollOffset > 0
                    val isThresholdMet = kotlin.math.abs(overscrollOffset) >= threshold
                    
                    val peekWidth = minOf(100f, kotlin.math.abs(overscrollOffset)).dp
                    
                    Box(
                        modifier = Modifier
                            .align(if (isLeft) Alignment.CenterStart else Alignment.CenterEnd)
                            .width(peekWidth)
                            .fillMaxHeight()
                            .background(
                                color = if (isThresholdMet) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                shape = if (isLeft) RoundedCornerShape(topEnd = 100.dp, bottomEnd = 100.dp) else RoundedCornerShape(topStart = 100.dp, bottomStart = 100.dp)
                            )
                            .padding(horizontal = 16.dp),
                        contentAlignment = if (isLeft) Alignment.CenterStart else Alignment.CenterEnd
                    ) {
                        val icon = if (isLeft) androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowLeft else androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight
                        val tint = if (isThresholdMet) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                        Icon(icon, contentDescription = "Navigate", tint = tint, modifier = Modifier.size(32.dp))
                    }
                }
            
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
                    .horizontalScroll(horizontalScrollState)
            ) {"""

content = content.replace(target, new_target)
content = content.replace("TimelineRuler(uiState.use24HourFormat)\n                                \n                                // Canvas Body", "TimelineRuler(uiState.use24HourFormat)\n                                \n                                // Canvas Body")

# we need an extra `}` for the Box wrapper we added.
# Find the end of `Column(modifier = Modifier.weight(1f)...)`
# The easiest way is to find DateNavigator and see where the Column ends.

# Wait, `BoxWithConstraints` ends, then Column ends, then `if (reschedulingSchedule != null)` starts.
# Let's do it via regex
end_target = """                                }
                            }
                        }
                    }
                }
            }
            
            if (reschedulingSchedule != null) {"""

new_end_target = """                                }
                            }
                        }
                    }
                }
            }
            } // Close overscroll Box
            
            if (reschedulingSchedule != null) {"""
content = content.replace(end_target, new_end_target)


with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
