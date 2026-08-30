path = 'app/src/main/java/com/example/ui/screens/MainScreen.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace("var showProfileScreen by remember { mutableStateOf(false) }", "var showProfileScreen by remember { mutableStateOf(false) }\n    var showSettingsScreen by remember { mutableStateOf(false) }")
content = content.replace("if (showProfileScreen) {\n        UserAccountScreen(viewModel = viewModel, uiState = uiState, onBack = { showProfileScreen = false })\n        return\n    }", "if (showProfileScreen) {\n        UserAccountScreen(viewModel = viewModel, uiState = uiState, onBack = { showProfileScreen = false })\n        return\n    }\n\n    if (showSettingsScreen) {\n        SettingsScreen(viewModel = viewModel, uiState = uiState, onBack = { showSettingsScreen = false })\n        return\n    }")

content = content.replace("""                        onClick = {
                            scope.launch { drawerState.close() }
                            android.widget.Toast.makeText(context, "Settings coming soon", android.widget.Toast.LENGTH_SHORT).show()
                        },""", """                        onClick = {
                            scope.launch { drawerState.close() }
                            showSettingsScreen = true
                        },""")

with open(path, 'w') as f:
    f.write(content)
