import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                            ) {
                                val startStr = getSemanticTime(ghostStartTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                val endStr = getSemanticTime(ghostEndTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                androidx.compose.material3.Text(
                                    text = "$startStr - $endStr",
                                    color = if (isWarning) androidx.compose.ui.graphics.Color.Red else androidx.compose.material3.MaterialTheme.colorScheme.primary,
                                    style = androidx.compose.material3.MaterialTheme.typography.labelSmall,
                                    modifier = androidx.compose.ui.Modifier.align(androidx.compose.ui.Alignment.Center)
                                )
                            }"""

replacement = """                            ) {
                                val startStr = getSemanticTime(ghostStartTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                val endStr = getSemanticTime(ghostEndTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                androidx.compose.material3.Text(
                                    text = "[ $startStr - $endStr ]",
                                    fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                                    color = if (isWarning) androidx.compose.ui.graphics.Color.Red else androidx.compose.material3.MaterialTheme.colorScheme.primary,
                                    style = androidx.compose.material3.MaterialTheme.typography.labelSmall,
                                    modifier = androidx.compose.ui.Modifier.align(androidx.compose.ui.Alignment.Center)
                                )
                            }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Ghost text patched")
