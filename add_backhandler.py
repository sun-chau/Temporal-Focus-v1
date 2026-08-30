import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Add import
if "import androidx.activity.compose.BackHandler" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.activity.compose.BackHandler\nimport androidx.compose.ui.Alignment")

search_str = '''    var showFeedbackDialog by remember { mutableStateOf(false) }'''

replace_str = '''    var showFeedbackDialog by remember { mutableStateOf(false) }

    BackHandler(enabled = drawerState.isOpen) {
        scope.launch { drawerState.close() }
    }

    BackHandler(enabled = !drawerState.isOpen && uiState.isCreatingChronometer) {
        viewModel.setEditingTask(null)
        viewModel.setCreatingChronometer(false)
    }

    BackHandler(enabled = !drawerState.isOpen && !uiState.isCreatingChronometer && uiState.currentMode != TimerMode.HOME) {
        viewModel.setTimerMode(TimerMode.HOME)
    }'''

content = content.replace(search_str, replace_str)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
