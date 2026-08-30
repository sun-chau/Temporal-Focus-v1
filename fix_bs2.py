import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Un-nest the settings gear (if not already done correctly)
# Looking for `if (!uiState.hasPomodoroStarted) {` followed by `IconButton(onClick = { showSettingsDialog = true }`
# Wait, let's just do it cleanly by searching for exact text.
import textwrap

old_gear = """                if (!uiState.hasPomodoroStarted) {
                    IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) {
                        Icon(
                            imageVector = Icons.Outlined.Settings,
                            contentDescription = "Settings",
                            modifier = Modifier.size(28.dp),
                            tint = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }"""
new_gear = """                IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) {
                    Icon(
                        imageVector = Icons.Outlined.Settings,
                        contentDescription = "Settings",
                        modifier = Modifier.size(28.dp),
                        tint = MaterialTheme.colorScheme.onSurface
                    )
                }"""
content = content.replace(old_gear, new_gear)

old_bs = """        if (showSettingsDialog && !uiState.hasPomodoroStarted) {"""
new_bs = """        if (showSettingsDialog) {"""
content = content.replace(old_bs, new_bs)


bs_start = content.find("        if (showSettingsDialog) {")
if bs_start != -1:
    bs_end = content.find("        if (showStats) {", bs_start)
    if bs_end != -1:
        new_bs_content = """        if (showSettingsDialog) {
            ModalBottomSheet(
                onDismissRequest = { showSettingsDialog = false },
                sheetState = sheetState,
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp)
                        .padding(bottom = 32.dp, top = 8.dp)
                        .navigationBarsPadding()
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            if (!uiState.hasPomodoroStarted) "SETUP PHASE SETTINGS" else "LIVE SESSION CONTROLS",
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        IconButton(onClick = { showSettingsDialog = false }, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurface)
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    
                    if (!uiState.hasPomodoroStarted) {
                        Text(
                            "Hold +/- for rapid adjustment",
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                            fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace
                        )
                        Spacer(Modifier.height(24.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Base Focus", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Standard focus cycle", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustBaseFocusTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.baseFocusDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustBaseFocusTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Base Break", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Standard breather cycle", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustBaseBreakTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.baseBreakDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustBaseBreakTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Target Sessions", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Sessions before long break", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustTargetSessions(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.pomodoroTargetSessions}", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustTargetSessions(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Long Break", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("After target sessions", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustLongBreakTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.longBreakDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustLongBreakTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                    } else {
                        // Live Session Controls
                        Spacer(Modifier.height(16.dp))
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            Button(onClick = { viewModel.addLiveExtraTime(-10 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-10m") }
                            Button(onClick = { viewModel.addLiveExtraTime(-5 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-5m") }
                            Button(onClick = { viewModel.addLiveExtraTime(-1 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-1m") }
                        }
                        Spacer(Modifier.height(8.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            Button(onClick = { viewModel.addLiveExtraTime(1 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+1m") }
                            Button(onClick = { viewModel.addLiveExtraTime(5 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+5m") }
                            Button(onClick = { viewModel.addLiveExtraTime(10 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+10m") }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        
                        // Undo Fail-Safe
                        val extraTimeMins = uiState.sessionExtraTimeSeconds / 60
                        val extraTimeLabel = if (extraTimeMins > 0) "+${extraTimeMins}m" else if (extraTimeMins < 0) "${extraTimeMins}m" else ""
                        
                        TextButton(
                            onClick = { viewModel.revertLiveExtraTime() },
                            enabled = uiState.sessionExtraTimeSeconds != 0L,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Revert to Original Target" + if (extraTimeLabel.isNotEmpty()) " ($extraTimeLabel)" else "")
                        }
                        
                        Spacer(Modifier.height(16.dp))
                        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                        Spacer(Modifier.height(16.dp))
                        
                        // Destructive Phase Overrides
                        Button(
                            onClick = { 
                                viewModel.skipPomodoroPhase() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.errorContainer, contentColor = MaterialTheme.colorScheme.onErrorContainer)
                        ) {
                            Text("End Early")
                        }
                        
                        Spacer(Modifier.height(8.dp))
                        
                        OutlinedButton(
                            onClick = { 
                                viewModel.resetPomodoro() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("Reset Pomodoro")
                        }
                    }
                }
            }
        }
"""
        content = content[:bs_start] + new_bs_content + content[bs_end:]

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)

