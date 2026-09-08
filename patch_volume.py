import re

with open("app/src/main/java/com/example/ui/screens/VolumeTrackerUI.kt", "r") as f:
    content = f.read()

# Replace Box and LazyColumn
old_layout = """    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 80.dp)
        ) {"""

new_layout = """    Column(modifier = Modifier.fillMaxSize()) {
        Button(
            onClick = { showAddDialog = true },
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            shape = RectangleShape
        ) {
            Text("+ ADD RESOURCE", fontWeight = FontWeight.Bold)
        }
        LazyColumn(
            modifier = Modifier.weight(1f)
        ) {"""

content = content.replace(old_layout, new_layout)

# Remove FAB
old_fab = """        }
        FloatingActionButton(
            onClick = { showAddDialog = true },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            Icon(Icons.Filled.Add, contentDescription = "Add Resource")
        }
    }"""

new_fab = """        }
    }"""

content = content.replace(old_fab, new_fab)

# Update Save Button
old_save = """        confirmButton = {
            TextButton(
                onClick = {
                    val t = total.toIntOrNull()
                    if (title.isNotBlank() && t != null && t > 0) {
                        onSave(title, t, metric.ifBlank { "Units" })
                    }
                }
            ) { Text("SAVE") }
        },"""

new_save = """        confirmButton = {
            val hasChanges = title != initialTitle || total != initialTotal || metric != initialMetric
            val t = total.toIntOrNull()
            val isValid = title.isNotBlank() && t != null && t > 0
            TextButton(
                onClick = { if (isValid) onSave(title, t!!, metric.ifBlank { "Units" }) },
                enabled = hasChanges && isValid
            ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
        },"""

content = content.replace(old_save, new_save)

# LinearProgressIndicator
old_lpi = """                        modifier = Modifier
                            .fillMaxWidth()
                            .height(12.dp)
                    )"""

new_lpi = """                        modifier = Modifier
                            .fillMaxWidth()
                            .height(12.dp),
                        strokeCap = androidx.compose.ui.graphics.StrokeCap.Square
                    )"""

content = content.replace(old_lpi, new_lpi)

# Numpad shape
old_numpad_shape = """                            .background(
                                color = if (key == "LOG") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                shape = MaterialTheme.shapes.medium
                            )"""

new_numpad_shape = """                            .background(
                                color = if (key == "LOG") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                shape = RectangleShape
                            )"""

content = content.replace(old_numpad_shape, new_numpad_shape)


# Add import for RectangleShape if missing
if "import androidx.compose.ui.graphics.RectangleShape" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.graphics.RectangleShape")

with open("app/src/main/java/com/example/ui/screens/VolumeTrackerUI.kt", "w") as f:
    f.write(content)

