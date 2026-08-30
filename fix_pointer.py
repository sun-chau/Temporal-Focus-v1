import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add imports if they don't exist
imports = """
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.ui.input.pointer.positionChange
"""

# add imports near the top
if "import androidx.compose.ui.input.pointer.positionChange" not in content:
    content = content.replace("import androidx.compose.foundation.horizontalScroll", imports.strip() + "\nimport androidx.compose.foundation.horizontalScroll")

# replace the pointerInput code
pattern = r'\.pointerInput\(horizontalScrollState\.canScrollForward, horizontalScrollState\.canScrollBackward\) \{.*?\n\s*\}'

new_code = """
                        .pointerInput(horizontalScrollState.canScrollForward, horizontalScrollState.canScrollBackward) {
                            awaitPointerEventScope {
                                while(true) {
                                    val down = awaitFirstDown(requireUnconsumed = false)
                                    var isHandlingOverscroll = false
                                    
                                    do {
                                        val event = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Final)
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
                            }
                        }"""

content = re.sub(pattern, new_code.strip(), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

print("Pointer code replaced")
