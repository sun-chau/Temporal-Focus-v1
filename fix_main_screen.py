import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

# Add import for viewModels
if 'import androidx.lifecycle.viewmodel.compose.viewModel' not in content:
    content = content.replace('import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.dp\nimport androidx.lifecycle.viewmodel.compose.viewModel\nimport com.example.viewmodel.TrackerViewModel')

# Update CheckInsScreen to TrackerDashboardScreen and pass TrackerViewModel
content = content.replace(
    'TimerMode.CHECK_INS -> CheckInsScreen(viewModel = viewModel,',
    'TimerMode.CHECK_INS -> TrackerDashboardScreen(viewModel = viewModel(),'
)

# In case it was already partially replaced:
content = content.replace(
    'TimerMode.CHECK_INS -> TrackerDashboardScreen(viewModel = viewModel,',
    'TimerMode.CHECK_INS -> TrackerDashboardScreen(viewModel = viewModel(),'
)


with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)
