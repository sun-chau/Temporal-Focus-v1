import re

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'r') as f:
    content = f.read()

target = """                        // Transparent gesture overlays for vertical dragging
                        Row(
                            modifier = Modifier
                                .padding(top = 20.dp)
                                .height(80.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""

replacement = """                        // Opaque gesture overlays for vertical dragging and smooth clock updates
                        val scope = rememberCoroutineScope()
                        var displayHour by remember { mutableIntStateOf(timePickerState.hour) }
                        var displayMinute by remember { mutableIntStateOf(timePickerState.minute) }
                        var isHourSelected by remember { mutableStateOf(true) }
                        var isDraggingHour by remember { mutableStateOf(false) }
                        var isDraggingMinute by remember { mutableStateOf(false) }
                        var animatingHourTarget: Int? by remember { mutableStateOf(null) }
                        var animatingMinuteTarget: Int? by remember { mutableStateOf(null) }

                        LaunchedEffect(timePickerState.hour) {
                            if (!isDraggingHour && animatingHourTarget == null) {
                                displayHour = timePickerState.hour
                            }
                        }
                        LaunchedEffect(timePickerState.minute) {
                            if (!isDraggingMinute && animatingMinuteTarget == null) {
                                displayMinute = timePickerState.minute
                            }
                        }

                        suspend fun animateClock(state: TimePickerState, isHour: Boolean, targetValue: Int) {
                            val currentValue = if (isHour) state.hour else state.minute
                            if (currentValue == targetValue) return
                            
                            val max = if (isHour) 24 else 60
                            val forwardDistance = (targetValue - currentValue + max) % max
                            val backwardDistance = (currentValue - targetValue + max) % max
                            val step = if (forwardDistance <= backwardDistance) 1 else -1
                            
                            var current = currentValue
                            while (current != targetValue) {
                                current = (current + step + max) % max
                                try {
                                    val prefix = if (isHour) "setHour" else "setMinute"
                                    val method = state.javaClass.methods.firstOrNull { it.name.startsWith(prefix) }
                                    method?.isAccessible = true
                                    method?.invoke(state, current)
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                                kotlinx.coroutines.delay(15)
                            }
                        }

                        Row(
                            modifier = Modifier
                                .padding(top = 20.dp)
                                .height(80.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""

content = content.replace(target, replacement)

target2 = """                            // Hour Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragEnd = { hourDragAccumulator = 0f },
                                            onDragCancel = { hourDragAccumulator = 0f }
                                        ) { change, dragAmount ->
                                            hourDragAccumulator += dragAmount
                                            if (kotlin.math.abs(hourDragAccumulator) >= threshold) {
                                                val steps = (hourDragAccumulator / threshold).toInt()
                                                hourDragAccumulator -= steps * threshold
                                                
                                                var newHour = timePickerState.hour - steps
                                                if (is24Hour) {
                                                    newHour = (newHour % 24 + 24) % 24
                                                } else {
                                                    // In 12-hour mode, TimePickerState.hour is 0-23 internally
                                                    newHour = (newHour % 24 + 24) % 24
                                                }
                                                setTimeReflectively(timePickerState, true, newHour)
                                                hapticFeedback.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            }
                                        }
                                    }
                            )"""

replacement2 = """                            // Hour Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .background(
                                        color = if (isHourSelected) MaterialTheme.colorScheme.primary.copy(alpha = 0.2f) 
                                                else MaterialTheme.colorScheme.surfaceVariant,
                                        shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
                                    )
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        awaitPointerEventScope {
                                            while (true) {
                                                val event = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                                                if (event.changes.any { it.pressed }) {
                                                    isHourSelected = true
                                                }
                                            }
                                        }
                                    }
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragStart = { isDraggingHour = true },
                                            onDragEnd = { 
                                                hourDragAccumulator = 0f 
                                                isDraggingHour = false
                                                animatingHourTarget = displayHour
                                                scope.launch {
                                                    animateClock(timePickerState, true, displayHour)
                                                    animatingHourTarget = null
                                                }
                                            },
                                            onDragCancel = { 
                                                hourDragAccumulator = 0f 
                                                isDraggingHour = false
                                                displayHour = timePickerState.hour
                                            }
                                        ) { change, dragAmount ->
                                            hourDragAccumulator += dragAmount
                                            if (kotlin.math.abs(hourDragAccumulator) >= threshold) {
                                                val steps = (hourDragAccumulator / threshold).toInt()
                                                hourDragAccumulator -= steps * threshold
                                                
                                                displayHour = (displayHour - steps + 24) % 24
                                                hapticFeedback.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            }
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "%02d".format(if (is24Hour) displayHour else {
                                        val h = displayHour % 12
                                        if (h == 0) 12 else h
                                    }),
                                    style = MaterialTheme.typography.displayLarge,
                                    color = if (isHourSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                                )
                            }"""

content = content.replace(target2, replacement2)

target3 = """                            // Minute Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragEnd = { minuteDragAccumulator = 0f },
                                            onDragCancel = { minuteDragAccumulator = 0f }
                                        ) { change, dragAmount ->
                                            minuteDragAccumulator += dragAmount
                                            if (kotlin.math.abs(minuteDragAccumulator) >= threshold) {
                                                val steps = (minuteDragAccumulator / threshold).toInt()
                                                minuteDragAccumulator -= steps * threshold
                                                
                                                val newMinute = ((timePickerState.minute - steps) % 60 + 60) % 60
                                                setTimeReflectively(timePickerState, false, newMinute)
                                                hapticFeedback.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            }
                                        }
                                    }
                            )"""

replacement3 = """                            // Minute Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .background(
                                        color = if (!isHourSelected) MaterialTheme.colorScheme.primary.copy(alpha = 0.2f) 
                                                else MaterialTheme.colorScheme.surfaceVariant,
                                        shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
                                    )
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        awaitPointerEventScope {
                                            while (true) {
                                                val event = awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                                                if (event.changes.any { it.pressed }) {
                                                    isHourSelected = false
                                                }
                                            }
                                        }
                                    }
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragStart = { isDraggingMinute = true },
                                            onDragEnd = { 
                                                minuteDragAccumulator = 0f 
                                                isDraggingMinute = false
                                                animatingMinuteTarget = displayMinute
                                                scope.launch {
                                                    animateClock(timePickerState, false, displayMinute)
                                                    animatingMinuteTarget = null
                                                }
                                            },
                                            onDragCancel = { 
                                                minuteDragAccumulator = 0f
                                                isDraggingMinute = false
                                                displayMinute = timePickerState.minute
                                            }
                                        ) { change, dragAmount ->
                                            minuteDragAccumulator += dragAmount
                                            if (kotlin.math.abs(minuteDragAccumulator) >= threshold) {
                                                val steps = (minuteDragAccumulator / threshold).toInt()
                                                minuteDragAccumulator -= steps * threshold
                                                
                                                displayMinute = ((displayMinute - steps) % 60 + 60) % 60
                                                hapticFeedback.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            }
                                        }
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "%02d".format(displayMinute),
                                    style = MaterialTheme.typography.displayLarge,
                                    color = if (!isHourSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                                )
                            }"""

content = content.replace(target3, replacement3)

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'w') as f:
    f.write(content)
