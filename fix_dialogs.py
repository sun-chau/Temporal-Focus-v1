import os

settings_path = 'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
with open(settings_path, 'r') as f:
    content = f.read()

content = content.replace(
    "var showClearHistoryDialog by remember { mutableStateOf(false) }",
    "var showClearHistoryDialog by remember { mutableStateOf(false) }\n    var showHardResetDialog by remember { mutableStateOf(false) }"
)

clear_history_dialog = """    if (showClearHistoryDialog) {
        AlertDialog(
            onDismissRequest = { showClearHistoryDialog = false },
            title = { Text("Clear History") },
            text = { Text("Are you sure you want to delete all completed timers? This action cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.clearHistory()
                    showClearHistoryDialog = false
                }) {
                    Text("Clear")
                }
            },
            dismissButton = {
                TextButton(onClick = { showClearHistoryDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }"""

hard_reset_dialog = """    if (showHardResetDialog) {
        AlertDialog(
            onDismissRequest = { showHardResetDialog = false },
            title = { Text("Confirm Hard Reset") },
            text = { Text("This will reset all your Pomodoro statistics (sessions done, focus elapsed). This action cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.hardResetPomodoro()
                    showHardResetDialog = false
                }) {
                    Text("Reset")
                }
            },
            dismissButton = {
                TextButton(onClick = { showHardResetDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }"""

content = content.replace(clear_history_dialog, clear_history_dialog + "\n\n" + hard_reset_dialog)

content = content.replace(
    "modifier = Modifier.clickable { viewModel.hardResetPomodoro() }",
    "modifier = Modifier.clickable { showHardResetDialog = true }"
)

with open(settings_path, 'w') as f:
    f.write(content)

account_path = 'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt'
with open(account_path, 'r') as f:
    account_content = f.read()

account_content = account_content.replace(
    "var newTag by remember { mutableStateOf(\"\") }",
    "var newTag by remember { mutableStateOf(\"\") }\n    var showResetAccountDialog by remember { mutableStateOf(false) }"
)

reset_dialog = """    if (showResetAccountDialog) {
        AlertDialog(
            onDismissRequest = { showResetAccountDialog = false },
            title = { Text("Reset Account Info") },
            text = { Text("Are you sure you want to remove your account info and tags? This action cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.resetProfileInfo()
                    name = "Guest"
                    bio = ""
                    imageUri = ""
                    showResetAccountDialog = false
                }) {
                    Text("Reset")
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetAccountDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    Scaffold("""

account_content = account_content.replace("    Scaffold(", reset_dialog)

old_button = """                Button(
                    onClick = {
                        viewModel.resetProfileInfo()
                        name = "Guest"
                        bio = ""
                        imageUri = ""
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer,
                        contentColor = MaterialTheme.colorScheme.onErrorContainer
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Reset Account Info")
                }"""

new_button = """                Button(
                    onClick = { showResetAccountDialog = true },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.errorContainer,
                        contentColor = MaterialTheme.colorScheme.onErrorContainer
                    ),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Reset Account Info")
                }"""

account_content = account_content.replace(old_button, new_button)

with open(account_path, 'w') as f:
    f.write(account_content)
