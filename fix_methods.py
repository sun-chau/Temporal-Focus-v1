import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace('viewModel.setChronometerLayout', 'viewModel.setLayoutPreference')
content = re.sub(r'viewModel.toggleUnitVisibility\("([^"]+)", it\)', r'viewModel.toggleUnitVisibility("\1")', content)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
