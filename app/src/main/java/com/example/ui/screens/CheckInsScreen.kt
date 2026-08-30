package com.example.ui.screens
import androidx.compose.foundation.border

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.data.TrackerEntity
import com.example.data.TrackerLogEntity
import com.example.data.TrackerType
import com.example.data.TrackerUnit
import com.example.viewmodel.MainViewModel
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CheckInsScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {
    val trackers by viewModel.trackers.collectAsStateWithLifecycle()
    val logs by viewModel.trackerLogs.collectAsStateWithLifecycle()
    
    var showCreateSheet by remember { mutableStateOf(false) }
    var selectedTracker by remember { mutableStateOf<TrackerEntity?>(null) }
    
    val todayStr = remember { SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date()) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Check-Ins & Consistency") },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { showCreateSheet = true }) {
                Icon(Icons.Default.Add, contentDescription = "New Tracker")
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (trackers.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillParentMaxSize(), contentAlignment = Alignment.Center) {
                        Text("No trackers yet. Tap + to create one.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            } else {
                items(trackers, key = { it.id }) { tracker ->
                    val trackerLogs = logs.filter { it.trackerId == tracker.id }
                    val totalLoggedVolume = trackerLogs.sumOf { it.loggedVolume.toDouble() }.toFloat()
                    TrackerCard(
                        tracker = tracker,
                        todayLog = trackerLogs.find { it.dateString == todayStr },
                        totalLoggedVolume = totalLoggedVolume,
                        onClick = { selectedTracker = tracker }
                    )
                }
            }
        }
    }
    
    if (showCreateSheet) {
        ModalBottomSheet(onDismissRequest = { showCreateSheet = false }) {
            CreateTrackerSheet(
                onSave = { entity -> 
                    viewModel.insertTracker(entity)
                    showCreateSheet = false
                },
                onCancel = { showCreateSheet = false }
            )
        }
    }
    
    if (selectedTracker != null) {
        val tracker = selectedTracker!!
        if (tracker.streakAtRisk) {
             AlertDialog(
                 onDismissRequest = { selectedTracker = null },
                 title = { Text("Streak at Risk!") },
                 text = { Text("You missed logging yesterday. Do you want to spend a banked day to save your streak, or accept the break?") },
                 confirmButton = {
                     Button(
                         onClick = {
                             viewModel.spendBankedDay(tracker)
                             selectedTracker = null
                         },
                         enabled = tracker.bankedDays > 0
                     ) { Text("Spend 1 Banked Day (${tracker.bankedDays} left)") }
                 },
                 dismissButton = {
                     TextButton(onClick = {
                         viewModel.acceptBreak(tracker)
                         selectedTracker = null
                     }) { Text("Accept Break") }
                 }
             )
        } else {
            ModalBottomSheet(onDismissRequest = { selectedTracker = null }) {
                LogTrackerSheet(
                    tracker = tracker,
                    todayLog = logs.find { it.trackerId == tracker.id && it.dateString == todayStr },
                    onSave = { volume -> 
                        viewModel.logTrackerVolume(tracker, todayStr, volume)
                        selectedTracker = null
                    },
                    onCancel = { selectedTracker = null }
                )
            }
        }
    }
}

@Composable
fun TrackerCard(tracker: TrackerEntity, todayLog: TrackerLogEntity?, totalLoggedVolume: Float, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()


        .clip(RoundedCornerShape(24.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha=0.05f), RoundedCornerShape(24.dp))
            .clickable(onClick = onClick)
            .padding(24.dp)
    ) {
        Column {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = tracker.title,
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f)
                )
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Security, 
                        contentDescription = "Banked Days",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "x${tracker.bankedDays}",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            if (tracker.type == TrackerType.FINITE && tracker.totalVolume != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Column(modifier = Modifier.fillMaxWidth()) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text("Overall Progress", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Text(
                            "${totalLoggedVolume.toInt()} / ${tracker.totalVolume.toInt()} ${if (tracker.unit == TrackerUnit.CONTINUOUS) "%" else "units"}",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    LinearProgressIndicator(
                        progress = { (totalLoggedVolume / tracker.totalVolume).coerceIn(0f, 1f) },
                        modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp))
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("Streak", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "${tracker.currentStreak} days",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = if (tracker.streakAtRisk) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
                        )
                        if (tracker.streakAtRisk) {
                            Icon(
                                Icons.Default.Warning,
                                contentDescription = "Risk",
                                tint = MaterialTheme.colorScheme.error,
                                modifier = Modifier.padding(start = 4.dp).size(16.dp)
                            )
                        }
                    }
                }
                
                Column(horizontalAlignment = Alignment.End) {
                    Text("Today's Target", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(
                        text = "${tracker.staticDailyTarget} ${if (tracker.unit == TrackerUnit.CONTINUOUS) "%" else "units"}",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            if (todayLog != null) {
                Row(
                    modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.primaryContainer).padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Logged Today", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
                    Text("${todayLog.loggedVolume} ${if (tracker.unit == TrackerUnit.CONTINUOUS) "%" else "units"}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimaryContainer)
                }
            } else {
                Row(
                    modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.surface).padding(12.dp),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Tap to log progress", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateTrackerSheet(onSave: (TrackerEntity) -> Unit, onCancel: () -> Unit) {
    var title by remember { mutableStateOf("") }
    var type by remember { mutableStateOf(TrackerType.ENDLESS) }
    var unit by remember { mutableStateOf(TrackerUnit.DISCRETE) }
    var dailyTarget by remember { mutableStateOf("1") }
    var totalVolumeStr by remember { mutableStateOf("") }
    
    Column(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp).padding(bottom = 32.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("New Tracker", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        
        OutlinedTextField(
            value = title,
            onValueChange = { title = it },
            label = { Text("Title") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Type", style = MaterialTheme.typography.labelMedium)
                SegmentedButtonSingleSelect(
                    options = listOf("Endless", "Finite"),
                    selectedIndex = if (type == TrackerType.ENDLESS) 0 else 1,
                    onSelect = { type = if (it == 0) TrackerType.ENDLESS else TrackerType.FINITE }
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text("Unit", style = MaterialTheme.typography.labelMedium)
                SegmentedButtonSingleSelect(
                    options = listOf("Discrete", "Continuous"),
                    selectedIndex = if (unit == TrackerUnit.DISCRETE) 0 else 1,
                    onSelect = { unit = if (it == 0) TrackerUnit.DISCRETE else TrackerUnit.CONTINUOUS }
                )
            }
        }
        
        OutlinedTextField(
            value = dailyTarget,
            onValueChange = { dailyTarget = it },
            label = { Text(if (unit == TrackerUnit.CONTINUOUS) "Daily Target (%)" else "Daily Target (units)") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )
        
        if (type == TrackerType.FINITE) {
            OutlinedTextField(
                value = totalVolumeStr,
                onValueChange = { totalVolumeStr = it },
                label = { Text("Total Volume (e.g. 30 chapters)") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
            
            var deadlineDaysStr by remember { mutableStateOf("") }
            OutlinedTextField(
                value = deadlineDaysStr,
                onValueChange = { deadlineDaysStr = it },
                label = { Text("Days until deadline (Optional)") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                TextButton(onClick = onCancel) { Text("Cancel") }
                Button(
                    onClick = {
                        val targetVal = dailyTarget.toFloatOrNull() ?: 1f
                        val totalVol = totalVolumeStr.toFloatOrNull()
                        val deadlineDays = deadlineDaysStr.toLongOrNull()
                        val deadlineMillis = if (deadlineDays != null) System.currentTimeMillis() + deadlineDays * 24 * 60 * 60 * 1000 else null
                        onSave(TrackerEntity(
                            title = title,
                            type = type,
                            unit = unit,
                            staticDailyTarget = targetVal,
                            totalVolume = totalVol,
                            deadlineMillis = deadlineMillis
                        ))
                    },
                    enabled = title.isNotBlank()
                ) { Text("Create") }
            }
        } else {
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                TextButton(onClick = onCancel) { Text("Cancel") }
                Button(
                    onClick = {
                        val targetVal = dailyTarget.toFloatOrNull() ?: 1f
                        onSave(TrackerEntity(
                            title = title,
                            type = type,
                            unit = unit,
                            staticDailyTarget = targetVal,
                            totalVolume = null,
                            deadlineMillis = null
                        ))
                    },
                    enabled = title.isNotBlank()
                ) { Text("Create") }
            }
        }
    }
}

@Composable
fun SegmentedButtonSingleSelect(options: List<String>, selectedIndex: Int, onSelect: (Int) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.surfaceVariant)
    ) {
        options.forEachIndexed { index, text ->
            val isSelected = index == selectedIndex
            Box(
                modifier = Modifier
                    .weight(1f)
                    .background(if (isSelected) MaterialTheme.colorScheme.primary else Color.Transparent)
                    .clickable { onSelect(index) }
                    .padding(vertical = 12.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = text,
                    style = MaterialTheme.typography.labelMedium,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LogTrackerSheet(tracker: TrackerEntity, todayLog: TrackerLogEntity?, onSave: (Float) -> Unit, onCancel: () -> Unit) {
    var volume by remember { mutableStateOf(todayLog?.loggedVolume?.toString() ?: "") }
    var continuousVolume by remember { mutableStateOf(todayLog?.loggedVolume ?: 0f) }
    
    Column(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp).padding(bottom = 32.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Log Progress: ${tracker.title}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("Target today: ${tracker.staticDailyTarget} ${if(tracker.unit == TrackerUnit.CONTINUOUS) "%" else "units"}", style = MaterialTheme.typography.bodyMedium)
        
        if (tracker.unit == TrackerUnit.CONTINUOUS) {
            Text("${continuousVolume.toInt()}%", style = MaterialTheme.typography.displayMedium, modifier = Modifier.align(Alignment.CenterHorizontally))
            Slider(
                value = continuousVolume,
                onValueChange = { continuousVolume = it },
                valueRange = 0f..100f,
                modifier = Modifier.fillMaxWidth()
            )
        } else {
            OutlinedTextField(
                value = volume,
                onValueChange = { volume = it },
                label = { Text("Volume Completed") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            TextButton(onClick = onCancel) { Text("Cancel") }
            Button(
                onClick = {
                    val vol = if (tracker.unit == TrackerUnit.CONTINUOUS) continuousVolume else (volume.toFloatOrNull() ?: 0f)
                    onSave(vol)
                }
            ) { Text("Save Log") }
        }
    }
}
