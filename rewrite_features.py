import sys
import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

pattern = r'''(Column\(\s*modifier = Modifier\s*\.fillMaxSize\(\)\s*\.padding\(padding\)\s*\.verticalScroll\(rememberScrollState\(\)\)\s*\)\s*\{)(.*?)(        \}\n    \}\n    if \(showSlotsDialog\))'''

def repl(match):
    prefix = match.group(1)
    inner = match.group(2)
    suffix = match.group(3)

    new_inner = """
            SettingsCategoryHeader("Deadlines")""" + inner + """
            androidx.compose.material3.HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
            SettingsCategoryHeader("Daily Schedule")

            ListItem(
                headlineContent = { Text("24-Hour Time Format") },
                supportingContent = { Text("Use 24-hour format instead of 12-hour AM/PM") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.AccessTime, contentDescription = null) },
                trailingContent = { ThemeSwitch(checked = uiState.use24HourFormat, onCheckedChange = { viewModel.setUse24HourFormat(it) }) }
            )
            ListItem(
                headlineContent = { Text("Default Status if Missed") },
                supportingContent = { Text("Automatically mark past tasks as: ${uiState.autoStatusIfMissed}") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.Update, contentDescription = null) },
                modifier = Modifier.clickable { showAutoStatusDialog = true }
            )"""
            
    return "    var showAutoStatusDialog by remember { mutableStateOf(false) }\n    " + prefix + new_inner + "\n" + suffix

content = re.sub(pattern, repl, content, flags=re.DOTALL)

# Add the new dialog
new_dialog = """    if (showAutoStatusDialog) {
        AlertDialog(
            onDismissRequest = { showAutoStatusDialog = false },
            title = { Text("Status if Missed") },
            text = {
                Column {
                    listOf("NOT_DONE", "COMPLETED", "SKIPPED").forEach { status ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    viewModel.setAutoStatusIfMissed(status)
                                    showAutoStatusDialog = false
                                }
                                .padding(vertical = 12.dp)
                        ) {
                            RadioButton(
                                selected = uiState.autoStatusIfMissed == status,
                                onClick = null
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(text = status)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showAutoStatusDialog = false }) {
                    Text("Close")
                }
            }
        )
    }"""
content = content.replace("    if (showSlotsDialog) {", new_dialog + "\n\n    if (showSlotsDialog) {")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

