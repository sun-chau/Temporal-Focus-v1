package com.example.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Keyboard
import androidx.compose.material.icons.filled.Schedule
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UniversalTimePickerDialog(
    initialHour: Int,
    initialMinute: Int,
    is24Hour: Boolean,
    onTimeSelected: (hour: Int, minute: Int) -> Unit,
    onDismiss: () -> Unit
) {
    var showDial by remember { mutableStateOf(true) }
    val timePickerState = rememberTimePickerState(
        initialHour = initialHour,
        initialMinute = initialMinute,
        is24Hour = is24Hour
    )

    AlertDialog(
        onDismissRequest = onDismiss,
        modifier = Modifier.fillMaxWidth(),
        shape = RectangleShape,
        containerColor = MaterialTheme.colorScheme.surface,
        title = { Text("SELECT TIME", fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.onSurface) },
        text = {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth()
            ) {
                val colors = TimePickerDefaults.colors(
                    clockDialColor = MaterialTheme.colorScheme.surfaceVariant,
                    clockDialSelectedContentColor = MaterialTheme.colorScheme.onPrimary,
                    clockDialUnselectedContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    selectorColor = MaterialTheme.colorScheme.primary,
                    containerColor = MaterialTheme.colorScheme.surface,
                    periodSelectorBorderColor = MaterialTheme.colorScheme.primary,
                    periodSelectorSelectedContainerColor = MaterialTheme.colorScheme.primary,
                    periodSelectorUnselectedContainerColor = MaterialTheme.colorScheme.surface,
                    periodSelectorSelectedContentColor = MaterialTheme.colorScheme.onPrimary,
                    periodSelectorUnselectedContentColor = MaterialTheme.colorScheme.onSurface,
                    timeSelectorSelectedContainerColor = MaterialTheme.colorScheme.primary,
                    timeSelectorUnselectedContainerColor = MaterialTheme.colorScheme.surfaceVariant,
                    timeSelectorSelectedContentColor = MaterialTheme.colorScheme.onPrimary,
                    timeSelectorUnselectedContentColor = MaterialTheme.colorScheme.onSurface
                )
                
                if (showDial) {
                    Box(contentAlignment = Alignment.TopCenter, modifier = Modifier.fillMaxWidth()) {
                        TimePicker(state = timePickerState, colors = colors)
                        
                        // Opaque gesture overlays for vertical dragging and smooth clock updates
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
                                    .pointerInput(Unit) {
                                        detectVerticalDragGestures(
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
                                    .pointerInput(Unit) {
                                        detectVerticalDragGestures(
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
                }
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    horizontalArrangement = Arrangement.Start
                ) {
                    IconButton(onClick = { showDial = !showDial }) {
                        Icon(
                            imageVector = if (showDial) Icons.Default.Keyboard else Icons.Default.Schedule,
                            contentDescription = "Toggle input mode",
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = {
                onTimeSelected(timePickerState.hour, timePickerState.minute)
            }) {
                Text("[ OK ]", fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.primary)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("[ CANCEL ]", fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.primary)
            }
        }
    )
}
