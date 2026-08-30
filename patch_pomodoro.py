import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

target_text = """                    Text(
                        text = timeString,
                        color = phaseColor,
                        fontSize = 80.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Monospace
                    )"""

replacement_text = """                    Box(contentAlignment = Alignment.Center) {
                        PomodoroArcDial(
                            uiState = uiState,
                            viewModel = viewModel,
                            phaseColor = phaseColor
                        )
                        Text(
                            text = timeString,
                            color = phaseColor,
                            fontSize = 80.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace
                        )
                    }"""

content = content.replace(target_text, replacement_text)

pomodoro_arc_dial = """

@Composable
private fun PomodoroArcDial(
    uiState: UiState,
    viewModel: MainViewModel,
    phaseColor: Color
) {
    val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
    var dragAccumulator by remember { mutableFloatStateOf(0f) }

    val maxDurationMinutes = when (uiState.currentPhase) {
        PomodoroPhase.FOCUS -> uiState.baseFocusDurationMinutes
        PomodoroPhase.SHORT_BREAK -> uiState.baseBreakDurationMinutes
        PomodoroPhase.LONG_BREAK -> uiState.longBreakDurationMinutes
    }
    val maxDurationSeconds = maxDurationMinutes * 60f
    val remainingPercentage = uiState.pomodoroTimeRemainingSeconds.toFloat() / maxDurationSeconds.coerceAtLeast(1f)
    val sweepAngle = remainingPercentage * 360f
    
    val trackColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f)

    androidx.compose.foundation.Canvas(
        modifier = Modifier
            .size(280.dp)
            .pointerInput(uiState.isPomodoroRunning, uiState.hasPomodoroStarted) {
                androidx.compose.foundation.gestures.detectDragGestures(
                    onDragStart = { dragAccumulator = 0f },
                    onDrag = { change, _ ->
                        change.consume()
                        val centerX = size.width / 2f
                        val centerY = size.height / 2f
                        
                        val prevAngle = Math.toDegrees(kotlin.math.atan2((change.previousPosition.y - centerY).toDouble(), (change.previousPosition.x - centerX).toDouble()))
                        val currentAngle = Math.toDegrees(kotlin.math.atan2((change.position.y - centerY).toDouble(), (change.position.x - centerX).toDouble()))
                        
                        var angleDelta = (currentAngle - prevAngle).toFloat()
                        if (angleDelta > 180f) angleDelta -= 360f
                        if (angleDelta < -180f) angleDelta += 360f

                        // 6 degrees of physical drag = 1 minute of time (360 degrees = 60 minutes)
                        val secondsPerDegree = 10f
                        dragAccumulator += angleDelta * secondsPerDegree
                        
                        if (kotlin.math.abs(dragAccumulator) >= 60f) {
                            val sign = kotlin.math.sign(dragAccumulator)
                            val minutesDelta = sign.toInt()
                            
                            if (!uiState.isPomodoroRunning && !uiState.hasPomodoroStarted) {
                                when (uiState.currentPhase) {
                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                    PomodoroPhase.SHORT_BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                }
                            } else {
                                viewModel.addLiveExtraTime((minutesDelta * 60).toLong())
                            }
                            
                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                            dragAccumulator -= sign * 60f
                        }
                    }
                )
            }
    ) {
        drawArc(
            color = trackColor,
            startAngle = -90f,
            sweepAngle = 360f,
            useCenter = false,
            style = androidx.compose.ui.graphics.drawscope.Stroke(width = 12.dp.toPx(), cap = androidx.compose.ui.graphics.StrokeCap.Round)
        )
        
        drawArc(
            color = phaseColor,
            startAngle = -90f,
            sweepAngle = sweepAngle,
            useCenter = false,
            style = androidx.compose.ui.graphics.drawscope.Stroke(width = 12.dp.toPx(), cap = androidx.compose.ui.graphics.StrokeCap.Round)
        )
    }
}
"""

content = content + pomodoro_arc_dial

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
