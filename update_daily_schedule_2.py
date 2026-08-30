import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Remove the "Today" TopAppBar button
target1 = """                    IconButton(onClick = { 
                        coroutineScope.launch {
                                scrollToNowTrigger++
                            }
                    }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Today, contentDescription = "Today")
                    }
                    IconButton(onClick = { showDatePicker = true }) {"""

replacement1 = """                    IconButton(onClick = { showDatePicker = true }) {"""
content = content.replace(target1, replacement1)

# 2. Change FAB icon
target2 = """Icon(androidx.compose.material.icons.Icons.Default.LocationSearching, contentDescription = "Now")"""
replacement2 = """Icon(androidx.compose.material.icons.Icons.Default.Today, contentDescription = "Now")"""
content = content.replace(target2, replacement2)

# 3. Increase border thickness for uncategorized tasks
target3 = """val blockBorderWidth = if (isUncategorized) 1.dp else 2.dp"""
replacement3 = """val blockBorderWidth = if (isUncategorized) 2.dp else 2.dp"""
content = content.replace(target3, replacement3)

# And also increase the border thickness in the status icon
target4 = """.then(if (isUncategorized) Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape) else Modifier)"""
replacement4 = """.then(if (isUncategorized) Modifier.border(2.dp, MaterialTheme.colorScheme.outlineVariant, CircleShape) else Modifier)"""
content = content.replace(target4, replacement4)

# 4. Make dashed line more visible
target5 = """val outlineColor = MaterialTheme.colorScheme.outlineVariant"""
replacement5 = """val outlineColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)"""
content = content.replace(target5, replacement5)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Updated successfully")
