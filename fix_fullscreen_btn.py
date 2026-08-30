import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

target = """                            Box {
                                var menuExpanded by remember { mutableStateOf(false) }
                                
                                FilledTonalIconButton(
                                    onClick = { menuExpanded = true },
                                ) {
                                    Icon(Icons.Default.MoreVert, contentDescription = "More Options")
                                }
                                
                                Spacer(Modifier.width(8.dp))
                            }
                            
                            FilledTonalIconButton(
                                onClick = { showImmersive = true }
                            ) {
                                Icon(androidx.compose.material.icons.filled.Fullscreen, contentDescription = "Full Screen")
                            }"""

replacement = """                            Box {
                                var menuExpanded by remember { mutableStateOf(false) }
                                
                                FilledTonalIconButton(
                                    onClick = { menuExpanded = true },
                                ) {
                                    Icon(Icons.Default.MoreVert, contentDescription = "More Options")
                                }
                                   
                                val isSetupPhase = !uiState.isPomodoroRunning && uiState.pomodoroTimeRemainingSeconds == currentBaseTime
                                   
                                DropdownMenu(
                                    expanded = menuExpanded,
                                    onDismissRequest = { menuExpanded = false }
                                ) {
                                    DropdownMenuItem(
                                        text = { Text("Restart Phase") },
                                        onClick = { 
                                            viewModel.restartPomodoroPhase()
                                            menuExpanded = false
                                        },
                                        leadingIcon = { Icon(Icons.Default.Refresh, contentDescription = null) }
                                    )
                                    DropdownMenuItem(
                                        text = { Text("Skip Phase") },
                                        onClick = { 
                                            viewModel.skipPomodoroPhase()
                                            menuExpanded = false
                                        },
                                        enabled = !isSetupPhase,
                                        leadingIcon = { Icon(Icons.Default.SkipNext, contentDescription = null) }
                                    )
                                    DropdownMenuItem(
                                        text = { Text("Reset Pomodoro") },
                                        onClick = { 
                                            viewModel.resetPomodoro()
                                            menuExpanded = false
                                        },
                                        leadingIcon = { Icon(Icons.Default.Clear, contentDescription = null) }
                                    )
                                }
                            }
                            Spacer(Modifier.width(8.dp))
                            FilledTonalIconButton(
                                onClick = { showImmersive = true }
                            ) {
                                Icon(androidx.compose.material.icons.filled.Fullscreen, contentDescription = "Full Screen")
                            }"""

# Actually, my previous replacement removed the DropdownMenu entirely because I didn't include it in target/replacement correctly. Wait, no I didn't remove it because the target ended early, so the DropdownMenu was still there. Let's check how the file looks right now.
