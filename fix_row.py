import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

old_row = """                    // Centralized Actions
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        // Reset
                        IconButton(onClick = { viewModel.resetPomodoro() }) {
                            Icon(Icons.Default.Refresh, contentDescription = "Reset", tint = MaterialTheme.colorScheme.onSurfaceVariant)
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
                                imageVector = if (uiState.isPomodoroRunning) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = if (uiState.isPomodoroRunning) "Pause" else "Play",
                                modifier = Modifier.size(36.dp)
                            )
                        }
                        
                        Spacer(modifier = Modifier.width(24.dp))
                        
                        // Skip
                        if (uiState.hasPomodoroStarted || uiState.currentPhase != PomodoroPhase.FOCUS) {
                            IconButton(onClick = { viewModel.skipPomodoroPhase() }) {
                                Icon(Icons.Default.SkipNext, contentDescription = "Skip", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        } else {
                            Spacer(modifier = Modifier.size(48.dp)) // Placeholder to maintain balance
                        }
                    }"""

new_row = """                    // Centralized Actions
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
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
                                imageVector = if (uiState.isPomodoroRunning) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = if (uiState.isPomodoroRunning) "Pause" else "Play",
                                modifier = Modifier.size(36.dp)
                            )
                        }
                    }"""

content = content.replace(old_row, new_row)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
