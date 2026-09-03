import re

with open("app/src/main/java/com/example/ui/screens/SyllabusTrackerUI.kt", "r") as f:
    content = f.read()

# Add Subject
add_sub_old = """                Button(
                    onClick = {
                        if (subjectName.isNotBlank()) {
                            val newSubject = Subject(name = subjectName)
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = payload.subjects + newSubject))
                            showAddSubject = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape
                ) {
                    Text("SAVE")
                }"""
add_sub_new = """                val hasChanges = subjectName.isNotBlank()
                Button(
                    onClick = {
                        if (subjectName.isNotBlank()) {
                            val newSubject = Subject(name = subjectName)
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = payload.subjects + newSubject))
                            showAddSubject = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape,
                    enabled = hasChanges
                ) {
                    Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                }"""
content = content.replace(add_sub_old, add_sub_new)

# Edit Subject
edit_sub_old = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubject(entity, sub.id, name, prio); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteSubject(entity, sub.id); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
edit_sub_new = """                val hasChanges = name != sub.name || prio != sub.priority
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubject(entity, sub.id, name, prio); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteSubject(entity, sub.id); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
content = content.replace(edit_sub_old, edit_sub_new)

# Add Module
add_mod_old = """                Button(
                    onClick = { 
                        if (title.isNotBlank() && weight.isNotBlank()) {
                            val newMods = sub.modules + Module(title = title, weightage = weight.toIntOrNull() ?: 0)
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = payload.subjects.map { if (it.id == sub.id) sub.copy(modules = newMods) else it }))
                            addingModuleToSubject = null
                        }
                    },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }"""
add_mod_new = """                val hasChanges = title.isNotBlank() && weight.isNotBlank()
                Button(
                    onClick = { 
                        if (title.isNotBlank() && weight.isNotBlank()) {
                            val newMods = sub.modules + Module(title = title, weightage = weight.toIntOrNull() ?: 0)
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = payload.subjects.map { if (it.id == sub.id) sub.copy(modules = newMods) else it }))
                            addingModuleToSubject = null
                        }
                    },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape, enabled = hasChanges
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }"""
content = content.replace(add_mod_old, add_mod_new)


# Edit Module
edit_mod_old = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateModule(entity, subId, mod.id, title); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteModule(entity, subId, mod.id); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
edit_mod_new = """                val hasChanges = title != mod.title || weight != mod.weightage.toString()
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateModule(entity, subId, mod.id, title); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteModule(entity, subId, mod.id); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
content = content.replace(edit_mod_old, edit_mod_new)


# Add Topic
add_top_old = """                Button(
                    onClick = { 
                        if (title.isNotBlank()) {
                            val newSubjects = payload.subjects.map { s ->
                                if (s.id == subId) {
                                    s.copy(modules = s.modules.map { m ->
                                        if (m.id == mod.id) {
                                            m.copy(subTopics = m.subTopics + SubTopic(title = title))
                                        } else m
                                    })
                                } else s
                            }
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = newSubjects))
                            addingTopicToModule = null
                        }
                    },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape
                ) { Text("SAVE") }"""
add_top_new = """                val hasChanges = title.isNotBlank()
                Button(
                    onClick = { 
                        if (title.isNotBlank()) {
                            val newSubjects = payload.subjects.map { s ->
                                if (s.id == subId) {
                                    s.copy(modules = s.modules.map { m ->
                                        if (m.id == mod.id) {
                                            m.copy(subTopics = m.subTopics + SubTopic(title = title))
                                        } else m
                                    })
                                } else s
                            }
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = newSubjects))
                            addingTopicToModule = null
                        }
                    },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape, enabled = hasChanges
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }"""
content = content.replace(add_top_old, add_top_new)


# Edit Topic
edit_top_old = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubTopic(entity, subId, modId, st.id, title, st.isCompleted); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("SAVE") }
                    OutlinedButton(onClick = { viewModel.deleteSubTopic(entity, subId, modId, st.id); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
edit_top_new = """                val hasChanges = title != st.title
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubTopic(entity, subId, modId, st.id, title, st.isCompleted); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteSubTopic(entity, subId, modId, st.id); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }"""
content = content.replace(edit_top_old, edit_top_new)

with open("app/src/main/java/com/example/ui/screens/SyllabusTrackerUI.kt", "w") as f:
    f.write(content)

