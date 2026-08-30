import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Remove state variables
content = re.sub(r'\s*var showStats by androidx\.compose\.runtime\.saveable\.rememberSaveable \{ mutableStateOf\(false\) \}\n', '\n', content)
content = re.sub(r'\s*var isPeeking by remember \{ mutableStateOf\(false\) \}\n', '\n', content)

# 2. Insert AnalyticsWatermark inside root Box
content = content.replace("    Box(modifier = Modifier.fillMaxSize()) {", "    Box(modifier = Modifier.fillMaxSize()) {\n        AnalyticsWatermark(uiState)")

# 3. Remove the Peeking FAB
fab_regex = r"\s*var isPeeking by remember \{ mutableStateOf\(false\) \}\n\s*Box\(\s*modifier = Modifier\s*\.align\(Alignment\.BottomEnd\).*?imageVector = Icons\.Default\.TouchApp,.*?\}\n"
# Wait, I already removed `var isPeeking by...` line above using re.sub, so fab_regex won't match if it depends on it. Let's just find the Box that aligns BottomEnd and contains TouchApp.
fab_regex_2 = r"\s*Box\(\s*modifier = Modifier\s*\.align\(Alignment\.BottomEnd\).*?imageVector = Icons\.Default\.TouchApp,.*?\}\n"
content = re.sub(fab_regex_2, "\n", content, flags=re.DOTALL)

# 4. Remove `if (showStats) { PomodoroStatsOverlay(...) }`
stats_regex = r"\s*if \(showStats\) \{\s*PomodoroStatsOverlay\(uiState, onDismiss = \{ showStats = false \}, isPeeking = isPeeking\)\s*\}"
content = re.sub(stats_regex, "", content, flags=re.DOTALL)

# 5. Replace PomodoroStatsOverlay and PomodoroStatCard with AnalyticsWatermark
watermark_code = """
@Composable
private fun AnalyticsWatermark(uiState: com.example.viewmodel.UiState) {
    val currentTimeMillis = System.currentTimeMillis()
    
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

    val idealBreakSeconds = uiState.totalBreaksTaken * uiState.baseBreakDurationMinutes * 60L
    val leakageSeconds = maxOf(0L, uiState.totalBreakTimeSeconds - idealBreakSeconds)
    val leakageMins = leakageSeconds / 60

    val investedMins = uiState.totalFocusTimeSeconds / 60
    val investedHours = investedMins / 60
    val investedMinsRem = investedMins % 60
    val formattedInvested = String.format(java.util.Locale.US, "%02d:%02d", investedHours, investedMinsRem)

    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 24.sp,
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f)
    )

    Column(modifier = Modifier.fillMaxSize().padding(32.dp)) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD: ${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
            Text("INVESTED: $formattedInvested", style = textStyle)
        }
        Spacer(modifier = Modifier.weight(1f))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("LEAKAGE: +${leakageMins}M", style = textStyle)
            Text("ETA: $formattedTerminalEta", style = textStyle)
        }
    }
}
"""

overlay_start = content.find("@Composable\nfun PomodoroStatsOverlay")
if overlay_start != -1:
    content = content[:overlay_start] + watermark_code
else:
    content += watermark_code

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
