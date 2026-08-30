import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    lines = f.readlines()

# add import
import_line = "import androidx.compose.foundation.gestures.detectVerticalDragGestures\n"
if import_line not in lines:
    for i, line in enumerate(lines):
        if line.startswith("import androidx.compose.foundation.gestures.detectDragGestures"):
            lines.insert(i+1, import_line)
            break

# find indices
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "// Main Timer Card" in line:
        start_idx = i
    if "Spacer(modifier = Modifier.height(80.dp)) // space for FAB" in line:
        end_idx = i
        break

new_block = """            // Main Timer Card
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(vertical = 48.dp, horizontal = 24.dp)
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally, 
                    modifier = Modifier.fillMaxWidth()
                ) {
                    val phaseColor = when (uiState.currentPhase) {
                        PomodoroPhase.FOCUS -> MaterialTheme.colorScheme.primary
                        PomodoroPhase.BREAK -> MaterialTheme.colorScheme.tertiary
                        PomodoroPhase.LONG_BREAK -> MaterialTheme.colorScheme.secondary
                    }
                    
                    // Phase indicator (Pill)
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(50))
                            .background(MaterialTheme.colorScheme.background)
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        val phaseText = when (uiState.currentPhase) {
                            PomodoroPhase.FOCUS -> "FOCUS (${uiState.currentSessionCount + 1}/${uiState.pomodoroTargetSessions})"
                            PomodoroPhase.BREAK -> "BREAK"
                            PomodoroPhase.LONG_BREAK -> "LONG BREAK"
                        }
                        Text(
                            text = phaseText,
                            color = phaseColor,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    
                    // Massive Text Timer with Vertical Drag
                    var dragAccumulator by remember { mutableFloatStateOf(0f) }
                    val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
                    
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .pointerInput(uiState.isPomodoroRunning, uiState.hasPomodoroStarted) {
                                detectVerticalDragGestures(
                                    onDragStart = { dragAccumulator = 0f },
                                    onVerticalDrag = { change, dragAmount ->
                                        change.consume()
                                        // dragAmount > 0 is drag down (should decrement time)
                                        // dragAmount < 0 is drag up (should increment time)
                                        // so we negate dragAmount for accumulation
                                        dragAccumulator += -dragAmount
                                        
                                        // e.g. 15 pixels of drag = 1 minute
                                        val pixelsPerMinute = 25f 
                                        if (kotlin.math.abs(dragAccumulator) >= pixelsPerMinute) {
                                            val sign = kotlin.math.sign(dragAccumulator)
                                            val minutesDelta = sign.toInt()
                                            
                                            if (!uiState.isPomodoroRunning && !uiState.hasPomodoroStarted) {
                                                when (uiState.currentPhase) {
                                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                                    PomodoroPhase.BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                                }
                                            } else {
                                                viewModel.addLiveExtraTime((minutesDelta * 60).toLong())
                                            }
                                            
                                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            dragAccumulator -= sign * pixelsPerMinute
                                        }
                                    }
                                )
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        val mins = uiState.pomodoroTimeRemainingSeconds / 60
                        val secs = uiState.pomodoroTimeRemainingSeconds % 60
                        val timeString = String.format(Locale.US, "%02d:%02d", mins, secs)
                        
                        Text(
                            text = timeString,
                            color = if (uiState.isPomodoroRunning) phaseColor else phaseColor.copy(alpha = 0.5f),
                            fontSize = 110.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace,
                            style = androidx.compose.ui.text.TextStyle(fontFeatureSettings = "tnum")
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(48.dp))
                    
                    // Centralized Actions
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        // Reset
                        IconButton(onClick = { viewModel.resetPomodoro() }) {
                            Icon(Icons.Rounded.Refresh, contentDescription = "Reset", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        
                        Spacer(modifier = Modifier.width(24.dp))
                        
                        // Play/Pause
                        FilledIconButton(
                            onClick = { viewModel.togglePomodoroTimer() },
                            modifier = Modifier.size(72.dp),
                            colors = IconButtonDefaults.filledIconButtonColors(
                                containerColor = if (uiState.isPomodoroRunning) MaterialTheme.colorScheme.onSurface else phaseColor,
                                contentColor = if (uiState.isPomodoroRunning) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onPrimary
                            )
                        ) {
                            Icon(
                                imageVector = if (uiState.isPomodoroRunning) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                contentDescription = if (uiState.isPomodoroRunning) "Pause" else "Play",
                                modifier = Modifier.size(36.dp)
                            )
                        }
                        
                        Spacer(modifier = Modifier.width(24.dp))
                        
                        // Skip
                        if (uiState.hasPomodoroStarted || uiState.currentPhase != PomodoroPhase.FOCUS) {
                            IconButton(onClick = { viewModel.skipPomodoroPhase() }) {
                                Icon(Icons.Rounded.SkipNext, contentDescription = "Skip", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        } else {
                            Spacer(modifier = Modifier.size(48.dp)) // Placeholder to maintain balance
                        }
                    }
                }
            }
"""

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_block + "\n"] + lines[end_idx:]

content = "".join(lines)

# Remove unused composables
# 1. LiveAdjustmentButton
content = re.sub(r'@Composable\nfun LiveAdjustmentButton\(.*?\n\}\n', '', content, flags=re.DOTALL)
# It might have been formatted slightly differently, let's just do it directly.

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
