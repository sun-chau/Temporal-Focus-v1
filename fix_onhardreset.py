path = 'app/src/main/java/com/example/ui/screens/PomodoroScreen.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    "PomodoroStatsOverlay(uiState, onDismiss = { showStats = false }, onHardReset = { viewModel.hardResetPomodoro() }, isPeeking = isPeeking)",
    "PomodoroStatsOverlay(uiState, onDismiss = { showStats = false }, isPeeking = isPeeking)"
)

content = content.replace(
    "fun PomodoroStatsOverlay(uiState: UiState, onDismiss: () -> Unit, onHardReset: () -> Unit, isPeeking: Boolean = false) {",
    "fun PomodoroStatsOverlay(uiState: UiState, onDismiss: () -> Unit, isPeeking: Boolean = false) {"
)

with open(path, 'w') as f:
    f.write(content)
