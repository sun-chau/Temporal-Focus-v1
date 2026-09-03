package com.example.ui.screens

import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.StrokeCap
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrackerDetailRouter(
    initialTracker: TrackerEntity,
    viewModel: TrackerViewModel,
    onBack: () -> Unit
) {
    val trackerState by viewModel.getTrackerById(initialTracker.id).collectAsState(initial = initialTracker)
    val tracker = trackerState ?: initialTracker
    val payload = viewModel.getParsedPayload(tracker)

    Scaffold(

        topBar = {
            TopAppBar(
                title = { Text(tracker.title) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .padding(paddingValues)
                .fillMaxSize()
                .padding(16.dp)
        ) {
            when (tracker.type) {
                TrackerType.CUSTOM -> {
                    if (payload is CustomPayload) {
                        CustomTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Custom Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.GYM -> {
                    if (payload is GymPayload) {
                        GymTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Gym Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.SYLLABUS -> {
                    if (payload is SyllabusPayload) {
                        SyllabusTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Syllabus Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                TrackerType.ASSIGNMENT -> {
                    if (payload is AssignmentPayload) {
                        AssignmentTrackerUI(tracker, payload, viewModel)
                    } else {
                        Text("Invalid Assignment Payload", color = MaterialTheme.colorScheme.error)
                    }
                }
                else -> {
                    Text("Payload UI Rendering: COMING SOON", fontFamily = FontFamily.Monospace)
                }
            }
        }
    }
}