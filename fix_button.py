path = 'app/src/main/java/com/example/ui/screens/SettingsScreen.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace("val contentColor = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface", "val contentColor = MaterialTheme.colorScheme.primary")
content = content.replace("val borderColor = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)", "val borderColor = MaterialTheme.colorScheme.primary.copy(alpha = if (selected) 1f else 0.5f)")

with open(path, 'w') as f:
    f.write(content)
