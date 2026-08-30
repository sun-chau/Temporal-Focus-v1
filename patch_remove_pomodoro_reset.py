import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Try to find the list item containing "Hard Reset Pomodoro" and remove it.
start_str = '            ListItem(\n                headlineContent = { Text("Hard Reset Pomodoro") },'
end_str = '            ListItem(\n                headlineContent = { Text("Factory Reset User Data"'

if start_str in content and end_str in content:
    idx_start = content.find(start_str)
    idx_end = content.find(end_str)
    content = content[:idx_start] + content[idx_end:]

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

