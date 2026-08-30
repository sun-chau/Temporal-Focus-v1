import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

content = content.replace("                        uiState = uiState,\n                        viewModel = viewModel,\n    tasks: List<TimerTask>,", "    tasks: List<TimerTask>,")

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
