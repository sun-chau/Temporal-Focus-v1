import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add clipboardManager
content = content.replace("fun SettingsScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {", "fun SettingsScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {\n    val clipboardManager = androidx.compose.ui.platform.LocalClipboardManager.current\n    val context = androidx.compose.ui.platform.LocalContext.current")

search_data_mgmt = "            SettingsCategoryHeader(\"Data Management\")"

replace_data_mgmt = """            SettingsCategoryHeader("Data Management")
            
            ListItem(
                headlineContent = { Text("Export Data") },
                supportingContent = { Text("Copy all data to clipboard as JSON") },
                modifier = Modifier.clickable {
                    val json = viewModel.exportData()
                    clipboardManager.setText(androidx.compose.ui.text.AnnotatedString(json))
                    android.widget.Toast.makeText(context, "Exported to Clipboard", android.widget.Toast.LENGTH_SHORT).show()
                }
            )
            
            ListItem(
                headlineContent = { Text("Import Data") },
                supportingContent = { Text("Load data from clipboard JSON") },
                modifier = Modifier.clickable {
                    val json = clipboardManager.getText()?.text
                    if (!json.isNullOrBlank()) {
                        viewModel.importData(json.toString())
                        android.widget.Toast.makeText(context, "Data Imported", android.widget.Toast.LENGTH_SHORT).show()
                    } else {
                        android.widget.Toast.makeText(context, "Clipboard is empty", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            )"""

content = content.replace(search_data_mgmt, replace_data_mgmt)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
