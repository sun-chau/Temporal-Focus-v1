import re

def process_syllabus():
    with open("app/src/main/java/com/example/ui/screens/SyllabusTrackerUI.kt", "r") as f:
        content = f.read()

    # Opt-in and import
    if "import androidx.compose.foundation.ExperimentalFoundationApi" not in content:
        content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable\nimport androidx.compose.foundation.border")
    
    if "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)" not in content:
        content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)")

    # Math fix
    content = content.replace("val weightPerTopic = mod.weightage.toFloat() / mod.subTopics.size", "val weightPerTopic = if (mod.subTopics.isNotEmpty()) mod.weightage.toFloat() / mod.subTopics.size else 0f")
    
    # Input fix
    content = content.replace("val newMods = sub.modules + Module(title = title, weightage = weight.toInt())", "val newMods = sub.modules + Module(title = title, weightage = weight.toIntOrNull() ?: 0)")

    # combinedClickable for subject
    subject_row = """                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(subject.name, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            Text("[ ${subject.priority} PRIORITY ]", fontFamily = FontFamily.Monospace, fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp), color = MaterialTheme.colorScheme.primary)
                        }
                        
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            IconButton(onClick = { expanded = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More")
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                DropdownMenuItem(text = { Text("Edit") }, onClick = { expanded = false; editingSubject = subject })
                                DropdownMenuItem(text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, onClick = { expanded = false; viewModel.deleteSubject(entity, subject.id) })
                            }
                        }
                    }"""
    
    new_subject_row = """                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.combinedClickable(
                            onClick = {},
                            onLongClick = { editingSubject = subject }
                        )
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(subject.name, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            Text("[ ${subject.priority} PRIORITY ]", fontFamily = FontFamily.Monospace, fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp), color = MaterialTheme.colorScheme.primary)
                        }
                    }"""
    
    content = content.replace(subject_row, new_subject_row)

    # combinedClickable for module
    mod_row = """                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("> ${mod.title} (W: ${mod.weightage})", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                                var expanded by remember { mutableStateOf(false) }
                                Box {
                                    IconButton(onClick = { expanded = true }) {
                                        Icon(Icons.Default.MoreVert, contentDescription = "More")
                                    }
                                    DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                        DropdownMenuItem(text = { Text("Edit") }, onClick = { expanded = false; editingModule = Pair(subject.id, mod) })
                                        DropdownMenuItem(text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, onClick = { expanded = false; viewModel.deleteModule(entity, subject.id, mod.id) })
                                    }
                                }
                            }"""
    new_mod_row = """                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .combinedClickable(
                                        onClick = {},
                                        onLongClick = { editingModule = Pair(subject.id, mod) }
                                    )
                                    .padding(vertical = 4.dp)
                            ) {
                                Text("> ${mod.title} (W: ${mod.weightage})", fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                            }"""
    content = content.replace(mod_row, new_mod_row)

    # combinedClickable for subtopic
    st_row = """                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(start = 16.dp)) {
                                    Checkbox(checked = st.isCompleted, onCheckedChange = { c ->
                                        viewModel.updateSubTopic(entity, subject.id, mod.id, st.id, st.title, c)
                                    })
                                    Text(st.title, modifier = Modifier.weight(1f), style = MaterialTheme.typography.bodyMedium)
                                    var expanded by remember { mutableStateOf(false) }
                                    Box {
                                        IconButton(onClick = { expanded = true }) {
                                            Icon(Icons.Default.MoreVert, contentDescription = "More")
                                        }
                                        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                            DropdownMenuItem(text = { Text("Edit") }, onClick = { expanded = false; editingTopic = Triple(subject.id, mod.id, st) })
                                            DropdownMenuItem(text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, onClick = { expanded = false; viewModel.deleteSubTopic(entity, subject.id, mod.id, st.id) })
                                        }
                                    }
                                }"""
    new_st_row = """                                Row(
                                    verticalAlignment = Alignment.CenterVertically, 
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(start = 16.dp)
                                        .combinedClickable(
                                            onClick = {
                                                viewModel.updateSubTopic(entity, subject.id, mod.id, st.id, st.title, !st.isCompleted)
                                            },
                                            onLongClick = { editingTopic = Triple(subject.id, mod.id, st) }
                                        )
                                ) {
                                    Checkbox(checked = st.isCompleted, onCheckedChange = { c ->
                                        viewModel.updateSubTopic(entity, subject.id, mod.id, st.id, st.title, c)
                                    })
                                    Text(st.title, modifier = Modifier.weight(1f), style = MaterialTheme.typography.bodyMedium)
                                }"""
    content = content.replace(st_row, new_st_row)

    # Editing Modals
    # Remove Delete button from dropdown and put it into modal if we removed dropdowns?
    # Wait, the prompt says "trigger the editing... state variables to open the Bottom Sheet modals for editing and deleting."
    # So the bottom sheets need a delete button now, since we removed the dropdown!
    
    # Subject delete
    if 'Button(' in content and 'viewModel.updateSubject' in content and 'Text("DELETE")' not in content:
        content = content.replace(
            """                Button(
                    onClick = { viewModel.updateSubject(entity, sub.id, name, prio); editingSubject = null },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }""",
            """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubject(entity, sub.id, name, prio); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteSubject(entity, sub.id); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
        )

    # Module delete
    if 'Button(' in content and 'viewModel.updateModule' in content and 'Text("DELETE")' not in content:
        content = content.replace(
            """                Button(
                    onClick = { viewModel.updateModule(entity, subId, mod.id, title); editingModule = null },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }""",
            """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateModule(entity, subId, mod.id, title); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteModule(entity, subId, mod.id); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
        )

    # Topic delete
    if 'Button(' in content and 'viewModel.updateSubTopic' in content and 'Text("DELETE")' not in content:
        content = content.replace(
            """                Button(
                    onClick = { viewModel.updateSubTopic(entity, subId, modId, st.id, title, st.isCompleted); editingTopic = null },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }""",
            """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubTopic(entity, subId, modId, st.id, title, st.isCompleted); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteSubTopic(entity, subId, modId, st.id); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
        )

    with open("app/src/main/java/com/example/ui/screens/SyllabusTrackerUI.kt", "w") as f:
        f.write(content)


def process_assignment():
    with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
        content = f.read()

    if "import androidx.compose.foundation.ExperimentalFoundationApi" not in content:
        content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable\nimport androidx.compose.foundation.border")
    
    if "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)" not in content:
        content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)")

    content = content.replace("val sortedTasks = payload.tasks.sortedBy { it.deadlineEpoch }", "val sortedTasks = payload.tasks.sortedWith(compareBy({ it.status }, { it.deadlineEpoch }))")

    clickable_old = """                        .clickable {
                            // Cycle status
                            val newStatus = when (task.status) {
                                AssignmentStatus.PENDING -> AssignmentStatus.IN_PROGRESS
                                AssignmentStatus.IN_PROGRESS -> AssignmentStatus.SUBMITTED
                                AssignmentStatus.SUBMITTED -> AssignmentStatus.PENDING
                            }
                            val newTasks = payload.tasks.map { if (it.id == task.id) it.copy(status = newStatus) else it }
                            viewModel.updateAssignmentPayload(entity, payload.copy(tasks = newTasks))
                        }"""
    clickable_new = """                        .combinedClickable(
                            onClick = {
                                val newStatus = when (task.status) {
                                    AssignmentStatus.PENDING -> AssignmentStatus.IN_PROGRESS
                                    AssignmentStatus.IN_PROGRESS -> AssignmentStatus.SUBMITTED
                                    AssignmentStatus.SUBMITTED -> AssignmentStatus.PENDING
                                }
                                val newTasks = payload.tasks.map { if (it.id == task.id) it.copy(status = newStatus) else it }
                                viewModel.updateAssignmentPayload(entity, payload.copy(tasks = newTasks))
                            },
                            onLongClick = { editingAssignment = task }
                        )"""
    content = content.replace(clickable_old, clickable_new)

    row_old = """                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(task.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            Text("[ ${task.priority} PRIORITY ]", fontFamily = FontFamily.Monospace, fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp), color = MaterialTheme.colorScheme.primary)
                        }
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            IconButton(onClick = { expanded = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More")
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                DropdownMenuItem(text = { Text("Edit") }, onClick = { expanded = false; editingAssignment = task })
                                DropdownMenuItem(text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, onClick = { expanded = false; viewModel.deleteAssignment(entity, task.id) })
                            }
                        }
                    }"""
    row_new = """                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(task.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            Text("[ ${task.priority} PRIORITY ]", fontFamily = FontFamily.Monospace, fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp), color = MaterialTheme.colorScheme.primary)
                        }
                    }"""
    content = content.replace(row_old, row_new)

    if 'Button(' in content and 'viewModel.updateAssignment' in content and 'Text("DELETE")' not in content:
        content = content.replace(
            """                Button(
                    onClick = { viewModel.updateAssignment(entity, task.id, title, prio); editingAssignment = null },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }""",
            """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateAssignment(entity, task.id, title, prio); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteAssignment(entity, task.id); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
        )

    with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
        f.write(content)

def process_custom():
    with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "r") as f:
        content = f.read()

    if "import androidx.compose.foundation.ExperimentalFoundationApi" not in content:
        content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable\nimport androidx.compose.foundation.border")
    
    if "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)" not in content:
        content = content.replace("@OptIn(ExperimentalMaterial3Api::class)", "@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)")

    row_old = """                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "[ ${dateFormatter.format(Date(entry.timestampEpoch)).uppercase(Locale.getDefault())} ]",
                            fontFamily = FontFamily.Monospace,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 12.sp,
                            modifier = Modifier.weight(1f)
                        )
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            IconButton(onClick = { expanded = true }, modifier = Modifier.size(24.dp)) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More", modifier = Modifier.size(20.dp))
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                DropdownMenuItem(
                                    text = { Text("Edit") }, 
                                    onClick = { expanded = false; editingEntry = entry }
                                )
                                DropdownMenuItem(
                                    text = { Text("Delete", color = MaterialTheme.colorScheme.error) }, 
                                    onClick = { expanded = false; viewModel.deleteCustomEntry(entity, entry.id) }
                                )
                            }
                        }
                    }"""
    row_new = """                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "[ ${dateFormatter.format(Date(entry.timestampEpoch)).uppercase(Locale.getDefault())} ]",
                            fontFamily = FontFamily.Monospace,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 12.sp,
                            modifier = Modifier.weight(1f)
                        )
                    }"""
    content = content.replace(row_old, row_new)

    modifier_old = """                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .padding(16.dp)
                ) {"""
    modifier_new = """                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .combinedClickable(
                            onClick = {},
                            onLongClick = { editingEntry = entry }
                        )
                        .padding(16.dp)
                ) {"""
    content = content.replace(modifier_old, modifier_new)

    if 'Button(' in content and 'viewModel.updateCustomEntry' in content and 'Text("DELETE")' not in content:
        content = content.replace(
            """                Button(
                    onClick = {
                        viewModel.updateCustomEntry(entity, entry.id, editValues)
                        editingEntry = null
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape
                ) {
                    Text("SAVE CHANGES")
                }""",
            """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
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
                    OutlinedButton(
                        onClick = {
                            viewModel.deleteCustomEntry(entity, entry.id)
                            editingEntry = null
                        },
                        modifier = Modifier.weight(1f),
                        shape = RectangleShape
                    ) {
                        Text("DELETE", color = MaterialTheme.colorScheme.error)
                    }
                }"""
        )

    with open("app/src/main/java/com/example/ui/screens/CustomTrackerUI.kt", "w") as f:
        f.write(content)

process_syllabus()
process_assignment()
process_custom()

