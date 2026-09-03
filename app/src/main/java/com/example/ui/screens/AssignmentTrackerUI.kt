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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun AssignmentTrackerUI(entity: TrackerEntity, payload: AssignmentPayload, viewModel: TrackerViewModel) {
    var showAddAssignment by remember { mutableStateOf(false) }
    var editingAssignment by remember { mutableStateOf<Deliverable?>(null) }
    
    val sortedTasks = payload.tasks.sortedWith(compareBy({ it.status }, { it.deadlineEpoch }))
    Column(modifier = Modifier.fillMaxSize()) {
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(sortedTasks) { task ->
                val statusColor = when (task.status) {
                    AssignmentStatus.PENDING -> Color.Gray
                    AssignmentStatus.IN_PROGRESS -> MaterialTheme.colorScheme.primary
                    AssignmentStatus.SUBMITTED -> Color(0xFF4CAF50)
                }
                
                val daysRemaining = ((task.deadlineEpoch - System.currentTimeMillis()) / (1000 * 60 * 60 * 24)).toInt()
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .combinedClickable(
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
                        )
                        .padding(16.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "[ ${task.status.name.replace("_", " ")} ]",
                            fontFamily = FontFamily.Monospace,
                            color = statusColor,
                            style = MaterialTheme.typography.labelMedium
                        )
                        Spacer(Modifier.weight(1f))
                        Text(
                            text = "T-${if (daysRemaining >= 0) daysRemaining else daysRemaining} DAYS",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            color = if (daysRemaining < 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
                        )
                    }
                    Spacer(Modifier.height(8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(task.title, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
                            Text("[ ${task.priority} PRIORITY ]", fontFamily = FontFamily.Monospace, fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp), color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }
            }
        }
        Button(
            onClick = { showAddAssignment = true },
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 16.dp),
            shape = RectangleShape
        ) {
            Text("+ ADD DELIVERABLE")
        }
    }
    
    if (showAddAssignment) {
        var deliverableTitle by remember { mutableStateOf("") }
        var daysUntilDeadline by remember { mutableStateOf("") }
        ModalBottomSheet(onDismissRequest = { showAddAssignment = false }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Deliverable", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = deliverableTitle,
                    onValueChange = { deliverableTitle = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                
                OutlinedTextField(
                    value = daysUntilDeadline,
                    onValueChange = { daysUntilDeadline = it.filter { char -> char.isDigit() } },
                    label = { Text("Days until deadline") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                val hasChanges = deliverableTitle.isNotBlank()
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
                }
            }
        }
    }

    editingAssignment?.let { task ->
        var title by remember { mutableStateOf(task.title) }
        var prio by remember { mutableStateOf(task.priority) }
        ModalBottomSheet(onDismissRequest = { editingAssignment = null }) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp).padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Edit Deliverable", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    PriorityLevel.values().forEach { p ->
                        FilterChip(selected = prio == p, onClick = { prio = p }, label = { Text("[ $p ]") })
                    }
                }
                val hasChanges = title != task.title || prio != task.priority
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = { viewModel.updateAssignment(entity, task.id, title, prio); editingAssignment = null },
                        modifier = Modifier.weight(1f),
                        shape = RectangleShape,
                        enabled = hasChanges
                    ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
                    OutlinedButton(onClick = { viewModel.deleteAssignment(entity, task.id); editingAssignment = null }, modifier = Modifier.weight(1f), shape = RectangleShape) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }
            }
        }
    }
}
