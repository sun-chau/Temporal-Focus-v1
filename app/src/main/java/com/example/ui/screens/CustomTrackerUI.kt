package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.viewmodel.TrackerViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CustomTrackerUI(entity: TrackerEntity, payload: CustomPayload, viewModel: TrackerViewModel) {
    if (payload.schema.isEmpty()) {
        CustomSchemaBuilderUI(entity, payload, viewModel)
    } else {
        CustomLoggerUI(entity, payload, viewModel)
    }
}

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CustomSchemaBuilderUI(entity: TrackerEntity, payload: CustomPayload, viewModel: TrackerViewModel) {
    var pendingSchema by remember { mutableStateOf(listOf<CustomField>()) }
    var showAddField by remember { mutableStateOf(false) }

    Column(modifier = Modifier.fillMaxSize()) {
        Text("Define Tracker Variables", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(16.dp))
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(pendingSchema) { field ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(field.label, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                    Text("[ ${field.fieldType.name} ]", fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.primary)
                }
            }
        }
        if (pendingSchema.isNotEmpty()) {
            Button(
                onClick = {
                    viewModel.updateCustomPayload(entity, payload.copy(schema = pendingSchema))
                },
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                shape = RectangleShape
            ) {
                Text("LOCK SCHEMA")
            }
        }
        OutlinedButton(
            onClick = { showAddField = true },
            modifier = Modifier.fillMaxWidth(),
            shape = RectangleShape
        ) {
            Text("+ ADD FIELD")
        }
    }

    if (showAddField) {
        var label by remember { mutableStateOf("") }
        var type by remember { mutableStateOf(CustomFieldType.NUMBER) }

        ModalBottomSheet(onDismissRequest = { showAddField = false }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("New Field", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = label,
                    onValueChange = { label = it },
                    label = { Text("Field Label") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                Row(
                    modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    CustomFieldType.values().forEach { t ->
                        FilterChip(
                            selected = type == t,
                            onClick = { type = t },
                            label = { Text(t.name) }
                        )
                    }
                }
                Button(
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
                }
            }
        }
    }
}

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CustomLoggerUI(entity: TrackerEntity, payload: CustomPayload, viewModel: TrackerViewModel) {
    var inputValues by remember { mutableStateOf(mapOf<String, String>()) }
    var editingEntry by remember { mutableStateOf<CustomEntry?>(null) }
    
    val dateFormatter = remember { SimpleDateFormat("dd-MMM-yy | HH:mm", Locale.getDefault()) }

    Column(modifier = Modifier.fillMaxSize()) {
        // Entry Form
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .border(2.dp, MaterialTheme.colorScheme.primary, RectangleShape)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("Log Entry", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
            
            payload.schema.forEach { field ->
                val currentValue = inputValues[field.id] ?: ""
                when (field.fieldType) {
                    CustomFieldType.NUMBER -> {
                        OutlinedTextField(
                            value = currentValue,
                            onValueChange = { inputValues = inputValues + (field.id to it) },
                            label = { Text(field.label) },
                            modifier = Modifier.fillMaxWidth(),
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true
                        )
                    }
                    CustomFieldType.TEXT -> {
                        OutlinedTextField(
                            value = currentValue,
                            onValueChange = { inputValues = inputValues + (field.id to it) },
                            label = { Text(field.label) },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                    }
                    CustomFieldType.CHECKBOX -> {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(
                                checked = currentValue == "true",
                                onCheckedChange = { inputValues = inputValues + (field.id to it.toString()) }
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(field.label)
                        }
                    }
                }
            }
            Button(
                onClick = {
                    viewModel.addCustomEntry(entity, inputValues)
                    inputValues = mapOf()
                },
                modifier = Modifier.fillMaxWidth(),
                shape = RectangleShape
            ) {
                Text("SAVE ENTRY")
            }
        }
        
        Spacer(Modifier.height(16.dp))
        Text("History", fontWeight = FontWeight.Bold, style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.height(8.dp))
        
        // History List
        val sortedEntries = payload.entries.sortedByDescending { it.timestampEpoch }
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(sortedEntries) { entry ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .combinedClickable(
                            onClick = {},
                            onLongClick = { editingEntry = entry }
                        )
                        .padding(16.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "[ ${dateFormatter.format(Date(entry.timestampEpoch)).uppercase(Locale.getDefault())} ]",
                            fontFamily = FontFamily.Monospace,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 12.sp,
                            modifier = Modifier.weight(1f)
                        )
                    }
                    Spacer(Modifier.height(8.dp))
                    
                    payload.schema.forEach { field ->
                        val value = entry.fieldData[field.id] ?: "N/A"
                        val displayValue = if (field.fieldType == CustomFieldType.CHECKBOX) {
                            if (value == "true") "YES" else "NO"
                        } else {
                            value
                        }
                        
                        Row(modifier = Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                            Text(
                                "> ${field.label.uppercase(Locale.getDefault()).padEnd(15, ' ')} : ",
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Bold,
                                fontSize = 12.sp
                            )
                            Text(
                                displayValue.uppercase(Locale.getDefault()), 
                                fontFamily = FontFamily.Monospace,
                                fontSize = 12.sp
                            )
                        }
                    }
                }
            }
        }
    }

    editingEntry?.let { entry ->
        var editValues by remember { mutableStateOf(entry.fieldData) }
        ModalBottomSheet(onDismissRequest = { editingEntry = null }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Edit Entry", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                
                payload.schema.forEach { field ->
                    val currentValue = editValues[field.id] ?: ""
                    when (field.fieldType) {
                        CustomFieldType.NUMBER -> {
                            OutlinedTextField(
                                value = currentValue,
                                onValueChange = { editValues = editValues + (field.id to it) },
                                label = { Text(field.label) },
                                modifier = Modifier.fillMaxWidth(),
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                singleLine = true
                            )
                        }
                        CustomFieldType.TEXT -> {
                            OutlinedTextField(
                                value = currentValue,
                                onValueChange = { editValues = editValues + (field.id to it) },
                                label = { Text(field.label) },
                                modifier = Modifier.fillMaxWidth(),
                                singleLine = true
                            )
                        }
                        CustomFieldType.CHECKBOX -> {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Checkbox(
                                    checked = currentValue == "true",
                                    onCheckedChange = { editValues = editValues + (field.id to it.toString()) }
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(field.label)
                            }
                        }
                    }
                }
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
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
                }
            }
        }
    }
}
