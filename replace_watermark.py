import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

new_watermark = """@Composable
private fun AnalyticsWatermark(uiState: com.example.viewmodel.UiState) {
    val currentTimeMillis = System.currentTimeMillis()
    
    // 1. ETA Math
    val pendingSessions = uiState.pomodoroTargetSessions - uiState.currentSessionCount
    val pendingFocusSeconds = if (uiState.currentPhase == com.example.viewmodel.PomodoroPhase.FOCUS) {
        maxOf(0, pendingSessions - 1) * uiState.baseFocusDurationMinutes * 60L
    } else {
        pendingSessions * uiState.baseFocusDurationMinutes * 60L
    }
    val pendingBreakSeconds = if (uiState.currentPhase == com.example.viewmodel.PomodoroPhase.BREAK) {
        maxOf(0, pendingSessions - 1) * uiState.baseBreakDurationMinutes * 60L
    } else {
        pendingSessions * uiState.baseBreakDurationMinutes * 60L
    }
    val terminalEtaMillis = currentTimeMillis + (uiState.pomodoroTimeRemainingSeconds + pendingFocusSeconds + pendingBreakSeconds) * 1000L
    val formattedTerminalEta = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date(terminalEtaMillis))

    // 2. Invested Math
    val investedMins = uiState.totalFocusTimeSeconds / 60
    val formattedInvested = String.format(java.util.Locale.US, "%02d:%02d", investedMins / 60, investedMins % 60)

    // 3. New Tactical Metrics
    val totalActiveSeconds = uiState.totalFocusTimeSeconds + uiState.totalBreakTimeSeconds
    val efficiency = if (totalActiveSeconds > 0) (uiState.totalFocusTimeSeconds.toFloat() / totalActiveSeconds * 100).toInt() else 0
    val interventions = uiState.liveAdjustmentCount

    val idealElapsed = (uiState.currentSessionCount * uiState.baseFocusDurationMinutes * 60L) + 
                       (uiState.totalBreaksTaken * uiState.baseBreakDurationMinutes * 60L)
    val actualElapsed = uiState.totalFocusTimeSeconds + uiState.totalBreakTimeSeconds
    val deviationMins = (actualElapsed - idealElapsed) / 60
    val formattedDeviation = if (deviationMins > 0) "+${deviationMins}M" else "${deviationMins}M"

    // 4. Ghost Typography
    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 22.sp, // Slightly reduced to fit 6 data points cleanly
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.06f)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(top = 80.dp, bottom = 48.dp, start = 24.dp, end = 24.dp)
    ) {
        // TOP ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD: ${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
            Text("INVESTED: $formattedInvested", style = textStyle)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // MIDDLE ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INTERVENTIONS: $interventions", style = textStyle)
            Text("EFFICIENCY: $efficiency%", style = textStyle)
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        // BOTTOM ROW
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("DEVIATION: $formattedDeviation", style = textStyle)
            Text("ETA: $formattedTerminalEta", style = textStyle)
        }
    }
}
"""

start_idx = content.find('@Composable\nprivate fun AnalyticsWatermark')
if start_idx != -1:
    end_idx = content.find('@Composable\nfun SystemTimeBar', start_idx)
    if end_idx != -1:
        content = content[:start_idx] + new_watermark + content[end_idx:]
    else:
        print("Could not find SystemTimeBar")
else:
    print("Could not find AnalyticsWatermark")

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)

