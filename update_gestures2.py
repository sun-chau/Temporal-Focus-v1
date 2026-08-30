import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Update activationThreshold from 80.dp to 50.dp
content = content.replace("val activationThreshold = with(density) { 80.dp.toPx() }", "val activationThreshold = with(density) { 50.dp.toPx() }")

# 2. Let's just find the whole object block and replace it.
pattern = r'object : androidx\.compose\.ui\.input\.nestedscroll\.NestedScrollConnection \{.*?return androidx\.compose\.ui\.unit\.Velocity\.Zero\s*\}\s*\}'

new_nested_scroll = """object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                @Suppress("DEPRECATION")
                private fun isDrag(source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): Boolean {
                    return source == androidx.compose.ui.input.nestedscroll.NestedScrollSource.UserInput || source == androidx.compose.ui.input.nestedscroll.NestedScrollSource.Drag
                }
                
                override fun onPreScroll(available: androidx.compose.ui.geometry.Offset, source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): androidx.compose.ui.geometry.Offset {
                    if (!isDrag(source)) return androidx.compose.ui.geometry.Offset.Zero
                    if (overscrollOffset != 0f) {
                        val oldOffset = overscrollOffset
                        val newOffset = oldOffset + available.x * 0.5f
                        if ((oldOffset > 0 && newOffset < 0) || (oldOffset < 0 && newOffset > 0)) {
                            overscrollOffset = 0f
                            return androidx.compose.ui.geometry.Offset(available.x - (newOffset / 0.5f), 0f)
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
                    if (!isDrag(source)) return androidx.compose.ui.geometry.Offset.Zero
                    if (available.x != 0f) {
                        overscrollOffset += available.x * 0.5f
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
            }"""

if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, new_nested_scroll, content, flags=re.DOTALL)
    print("Nested Scroll Connection updated")
else:
    print("Nested Scroll Connection NOT found")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

