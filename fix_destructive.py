import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

old_destructive = """                        // Destructive Phase Overrides
                        Button(
                            onClick = { 
                                viewModel.skipPomodoroPhase() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.errorContainer, contentColor = MaterialTheme.colorScheme.onErrorContainer)
                        ) {
                            Text("End Early")
                        }"""

new_destructive = """                        // Destructive Phase Overrides
                        OutlinedButton(
                            onClick = { 
                                viewModel.skipPomodoroPhase() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("End Early")
                        }"""

content = content.replace(old_destructive, new_destructive)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
