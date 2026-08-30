import re

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "r") as f:
    content = f.read()

# Add to TimerMode mappings in MainScreen
new_mapping = """                            TimerMode.SETTINGS_FEATURE -> SettingsFeatureScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })
                            TimerMode.SETTINGS_DAILY_SCHEDULE -> SettingsDailyScheduleScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_FEATURE) })
                            TimerMode.SETTINGS_REMINDERS -> SettingsRemindersScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS_FEATURE) })"""

content = content.replace("                            TimerMode.SETTINGS_FEATURE -> SettingsFeatureScreen(viewModel = viewModel, uiState = uiState, onBack = { viewModel.setTimerMode(TimerMode.SETTINGS) })", new_mapping)

with open("app/src/main/java/com/example/ui/screens/MainScreen.kt", "w") as f:
    f.write(content)
