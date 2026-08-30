with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'Spacer(modifier = Modifier.height(80.dp)) // space for FAB',
    'TacticalStatsGrid(uiState)\n            Spacer(modifier = Modifier.height(80.dp)) // space for FAB'
)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
