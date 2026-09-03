package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun VolumeTrackerUI(
    entity: TrackerEntity,
    payload: VolumePayload,
    viewModel: TrackerViewModel
) {
    var showAddDialog by remember { mutableStateOf(false) }
    var editingResource by remember { mutableStateOf<VolumeResource?>(null) }
    var numpadResource by remember { mutableStateOf<VolumeResource?>(null) }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 80.dp)
        ) {
            items(payload.resources, key = { it.id }) { resource ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .combinedClickable(
                            onClick = { numpadResource = resource },
                            onLongClick = { editingResource = resource }
                        )
                        .padding(16.dp)
                ) {
                    Text(
                        text = resource.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "[ ${resource.currentProgress} / ${resource.totalProgress} ${resource.metricLabel} ]",
                        style = MaterialTheme.typography.bodyMedium,
                        fontFamily = FontFamily.Monospace
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    LinearProgressIndicator(
                        progress = {
                            if (resource.totalProgress > 0) {
                                (resource.currentProgress.toFloat() / resource.totalProgress).coerceIn(0f, 1f)
                            } else 0f
                        },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(12.dp)
                    )
                }
                Divider()
            }
        }

        FloatingActionButton(
            onClick = { showAddDialog = true },
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp)
        ) {
            Icon(Icons.Filled.Add, contentDescription = "Add Resource")
        }
    }

    if (showAddDialog) {
        ResourceEditDialog(
            initialTitle = "",
            initialTotal = "",
            initialMetric = "",
            onDismiss = { showAddDialog = false },
            onSave = { title, total, metric ->
                val newRes = VolumeResource(
                    id = UUID.randomUUID().toString(),
                    title = title,
                    currentProgress = 0,
                    totalProgress = total,
                    metricLabel = metric
                )
                viewModel.updateVolumePayload(entity, payload.copy(resources = payload.resources + newRes))
                showAddDialog = false
            }
        )
    }

    editingResource?.let { res ->
        ResourceEditDialog(
            initialTitle = res.title,
            initialTotal = res.totalProgress.toString(),
            initialMetric = res.metricLabel,
            onDismiss = { editingResource = null },
            onSave = { title, total, metric ->
                val updated = payload.resources.map {
                    if (it.id == res.id) it.copy(title = title, totalProgress = total, metricLabel = metric) else it
                }
                viewModel.updateVolumePayload(entity, payload.copy(resources = updated))
                editingResource = null
            },
            onDelete = {
                val updated = payload.resources.filter { it.id != res.id }
                viewModel.updateVolumePayload(entity, payload.copy(resources = updated))
                editingResource = null
            }
        )
    }

    numpadResource?.let { res ->
        VolumeNumpadSheet(
            resource = res,
            onDismiss = { numpadResource = null },
            onSave = { newProgress ->
                val updated = payload.resources.map {
                    if (it.id == res.id) it.copy(currentProgress = newProgress) else it
                }
                viewModel.updateVolumePayload(entity, payload.copy(resources = updated))
                numpadResource = null
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VolumeNumpadSheet(
    resource: VolumeResource,
    onDismiss: () -> Unit,
    onSave: (Int) -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var inputStr by remember { mutableStateOf("") }
    
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Log Progress for ${resource.title}",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = if (inputStr.isEmpty()) "0" else inputStr,
                style = MaterialTheme.typography.displayMedium,
                fontFamily = FontFamily.Monospace,
                modifier = Modifier.fillMaxWidth(),
                textAlign = TextAlign.Center
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            val keys = listOf("1", "2", "3", "4", "5", "6", "7", "8", "9", "DEL", "0", "LOG")
            LazyVerticalGrid(
                columns = GridCells.Fixed(3),
                modifier = Modifier.fillMaxWidth()
            ) {
                items(keys) { key ->
                    Box(
                        modifier = Modifier
                            .aspectRatio(2f)
                            .padding(4.dp)
                            .background(
                                color = if (key == "LOG") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                shape = MaterialTheme.shapes.medium
                            )
                            .clickable {
                                if (key == "LOG") {
                                    val newVal = inputStr.toIntOrNull() ?: 0
                                    onSave(newVal)
                                } else if (key == "DEL") {
                                    if (inputStr.isNotEmpty()) inputStr = inputStr.dropLast(1)
                                } else {
                                    inputStr += key
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = key,
                            color = if (key == "LOG") MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface,
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
fun ResourceEditDialog(
    initialTitle: String,
    initialTotal: String,
    initialMetric: String,
    onDismiss: () -> Unit,
    onSave: (String, Int, String) -> Unit,
    onDelete: (() -> Unit)? = null
) {
    var title by remember { mutableStateOf(initialTitle) }
    var total by remember { mutableStateOf(initialTotal) }
    var metric by remember { mutableStateOf(initialMetric) }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Resource") },
        text = {
            Column {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Title") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = total,
                    onValueChange = { total = it },
                    label = { Text("Total") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = metric,
                    onValueChange = { metric = it },
                    label = { Text("Metric (e.g. Pages, Modules)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    val t = total.toIntOrNull()
                    if (title.isNotBlank() && t != null && t > 0) {
                        onSave(title, t, metric.ifBlank { "Units" })
                    }
                }
            ) { Text("SAVE") }
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
