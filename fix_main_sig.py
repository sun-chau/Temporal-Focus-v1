import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

bad_sheet = "com.example.ui.components.QuickDeadlineSheet(viewModel = viewModel, uiState = uiState)"

good_sheet = """com.example.ui.components.QuickDeadlineSheet(
            onDismiss = { viewModel.setQuickDeadlineSheet(false) },
            onSave = { name, time -> viewModel.addQuickDeadline(name, time) }
        )"""

content = content.replace(bad_sheet, good_sheet)

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)

