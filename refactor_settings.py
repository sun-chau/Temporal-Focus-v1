import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Replace Deadlines with Reminders in SettingsCategoryHeader
content = content.replace('SettingsCategoryHeader("Deadlines")', 'SettingsCategoryHeader("Reminders")')

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
