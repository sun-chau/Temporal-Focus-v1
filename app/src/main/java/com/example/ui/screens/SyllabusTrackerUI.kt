package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun SyllabusTrackerUI(entity: TrackerEntity, payload: SyllabusPayload, viewModel: TrackerViewModel) {
    var showAddSubject by remember { mutableStateOf(false) }
    
    // Edit modals state
    var editingSubject by remember { mutableStateOf<Subject?>(null) }
    var addingModuleToSubject by remember { mutableStateOf<Subject?>(null) }
    var editingModule by remember { mutableStateOf<Pair<String, Module>?>(null) } // subjectId to Module
    var addingTopicToModule by remember { mutableStateOf<Pair<String, Module>?>(null) }
    var editingTopic by remember { mutableStateOf<Triple<String, String, SubTopic>?>(null) } // subId, modId to SubTopic

    Column(modifier = Modifier.fillMaxSize()) {
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(payload.subjects) { subject ->
                // Calculate progress
                val totalWeight = subject.modules.flatMap { it.subTopics }.size.toFloat() // Using size for simplicity, or sum of weightage? Prompt says: (Sum of weightage of completed sub-topics) / (Total sum of all weightages in the subject). Wait, subtopic doesn't have weightage, Module has weightage.
                // Let's assume each subtopic takes a fraction of the module's weightage.
                // Module weightage / number of subtopics = weight per subtopic.
                val totalSubjectWeight = subject.modules.sumOf { it.weightage }.toFloat()
                var completedWeight = 0f
                subject.modules.forEach { mod ->
                    if (mod.subTopics.isNotEmpty()) {
                        val weightPerTopic = if (mod.subTopics.isNotEmpty()) mod.weightage.toFloat() / mod.subTopics.size else 0f
                        completedWeight += mod.subTopics.count { it.isCompleted } * weightPerTopic
                    }
                }
                val progress = if (totalSubjectWeight > 0f) completedWeight / totalSubjectWeight else 0f

                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .padding(16.dp)
                ) {
                    Row(
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
                    }

                    Spacer(Modifier.height(8.dp))
                    LinearProgressIndicator(
                        progress = { progress },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(12.dp),
                        trackColor = MaterialTheme.colorScheme.surfaceVariant,
                        color = MaterialTheme.colorScheme.primary,
                        strokeCap = StrokeCap.Square
                    )
                    Spacer(Modifier.height(16.dp))

                    subject.modules.forEach { mod ->
                        Column(modifier = Modifier.fillMaxWidth().padding(start = 8.dp, bottom = 8.dp)) {
                            Row(
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
                            }
                            
                            mod.subTopics.forEach { st ->
                                Row(
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
                                }
                            }
                            
                            TextButton(onClick = { addingTopicToModule = Pair(subject.id, mod) }) {
                                Text("+ ADD TOPIC", fontFamily = FontFamily.Monospace)
                            }
                        }
                    }
                    
                    OutlinedButton(
                        onClick = { addingModuleToSubject = subject },
                        shape = RectangleShape,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("+ ADD MODULE")
                    }
                }
            }
        }
        Button(
            onClick = { showAddSubject = true },
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp),
            shape = RectangleShape
        ) {
            Text("+ ADD SUBJECT")
        }
    }

    if (showAddSubject) {
        var subjectName by remember { mutableStateOf("") }
        ModalBottomSheet(onDismissRequest = { showAddSubject = false }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Subject", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = subjectName,
                    onValueChange = { subjectName = it },
                    label = { Text("Subject Name") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                val hasChanges = subjectName.isNotBlank()
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
                }
            }
        }
    }
    
    editingSubject?.let { sub ->
        var name by remember { mutableStateOf(sub.name) }
        var prio by remember { mutableStateOf(sub.priority) }
        ModalBottomSheet(onDismissRequest = { editingSubject = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Edit Subject", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth())
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    PriorityLevel.values().forEach { p ->
                        FilterChip(selected = prio == p, onClick = { prio = p }, label = { Text("[ $p ]") })
                    }
                }
                val hasChanges = name != sub.name || prio != sub.priority
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubject(entity, sub.id, name, prio); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteSubject(entity, sub.id); editingSubject = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }
            }
        }
    }
    
    addingModuleToSubject?.let { sub ->
        var title by remember { mutableStateOf("") }
        var weight by remember { mutableStateOf("") }
        ModalBottomSheet(onDismissRequest = { addingModuleToSubject = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Module", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = weight, onValueChange = { weight = it.filter { c -> c.isDigit() } }, label = { Text("Weightage") }, modifier = Modifier.fillMaxWidth())
                val hasChanges = title.isNotBlank() && weight.isNotBlank()
                Button(
                    onClick = { 
                        if (title.isNotBlank() && weight.isNotBlank()) {
                            val newMods = sub.modules + Module(title = title, weightage = weight.toIntOrNull() ?: 0)
                            viewModel.updateSyllabusPayload(entity, payload.copy(subjects = payload.subjects.map { if (it.id == sub.id) sub.copy(modules = newMods) else it }))
                            addingModuleToSubject = null
                        }
                    },
                    modifier = Modifier.fillMaxWidth(), shape = RectangleShape, enabled = hasChanges
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
            }
        }
    }
    
    editingModule?.let { (subId, mod) ->
        var title by remember { mutableStateOf(mod.title) }
        var weight by remember { mutableStateOf(mod.weightage.toString()) }
        ModalBottomSheet(onDismissRequest = { editingModule = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Edit Module", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                // Weightage edit not explicitly asked in ViewModel mutations, but good to have.
                // Wait, I only added updateModule(..., newTitle). Let me just edit the title.
                val hasChanges = title != mod.title || weight != mod.weightage.toString()
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateModule(entity, subId, mod.id, title); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteModule(entity, subId, mod.id); editingModule = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }
            }
        }
    }
    
    addingTopicToModule?.let { (subId, mod) ->
        var title by remember { mutableStateOf("") }
        ModalBottomSheet(onDismissRequest = { addingTopicToModule = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Topic", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                val hasChanges = title.isNotBlank()
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
                ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
            }
        }
    }
    
    editingTopic?.let { (subId, modId, st) ->
        var title by remember { mutableStateOf(st.title) }
        ModalBottomSheet(onDismissRequest = { editingTopic = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Edit Topic", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                val hasChanges = title != st.title
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { viewModel.updateSubTopic(entity, subId, modId, st.id, title, st.isCompleted); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape, enabled = hasChanges) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteSubTopic(entity, subId, modId, st.id); editingTopic = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }
            }
        }
    }
}
