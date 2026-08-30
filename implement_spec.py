import sys

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

start_marker = "            var overscrollOffset by remember { mutableStateOf(0f) }"
end_marker = "                // Timeline Ruler"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    sys.exit(1)

new_code = """
            var overscrollOffset by remember { mutableStateOf(0f) }
            val density = androidx.compose.ui.platform.LocalDensity.current
            val activationThreshold = with(density) { 80.dp.toPx() }
            val isThresholdCrossed by remember { androidx.compose.runtime.derivedStateOf { kotlin.math.abs(overscrollOffset) >= activationThreshold } }
            
            val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
            val coroutineScope = rememberCoroutineScope()
            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .pointerInput(Unit) {
                        androidx.compose.foundation.gestures.detectHorizontalDragGestures(
                            onDragEnd = {
                                if (isThresholdCrossed) {
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
                            },
                            onDragCancel = {
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
                            },
                            onHorizontalDrag = { change, dragAmount ->
                                val isLeftEdgeLock = horizontalScrollState.value == 0
                                val isRightEdgeLock = horizontalScrollState.value == horizontalScrollState.maxValue
                                
                                if (isLeftEdgeLock && dragAmount > 0) {
                                    overscrollOffset += dragAmount * 0.3f
                                    change.consume()
                                } else if (isRightEdgeLock && dragAmount < 0) {
                                    overscrollOffset += dragAmount * 0.3f
                                    change.consume()
                                } else if (overscrollOffset != 0f) {
                                    // If we're already overscrolling, continue accumulating but respect direction
                                    if ((overscrollOffset > 0 && dragAmount < 0) || (overscrollOffset < 0 && dragAmount > 0)) {
                                        overscrollOffset += dragAmount * 0.3f
                                        // Snap back to 0 if we cross it
                                        if (overscrollOffset > 0 && dragAmount > 0) overscrollOffset = 0f
                                        if (overscrollOffset < 0 && dragAmount < 0) overscrollOffset = 0f
                                        change.consume()
                                    } else {
                                        overscrollOffset += dragAmount * 0.3f
                                        change.consume()
                                    }
                                }
                            }
                        )
                    }
            ) {
                // Add visual overscroll indicator (The Peek UI)
                if (overscrollOffset != 0f) {
                    val isLeft = overscrollOffset > 0f
                    val peekWidth = with(density) { kotlin.math.abs(overscrollOffset).toDp() }
                    
                    Box(
                        modifier = Modifier
                            .align(if (isLeft) Alignment.CenterStart else Alignment.CenterEnd)
                            .width(minOf(peekWidth, 120.dp))
                            .fillMaxHeight()
                            .background(
                                color = if (isThresholdCrossed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                shape = if (isLeft) RoundedCornerShape(topEnd = 100.dp, bottomEnd = 100.dp) else RoundedCornerShape(topStart = 100.dp, bottomStart = 100.dp)
                            )
                            .padding(horizontal = 16.dp),
                        contentAlignment = if (isLeft) Alignment.CenterStart else Alignment.CenterEnd
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            modifier = Modifier.offset(x = if (isThresholdCrossed) (if (isLeft) 4.dp else (-4).dp) else 0.dp)
                        ) {
                            if (!isLeft) {
                                Text(
                                    text = "Tomorrow",
                                    color = if (isThresholdCrossed) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                            
                            val icon = if (isLeft) androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowLeft else androidx.compose.material.icons.Icons.AutoMirrored.Filled.KeyboardArrowRight
                            val tint = if (isThresholdCrossed) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            Icon(icon, contentDescription = "Navigate", tint = tint, modifier = Modifier.size(24.dp))
                            
                            if (isLeft) {
                                Text(
                                    text = "Yesterday",
                                    color = if (isThresholdCrossed) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }
                }
            
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
                        .horizontalScroll(horizontalScrollState)
                ) {
"""

content = content[:start_idx] + new_code + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Applied successfully.")
