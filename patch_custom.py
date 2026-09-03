import re

with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "r") as f:
    content = f.read()

# SAVE FIELD (Add Modal)
field_old = """                Button(
                    onClick = {
                        if (label.isNotBlank()) {
                            pendingSchema = pendingSchema + CustomField(label = label, fieldType = type)
                            showAddField = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape
                ) {
                    Text("SAVE FIELD")
                }"""
field_new = """                val hasChanges = label.isNotBlank()
                Button(
                    onClick = {
                        if (label.isNotBlank()) {
                            pendingSchema = pendingSchema + CustomField(label = label, fieldType = type)
                            showAddField = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape,
                    enabled = hasChanges
                ) {
                    Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                }"""
content = content.replace(field_old, field_new)

# Edit Entry
edit_old = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            viewModel.updateCustomEntry(entity, entry.id, editValues)
                            editingEntry = null
                        },
                        modifier = Modifier.weight(1f),
                        shape = RectangleShape
                    ) {
                        Text("SAVE")
                    }
                    OutlinedButton("""
edit_new = """                val hasChanges = editValues != entry.fieldData
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            viewModel.updateCustomEntry(entity, entry.id, editValues)
                            editingEntry = null
                        },
                        modifier = Modifier.weight(1f),
                        shape = RectangleShape,
                        enabled = hasChanges
                    ) {
                        Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                    }
                    OutlinedButton("""
content = content.replace(edit_old, edit_new)

with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "w") as f:
    f.write(content)

