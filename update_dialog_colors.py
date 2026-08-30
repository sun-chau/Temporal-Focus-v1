import os

settings_path = 'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
with open(settings_path, 'r') as f:
    content = f.read()

content = content.replace(
    """TextButton(onClick = {
                    viewModel.clearHistory()
                    showClearHistoryDialog = false
                })""",
    """TextButton(
                    onClick = {
                        viewModel.clearHistory()
                        showClearHistoryDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                )"""
)

content = content.replace(
    """TextButton(onClick = {
                    viewModel.hardResetPomodoro()
                    showHardResetDialog = false
                })""",
    """TextButton(
                    onClick = {
                        viewModel.hardResetPomodoro()
                        showHardResetDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                )"""
)

with open(settings_path, 'w') as f:
    f.write(content)

account_path = 'app/src/main/java/com/example/ui/screens/UserAccountScreen.kt'
with open(account_path, 'r') as f:
    account_content = f.read()

account_content = account_content.replace(
    """TextButton(onClick = {
                    viewModel.resetProfileInfo()
                    name = "Guest"
                    bio = ""
                    imageUri = ""
                    showResetAccountDialog = false
                })""",
    """TextButton(
                    onClick = {
                        viewModel.resetProfileInfo()
                        name = "Guest"
                        bio = ""
                        imageUri = ""
                        showResetAccountDialog = false
                    },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                )"""
)

with open(account_path, 'w') as f:
    f.write(account_content)
