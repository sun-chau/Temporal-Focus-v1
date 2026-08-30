import re

path = 'app/src/main/java/com/example/ui/screens/PomodoroScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# Remove var showResetDialog
content = content.replace(
    "var showResetDialog by remember { mutableStateOf(false) }",
    ""
)

# Remove button
button_old = """            Spacer(Modifier.height(24.dp))
            
            Button(
                onClick = { showResetDialog = true },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF5252)),
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(50)
            ) {
                Text("HARD RESET STATS", color = Color.White, fontWeight = FontWeight.Bold)
            }"""
content = content.replace(button_old, "")

# Remove dialog
dialog_old = """        if (showResetDialog) {
            AlertDialog(
                onDismissRequest = { showResetDialog = false },
                title = { Text("Confirm Hard Reset") },
                text = { Text("This will reset all your Pomodoro statistics (sessions done, focus elapsed). This action cannot be undone.") },
                confirmButton = {
                    TextButton(
                        onClick = {
                            onHardReset()
                            showResetDialog = false
                            onDismiss()
                        }
                    ) {
                        Text("Reset", color = MaterialTheme.colorScheme.error)
                    }
                },
                dismissButton = {
                    TextButton(
                        onClick = { showResetDialog = false }
                    ) {
                        Text("Cancel")
                    }
                }
            )
        }"""
content = content.replace(dialog_old, "")

with open(path, 'w') as f:
    f.write(content)
