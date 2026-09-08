import re

with open("app/src/main/java/com/example/ui/screens/BinaryTrackerUI.kt", "r") as f:
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
            Text("+ ADD DISCIPLINE", fontWeight = FontWeight.Bold)
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
            Icon(Icons.Filled.Add, contentDescription = "Add Discipline")
        }
    }"""

new_fab = """        }
    }"""

content = content.replace(old_fab, new_fab)

# Update Save Button
old_save = """        confirmButton = {
            TextButton(
                onClick = {
                    if (name.isNotBlank()) onSave(name)
                }
            ) { Text("SAVE") }
        },"""

new_save = """        confirmButton = {
            val hasChanges = name != initialName && name.isNotBlank()
            TextButton(
                onClick = { if (name.isNotBlank()) onSave(name) },
                enabled = hasChanges
            ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
        },"""

content = content.replace(old_save, new_save)

# Add import for RectangleShape
if "import androidx.compose.ui.graphics.RectangleShape" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.graphics.RectangleShape")


with open("app/src/main/java/com/example/ui/screens/BinaryTrackerUI.kt", "w") as f:
    f.write(content)

