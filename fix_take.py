import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'activeTasks.sortedBy { it.targetDateTime }.take(uiState.maxStageSlots).size',
    'activeTasks.sortedBy { it.targetDateTime }.let { if (uiState.maxStageSlots == -1) it else it.take(uiState.maxStageSlots) }.size'
)

content = content.replace(
    'activeTasks.sortedBy { it.targetDateTime }.take(uiState.maxStageSlots)',
    'activeTasks.sortedBy { it.targetDateTime }.let { if (uiState.maxStageSlots == -1) it else it.take(uiState.maxStageSlots) }'
)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
