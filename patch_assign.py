import re

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
    content = f.read()

add_old = """                Button(
                    onClick = {
                        val days = daysUntilDeadline.toLongOrNull() ?: 0L
                        if (deliverableTitle.isNotBlank()) {
                            val targetEpoch = System.currentTimeMillis() + (days * 24 * 60 * 60 * 1000)
                            val newTask = Deliverable(title = deliverableTitle, deadlineEpoch = targetEpoch)
                            viewModel.updateAssignmentPayload(entity, payload.copy(tasks = payload.tasks + newTask))
                            showAddAssignment = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape
                ) {
                    Text("SAVE")
                }"""

add_new = """                val hasChanges = deliverableTitle.isNotBlank()
                Button(
                    onClick = {
                        val days = daysUntilDeadline.toLongOrNull() ?: 0L
                        if (deliverableTitle.isNotBlank()) {
                            val targetEpoch = System.currentTimeMillis() + (days * 24 * 60 * 60 * 1000)
                            val newTask = Deliverable(title = deliverableTitle, deadlineEpoch = targetEpoch)
                            viewModel.updateAssignmentPayload(entity, payload.copy(tasks = payload.tasks + newTask))
                            showAddAssignment = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape,
                    enabled = hasChanges
                ) {
                    Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                }"""
content = content.replace(add_old, add_new)


edit_old = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateAssignment(entity, task.id, title, prio); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteAssignment(entity, task.id); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
edit_new = """                val hasChanges = title != task.title || prio != task.priority
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = { viewModel.updateAssignment(entity, task.id, title, prio); editingAssignment = null },
                        modifier = Modifier.weight(1f),
                        shape = RectangleShape,
                        enabled = hasChanges
                    ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteAssignment(entity, task.id); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
content = content.replace(edit_old, edit_new)


with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
    f.write(content)

