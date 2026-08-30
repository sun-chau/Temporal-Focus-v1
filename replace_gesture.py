import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Remove the nestedScrollConnection block completely
# It starts at: val nestedScrollConnection = remember {
# It ends exactly before Box( modifier = Modifier.weight(1f).fillMaxWidth().nestedScroll(nestedScrollConnection) )
start_idx = content.find("val nestedScrollConnection = remember {")
end_idx = content.find("Box(\n                modifier = Modifier\n                    .weight(1f)\n                    .fillMaxWidth()\n                    .nestedScroll(nestedScrollConnection)")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]
    content = content.replace(".nestedScroll(nestedScrollConnection)", "")
    
    # Now we need to insert the pointerInput modifier.
    # Where should we add it? Probably on the Box that had nestedScroll, or on the Column that has horizontalScroll.
    # The prompt says "Refactor the pointerInput block to prioritize the scroll state check".
    # We will add it to the Column that has horizontalScroll.
    
    # Let's find the Column:
    # Column(
    #     modifier = Modifier
    #         .fillMaxSize()
    #         .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
    #         .horizontalScroll(horizontalScrollState)
    # ) {
    
    pointer_input_code = """
                        .pointerInput(horizontalScrollState.canScrollForward, horizontalScrollState.canScrollBackward) {
                            androidx.compose.foundation.gestures.awaitEachGesture {
                                val down = androidx.compose.foundation.gestures.awaitFirstDown(requireUnconsumed = false)
                                var isHandlingOverscroll = false
                                
                                do {
                                    val event = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Post)
                                    val dragEvent = event.changes.firstOrNull { it.pressed }
                                    
                                    if (dragEvent != null) {
                                        val delta = dragEvent.positionChange().x
                                        val isConsumed = dragEvent.isConsumed
                                        
                                        if (!isConsumed) {
                                            if (delta > 0 && !horizontalScrollState.canScrollBackward) {
                                                overscrollOffset += delta * 0.5f
                                                isHandlingOverscroll = true
                                                dragEvent.consume()
                                            } else if (delta < 0 && !horizontalScrollState.canScrollForward) {
                                                overscrollOffset += delta * 0.5f
                                                isHandlingOverscroll = true
                                                dragEvent.consume()
                                            } else if (isHandlingOverscroll) {
                                                overscrollOffset += delta * 0.5f
                                                dragEvent.consume()
                                            }
                                        }
                                    }
                                } while (dragEvent != null && dragEvent.pressed)
                                
                                if (isHandlingOverscroll && overscrollOffset != 0f) {
                                    if (kotlin.math.abs(overscrollOffset) >= activationThreshold) {
                                        haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                                        if (overscrollOffset > 0) {
                                            selectedDateMillis -= 24 * 60 * 60 * 1000L
                                        } else {
                                            selectedDateMillis += 24 * 60 * 60 * 1000L
                                        }
                                    }
                                    coroutineScope.launch {
                                        androidx.compose.animation.core.Animatable(overscrollOffset).animateTo(
                                            targetValue = 0f,
                                            animationSpec = androidx.compose.animation.core.spring(
                                                dampingRatio = androidx.compose.animation.core.Spring.DampingRatioMediumBouncy,
                                                stiffness = androidx.compose.animation.core.Spring.StiffnessLow
                                            )
                                        ) {
                                            overscrollOffset = value
                                        }
                                    }
                                }
                            }
                        }"""
    
    col_str = "                        .horizontalScroll(horizontalScrollState)"
    content = content.replace(col_str, col_str + pointer_input_code)
    
    with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
        f.write(content)
    print("Replaced!")
else:
    print("Could not find blocks")

