import re

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'r') as f:
    content = f.read()

target = """                if (showDial) {
                    TimePicker(state = timePickerState, colors = colors)
                } else {
                    TimeInput(state = timePickerState, colors = colors)
                }"""

replacement = """                if (showDial) {
                    Box(contentAlignment = Alignment.TopCenter, modifier = Modifier.fillMaxWidth()) {
                        TimePicker(state = timePickerState, colors = colors)
                        
                        // Transparent gesture overlays for vertical dragging
                        Row(
                            modifier = Modifier
                                .padding(top = 20.dp)
                                .height(80.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            var hourDragAccumulator by remember { mutableFloatStateOf(0f) }
                            var minuteDragAccumulator by remember { mutableFloatStateOf(0f) }
                            val threshold = with(androidx.compose.ui.platform.LocalDensity.current) { 24.dp.toPx() }
                            val hapticFeedback = androidx.compose.ui.platform.LocalHapticFeedback.current

                            fun setTimeReflectively(state: TimePickerState, isHour: Boolean, value: Int) {
                                try {
                                    val prefix = if (isHour) "setHour" else "setMinute"
                                    val method = state.javaClass.methods.firstOrNull { it.name.startsWith(prefix) }
                                    method?.isAccessible = true
                                    method?.invoke(state, value)
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }

                            // Hour Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragEnd = { hourDragAccumulator = 0f },
                                            onDragCancel = { hourDragAccumulator = 0f }
                                        ) { _, dragAmount ->
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
                            )
                            
                            Spacer(modifier = Modifier.width(24.dp))
                            
                            // Minute Box Overlay
                            Box(
                                modifier = Modifier
                                    .size(96.dp, 80.dp)
                                    .androidx.compose.ui.input.pointer.pointerInput(Unit) {
                                        androidx.compose.foundation.gestures.detectVerticalDragGestures(
                                            onDragEnd = { minuteDragAccumulator = 0f },
                                            onDragCancel = { minuteDragAccumulator = 0f }
                                        ) { _, dragAmount ->
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
                            )
                            
                            // To keep the row center-aligned correctly, we must offset the AM/PM toggle width in 12h mode
                            if (!is24Hour) {
                                Spacer(modifier = Modifier.width(8.dp))
                                Spacer(modifier = Modifier.width(52.dp))
                            }
                        }
                    }
                } else {
                    TimeInput(state = timePickerState, colors = colors)
                }"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'w') as f:
    f.write(content)

