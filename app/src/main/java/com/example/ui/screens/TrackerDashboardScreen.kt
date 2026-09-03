package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.border
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.TrackerEntity
import com.example.data.TrackerType
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.TrackerViewModel

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun TrackerDashboardScreen(viewModel: TrackerViewModel, onMenuClick: () -> Unit) {
    val trackers by viewModel.trackers.collectAsStateWithLifecycle()
    var showSheet by remember { mutableStateOf(false) }
    var selectedTracker by remember { mutableStateOf<TrackerEntity?>(null) }
    var trackerToDelete by remember { mutableStateOf<TrackerEntity?>(null) }
    val context = LocalContext.current

    if (selectedTracker != null) {
        TrackerDetailRouter(
            initialTracker = selectedTracker!!,
            viewModel = viewModel,
            onBack = { selectedTracker = null }
        )
    } else {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Trackers & Consistency") },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp)
        ) {
            Button(
                onClick = { showSheet = true },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                shape = RectangleShape
            ) {
                Text("+ NEW TRACKER", fontWeight = FontWeight.Bold)
            }

            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(trackers) { tracker ->
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                            .combinedClickable(
                                onClick = { selectedTracker = tracker },
                                onLongClick = { trackerToDelete = tracker }
                            )
                            .padding(16.dp)
                    ) {
                        Column {
                            Text(
                                text = "[ ${tracker.type.name} ]",
                                fontFamily = FontFamily.Monospace,
                                color = MaterialTheme.colorScheme.primary,
                                style = MaterialTheme.typography.labelMedium
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = tracker.title,
                                fontWeight = FontWeight.Bold,
                                style = MaterialTheme.typography.titleLarge
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = viewModel.getTelemetryString(tracker),
                                fontFamily = FontFamily.Monospace,
                                fontSize = androidx.compose.ui.unit.TextUnit(12f, androidx.compose.ui.unit.TextUnitType.Sp),
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
                item {
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }

    if (showSheet) {
        NewTrackerSheet(
            onDismiss = { showSheet = false },
            onSave = { title, type ->
                viewModel.insertTracker(
                    TrackerEntity(
                        title = title,
                        type = type,
                        payloadData = "{}"
                    )
                )
                showSheet = false
            }
        )
    }
    }

    trackerToDelete?.let { targetTracker ->
        AlertDialog(
            onDismissRequest = { trackerToDelete = null },
            title = { Text("Purge Tracker") },
            text = { 
                Text(
                    "Are you sure you want to permanently delete '[ ${targetTracker.title} ]'? All historical logs and schemas will be destroyed.",
                    color = MaterialTheme.colorScheme.error
                ) 
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteTracker(targetTracker)
                        trackerToDelete = null
                    }
                ) { Text("DELETE", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                TextButton(onClick = { trackerToDelete = null }) { Text("CANCEL") }
            }
        )
    }
}
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NewTrackerSheet(onDismiss: () -> Unit, onSave: (String, TrackerType) -> Unit) {
    var title by remember { mutableStateOf("") }
    var selectedType by remember { mutableStateOf(TrackerType.GYM) }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("Create New Tracker", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)

            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Tracker Title") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            Text("Tracker Type", style = MaterialTheme.typography.titleMedium)
            
            // Horizontal chip row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                TrackerType.values().forEach { type ->
                    FilterChip(
                        selected = selectedType == type,
                        onClick = { selectedType = type },
                        label = { Text(type.name) }
                    )
                }
            }

            Button(
                onClick = {
                    if (title.isNotBlank()) {
                        onSave(title, selectedType)
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                shape = RectangleShape
            ) {
                Text("SAVE TRACKER")
            }
        }
    }
}
