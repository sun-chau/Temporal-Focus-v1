import re

with open("app/src/main/java/com/example/ui/screens/SecuritySettingsScreen.kt", "r") as f:
    content = f.read()

# Replace variables
content = content.replace("    var appPasswordEnabled by remember { mutableStateOf(uiState.appPasswordEnabled) }",
                          "    var privateJournalLockEnabled by remember { mutableStateOf(uiState.privateJournalLockEnabled) }\n    var appPasswordEnabled by remember { mutableStateOf(uiState.appPasswordEnabled) }")

# Replace save logic
save_logic = """                        viewModel.togglePrivateJournalLock(privateJournalLockEnabled)
                        viewModel.toggleAppPasswordEnabled(appPasswordEnabled)"""
content = content.replace("                        viewModel.toggleAppPasswordEnabled(appPasswordEnabled)", save_logic)

# Replace Switch for app password
switch_old = """                    Switch(
                        checked = appPasswordEnabled,
                        onCheckedChange = { appPasswordEnabled = it }
                    )"""
switch_new = """                    ThemeSwitch(
                        checked = appPasswordEnabled,
                        onCheckedChange = { appPasswordEnabled = it }
                    )"""
content = content.replace(switch_old, switch_new)

# Add Private Journal Lock item
journal_lock_item = """            ListItem(
                headlineContent = { Text("Private Journal Lock") },
                supportingContent = { Text("Require lock to access private journal") },
                trailingContent = {
                    ThemeSwitch(
                        checked = privateJournalLockEnabled,
                        onCheckedChange = { privateJournalLockEnabled = it }
                    )
                }
            )
            ListItem("""
content = content.replace("            ListItem(\n                headlineContent = { Text(\"Enable App Password\") },", journal_lock_item + "\n                headlineContent = { Text(\"Enable App Password\") },")


with open("app/src/main/java/com/example/ui/screens/SecuritySettingsScreen.kt", "w") as f:
    f.write(content)

