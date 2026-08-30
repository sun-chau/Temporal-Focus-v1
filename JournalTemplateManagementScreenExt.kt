package com.example.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.JournalTemplate
import com.example.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JournalTemplateManagementScreen(
    viewModel: MainViewModel,
    onClose: () -> Unit
) {
    val templates by viewModel.journalTemplates.collectAsStateWithLifecycle(initialValue = emptyList())
    var creatingTemplate by remember { mutableStateOf(false) }

    if (creatingTemplate) {
        var title by remember { mutableStateOf("") }
        var content by remember { mutableStateOf("") }

        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("New Template") },
                    navigationIcon = {
                        IconButton(onClick = { creatingTemplate = false }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    },
                    actions = {
                        TextButton(onClick = {
                            if (title.isNotBlank()) {
                                viewModel.insertJournalTemplate(JournalTemplate(title = title, content = content))
                                creatingTemplate = false
                            }
                        }) {
                            Text("Save")
                        }
                    }
                )
            }
        ) { paddingValues ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Template Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = content,
                    onValueChange = { content = it },
                    label = { Text("Template Content") },
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    } else {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Manage Templates") },
                    navigationIcon = {
                        IconButton(onClick = onClose) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                )
            },
            floatingActionButton = {
                FloatingActionButton(onClick = { creatingTemplate = true }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {
                    Icon(Icons.Default.Add, contentDescription = "New Template")
                }
            }
        ) { paddingValues ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentPadding = PaddingValues(16.dp)
            ) {
                items(templates, key = { it.templateId }) { template ->
                    ListItem(
                        headlineContent = { Text(template.title) },
                        supportingContent = { Text(template.content, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis) },
                        trailingContent = {
                            IconButton(onClick = { viewModel.deleteJournalTemplate(template) }) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete Template")
                            }
                        }
                    )
                }
            }
        }
    }
}
