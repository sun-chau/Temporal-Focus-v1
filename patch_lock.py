import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

# Update JournalLockScreen call
content = content.replace("        JournalLockScreen(\n            onUnlock = { isUnlocked = true },\n            onMenuClick = onMenuClick\n        )",
"        JournalLockScreen(\n            uiState = uiState,\n            onUnlock = { isUnlocked = true },\n            onMenuClick = onMenuClick\n        )")

# Update JournalLockScreen signature
content = content.replace("fun JournalLockScreen(onUnlock: () -> Unit, onMenuClick: () -> Unit) {",
"fun JournalLockScreen(uiState: UiState, onUnlock: () -> Unit, onMenuClick: () -> Unit) {")

# Update PIN confirm button
old_confirm = """            confirmButton = {
                TextButton(onClick = {
                    onUnlock()
                    showPinDialog = false
                }) { Text("Unlock") }
            },"""
new_confirm = """            confirmButton = {
                TextButton(onClick = {
                    if (uiState.appPassword.isBlank() || pin == uiState.appPassword) {
                        onUnlock()
                        showPinDialog = false
                    } else {
                        android.widget.Toast.makeText(context, "Incorrect Password", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }) { Text("Unlock") }
            },"""
content = content.replace(old_confirm, new_confirm)

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
    f.write(content)

