package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.time.LocalDate
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun BinaryTrackerUI(
    entity: TrackerEntity,
    payload: BinaryPayload,
    viewModel: TrackerViewModel
) {
    val today = LocalDate.now().toString()
    var editingDiscipline by remember { mutableStateOf<BinaryDiscipline?>(null) }
    var showAddDialog by remember { mutableStateOf(false) }

    Column(modifier = Modifier.fillMaxSize()) {
        Button(
            onClick = { showAddDialog = true },
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            shape = RectangleShape
        ) {
            Text("+ ADD DISCIPLINE", fontWeight = FontWeight.Bold)
        }
        LazyColumn(
            modifier = Modifier.weight(1f)
        ) {
            items(payload.disciplines, key = { it.id }) { discipline ->
                val isDoneToday = discipline.completedDates.contains(today)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .combinedClickable(
                            onClick = {
                                val newDates = if (isDoneToday) {
                                    discipline.completedDates - today
                                } else {
                                    discipline.completedDates + today
                                }
                                val updated = payload.disciplines.map {
                                    if (it.id == discipline.id) it.copy(completedDates = newDates) else it
                                }
                                viewModel.updateBinaryPayload(entity, payload.copy(disciplines = updated))
                            },
                            onLongClick = {
                                editingDiscipline = discipline
                            }
                        )
                        .padding(vertical = 12.dp, horizontal = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = discipline.name,
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.weight(1f)
                    )
                    Checkbox(
                        checked = isDoneToday,
                        onCheckedChange = null,
                        modifier = Modifier.size(32.dp)
                    )
                }
                Divider()
            }
        }
    }

    if (showAddDialog) {
        DisciplineEditDialog(
            initialName = "",
            onDismiss = { showAddDialog = false },
            onSave = { name ->
                val newDisc = BinaryDiscipline(id = UUID.randomUUID().toString(), name = name)
                viewModel.updateBinaryPayload(entity, payload.copy(disciplines = payload.disciplines + newDisc))
                showAddDialog = false
            }
        )
    }

    editingDiscipline?.let { disc ->
        DisciplineEditDialog(
            initialName = disc.name,
            onDismiss = { editingDiscipline = null },
            onSave = { name ->
                val updated = payload.disciplines.map { if (it.id == disc.id) it.copy(name = name) else it }
                viewModel.updateBinaryPayload(entity, payload.copy(disciplines = updated))
                editingDiscipline = null
            },
            onDelete = {
                val updated = payload.disciplines.filter { it.id != disc.id }
                viewModel.updateBinaryPayload(entity, payload.copy(disciplines = updated))
                editingDiscipline = null
            }
        )
    }
}

@Composable
fun DisciplineEditDialog(
    initialName: String,
    onDismiss: () -> Unit,
    onSave: (String) -> Unit,
    onDelete: (() -> Unit)? = null
) {
    var name by remember { mutableStateOf(initialName) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Discipline") },
        text = {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
        },
        confirmButton = {
            val hasChanges = name != initialName && name.isNotBlank()
            TextButton(
                onClick = { if (name.isNotBlank()) onSave(name) },
                enabled = hasChanges
            ) { Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold) }
        },
        dismissButton = {
            Row {
                if (onDelete != null) {
                    TextButton(onClick = onDelete) { Text("DELETE", color = MaterialTheme.colorScheme.error) }
                }
                TextButton(onClick = onDismiss) { Text("CANCEL") }
            }
        }
    )
}
