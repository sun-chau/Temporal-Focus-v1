import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Update blockBorderColor
old_line1 = "val blockBorderColor = if (isUncategorized) MaterialTheme.colorScheme.outlineVariant else tagColor.copy(alpha = borderOpacity)"
new_line1 = "val blockBorderColor = if (isUncategorized) MaterialTheme.colorScheme.onSurface else tagColor.copy(alpha = borderOpacity)"
content = content.replace(old_line1, new_line1)

# Update radio button border
old_line2 = ".then(if (isUncategorized) Modifier.border(2.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape) else Modifier)"
new_line2 = ".then(if (isUncategorized) Modifier.border(2.dp, MaterialTheme.colorScheme.onSurface, CircleShape) else Modifier)"
content = content.replace(old_line2, new_line2)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)

