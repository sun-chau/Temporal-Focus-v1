import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Try to find the block for showHardResetDialog
start_str = '    if (showHardResetDialog) {'
end_str = '    if (showFactoryResetDialog) {'

if start_str in content and end_str in content:
    idx_start = content.find(start_str)
    idx_end = content.find(end_str)
    content = content[:idx_start] + content[idx_end:]

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

