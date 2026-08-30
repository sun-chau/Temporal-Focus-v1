import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Use regex to find the pointerInput block and the Box definition.
# It starts at: Box(\n                modifier = Modifier\n                    .weight(1f)\n                    .fillMaxWidth()
# It ends at: ) {  right before // Add visual overscroll indicator (The Peek UI)

pattern = r'(Box\(\s*modifier = Modifier\s*\.weight\(1f\)\s*\.fillMaxWidth\(\)\s*).*?(\)\s*\{\s*// Add visual overscroll indicator \(The Peek UI\))'

replacement = """val nestedScrollConnection = remember {
            object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): androidx.compose.ui.geometry.Offset {
                    if (overscrollOffset != 0f) {
                        val oldOffset = overscrollOffset
                        val newOffset = oldOffset + available.x * 0.3f
                        if ((oldOffset > 0 && newOffset < 0) || (oldOffset < 0 && newOffset > 0)) {
                            overscrollOffset = 0f
                            return androidx.compose.ui.geometry.Offset(available.x - (newOffset / 0.3f), 0f)
                        } else {
                            overscrollOffset = newOffset
                            return androidx.compose.ui.geometry.Offset(available.x, 0f)
                        }
                    }
                    return androidx.compose.ui.geometry.Offset.Zero
                }

                override fun onPostScroll(
                    consumed: androidx.compose.ui.geometry.Offset,
                    available: androidx.compose.ui.geometry.Offset,
                    source: androidx.compose.ui.input.nestedscroll.NestedScrollSource
                ): androidx.compose.ui.geometry.Offset {
                    if (available.x != 0f) {
                        overscrollOffset += available.x * 0.3f
                        return androidx.compose.ui.geometry.Offset(available.x, 0f)
                    }
                    return androidx.compose.ui.geometry.Offset.Zero
                }
                
                override suspend fun onPreFling(available: androidx.compose.ui.unit.Velocity): androidx.compose.ui.unit.Velocity {
                    if (overscrollOffset != 0f) {
                        if (kotlin.math.abs(overscrollOffset) >= activationThreshold) {
                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                            if (overscrollOffset > 0) {
                                selectedDateMillis -= 24 * 60 * 60 * 1000L
                            } else {
                                selectedDateMillis += 24 * 60 * 60 * 1000L
                            }
                            overscrollOffset = 0f
                        } else {
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
                        return androidx.compose.ui.unit.Velocity(available.x, 0f)
                    }
                    return androidx.compose.ui.unit.Velocity.Zero
                }
            }
        }
        
        Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .androidx.compose.ui.input.nestedscroll.nestedScroll(nestedScrollConnection)\n        ) {
                // Add visual overscroll indicator (The Peek UI)"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
