import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Update activationThreshold from 80.dp to 50.dp
content = content.replace("val activationThreshold = with(density) { 80.dp.toPx() }", "val activationThreshold = with(density) { 50.dp.toPx() }")

# 2. Update the nestedScrollConnection Drag check and multipliers
nested_scroll_pattern = r'val nestedScrollConnection = remember \{\s*object : androidx\.compose\.ui\.input\.nestedscroll\.NestedScrollConnection \{.*?\n        \}\n        \}'

new_nested_scroll = """val nestedScrollConnection = remember {
            object : androidx.compose.ui.input.nestedscroll.NestedScrollConnection {
                private fun isDrag(source: androidx.compose.ui.input.nestedscroll.NestedScrollSource): Boolean {
                    val s = source.toString()
                    return s.contains("Drag") || s.contains("UserInput")
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
            }
        }"""

content = re.sub(nested_scroll_pattern, new_nested_scroll, content, flags=re.DOTALL)

# 3. Update the Peek UI to remove text and make icon bigger
row_pattern = r'Row\(\s*verticalAlignment = Alignment\.CenterVertically.*?modifier = Modifier\.offset\(x = if \(isThresholdCrossed\) \(if \(isLeft\) 4\.dp else \(-4\)\.dp\) else 0\.dp\)\s*\) \{.*?\}\s*\}'

new_row = """Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.Center,
                            modifier = Modifier.offset(x = if (isThresholdCrossed) (if (isLeft) 6.dp else (-6).dp) else 0.dp)
                        ) {
                            val icon = if (isLeft) androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowLeft else androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight
                            val tint = if (isThresholdCrossed) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            Icon(icon, contentDescription = "Navigate", tint = tint, modifier = Modifier.size(36.dp))
                        }
                    }"""

content = re.sub(row_pattern, new_row, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

print("Update applied")
