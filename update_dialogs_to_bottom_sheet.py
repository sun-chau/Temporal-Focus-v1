import re

settings_path = 'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
with open(settings_path, 'r') as f:
    content = f.read()

# Replace Clear History Dialog
clear_history_old = """    if (showClearHistoryDialog) {
        AlertDialog(
            onDismissRequest = { showClearHistoryDialog = false },
            title = { Text("Clear History") },
            text = { Text("Are you sure you want to delete all completed timers? This action cannot be undone.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.clearHistory()
                        showClearHistoryDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                ) {
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

clear_history_new = """    if (showClearHistoryDialog) {
        ModalBottomSheet(
            onDismissRequest = { showClearHistoryDialog = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text(
                    text = "Clear History",
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Are you sure you want to delete all completed timers? This action cannot be undone.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(32.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showClearHistoryDialog = false }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(
                        onClick = {
                            viewModel.clearHistory()
                            showClearHistoryDialog = false
                        }
                    ) {
                        Text("Clear", color = MaterialTheme.colorScheme.error)
                    }
                }
                Spacer(modifier = Modifier.height(WindowInsets.navigationBars.asPaddingValues().calculateBottomPadding()))
            }
        }
    }"""

# Replace Hard Reset Dialog
hard_reset_old = """    if (showHardResetDialog) {
        AlertDialog(
            onDismissRequest = { showHardResetDialog = false },
            title = { Text("Confirm Hard Reset") },
            text = { Text("This will reset all your Pomodoro statistics (sessions done, focus elapsed). This action cannot be undone.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.hardResetPomodoro()
                        showHardResetDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                ) {
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

hard_reset_new = """    if (showHardResetDialog) {
        ModalBottomSheet(
            onDismissRequest = { showHardResetDialog = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text(
                    text = "Confirm Hard Reset",
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "This will reset all your Pomodoro statistics (sessions done, focus elapsed). This action cannot be undone.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(32.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showHardResetDialog = false }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(
                        onClick = {
                            viewModel.hardResetPomodoro()
                            showHardResetDialog = false
                        }
                    ) {
                        Text("Reset", color = MaterialTheme.colorScheme.error)
                    }
                }
                Spacer(modifier = Modifier.height(WindowInsets.navigationBars.asPaddingValues().calculateBottomPadding()))
            }
        }
    }"""

content = content.replace(clear_history_old, clear_history_new)
content = content.replace(hard_reset_old, hard_reset_new)

with open(settings_path, 'w') as f:
    f.write(content)

account_path = 'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt'
with open(account_path, 'r') as f:
    account_content = f.read()

reset_account_old = """    if (showResetAccountDialog) {
        AlertDialog(
            onDismissRequest = { showResetAccountDialog = false },
            title = { Text("Reset Account Info") },
            text = { Text("Are you sure you want to remove your account info and tags? This action cannot be undone.") },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.resetProfileInfo()
                        name = "Guest"
                        bio = ""
                        imageUri = ""
                        showResetAccountDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                ) {
                    Text("Reset")
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetAccountDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }"""

reset_account_new = """    if (showResetAccountDialog) {
        ModalBottomSheet(
            onDismissRequest = { showResetAccountDialog = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text(
                    text = "Reset Account Info",
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Are you sure you want to remove your account info and tags? This action cannot be undone.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(32.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showResetAccountDialog = false }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(
                        onClick = {
                            viewModel.resetProfileInfo()
                            name = "Guest"
                            bio = ""
                            imageUri = ""
                            showResetAccountDialog = false
                        }
                    ) {
                        Text("Reset", color = MaterialTheme.colorScheme.error)
                    }
                }
                Spacer(modifier = Modifier.height(WindowInsets.navigationBars.asPaddingValues().calculateBottomPadding()))
            }
        }
    }"""

account_content = account_content.replace(reset_account_old, reset_account_new)

with open(account_path, 'w') as f:
    f.write(account_content)

