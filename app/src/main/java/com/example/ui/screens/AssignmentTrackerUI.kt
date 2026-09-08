package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.ui.unit.sp
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
                
                val timeDiffMillis = task.deadlineEpoch - System.currentTimeMillis()
                val hoursRemaining = timeDiffMillis / (1000 * 60 * 60)
                val daysRemaining = hoursRemaining / 24
                val countdownStr = if (java.lang.Math.abs(daysRemaining) > 0) "T-${daysRemaining} DAYS" else "T-${hoursRemaining} HOURS"
                val format = java.text.SimpleDateFormat("dd MMM HH:mm", java.util.Locale.getDefault())
                val absoluteTime = format.format(java.util.Date(task.deadlineEpoch)).uppercase()
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                        .combinedClickable(
                            onClick = {
                                viewModel.cycleAssignmentStatus(entity, task.id)
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
                            text = "[ $absoluteTime | $countdownStr ]",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            color = if (timeDiffMillis < 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
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
        val hours = remember { (0..23).map { it.toString().padStart(2, '0') } }
        val minutes = remember { (0..55 step 5).map { it.toString().padStart(2, '0') } }
        val days = remember { (1..31).map { it.toString().padStart(2, '0') } }
        val months = remember { (1..12).map { it.toString().padStart(2, '0') } }
        val years = remember { (2026..2030).map { it.toString() } }
        var selDay by remember { mutableStateOf(days[0]) }
        var selMonth by remember { mutableStateOf(months[0]) }
        var selYear by remember { mutableStateOf(years[0]) }
        var selHour by remember { mutableStateOf(hours[0]) }
        var selMinute by remember { mutableStateOf(minutes[0]) }
        var selectedPrio by remember { mutableStateOf(PriorityLevel.MID) }
        var selectedRecur by remember { mutableStateOf(Recurrence.NONE) }
        
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
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                     TerminalWheelPicker(items = days, onItemSelected = { selDay = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = months, onItemSelected = { selMonth = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = years, onItemSelected = { selYear = it }, modifier = Modifier.weight(1f))
                }
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                     TerminalWheelPicker(items = hours, onItemSelected = { selHour = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = minutes, onItemSelected = { selMinute = it }, modifier = Modifier.weight(1f))
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    PriorityLevel.values().forEach { p ->
                        FilterChip(selected = selectedPrio == p, onClick = { selectedPrio = p }, label = { Text("[ $p ]") })
                    }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Recurrence.values().forEach { r ->
                        FilterChip(selected = selectedRecur == r, onClick = { selectedRecur = r }, label = { Text(if(r == Recurrence.NONE) "[ ONE-OFF ]" else "[ WEEKLY ]") })
                    }
                }
                val hasChanges = deliverableTitle.isNotBlank()
                Button(
                    onClick = {
                        if (deliverableTitle.isNotBlank()) {
                            val format = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm", java.util.Locale.getDefault())
                            val parsedEpoch = try {
                                format.parse("$selYear-$selMonth-$selDay $selHour:$selMinute")?.time ?: System.currentTimeMillis()
                            } catch (e: Exception) {
                                System.currentTimeMillis()
                            }
                            val newTask = Deliverable(
                                title = deliverableTitle, 
                                deadlineEpoch = parsedEpoch, 
                                priority = selectedPrio, 
                                recurrence = selectedRecur
                            )
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

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun TerminalWheelPicker(
    items: List<String>,
    onItemSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()
    val flingBehavior = rememberSnapFlingBehavior(lazyListState = listState)
    
    val selectedIndex by remember {
        derivedStateOf {
            val layoutInfo = listState.layoutInfo
            val visibleItemsInfo = layoutInfo.visibleItemsInfo
            if (visibleItemsInfo.isEmpty()) return@derivedStateOf -1
            
            val viewportCenter = layoutInfo.viewportEndOffset / 2
            val closest = visibleItemsInfo.minByOrNull { Math.abs((it.offset + it.size / 2) - viewportCenter) }
            closest?.index ?: -1
        }
    }
    
    LaunchedEffect(selectedIndex) {
        if (selectedIndex in items.indices) {
            onItemSelected(items[selectedIndex])
        }
    }

    Box(
        modifier = modifier
            .height(120.dp)
            .fillMaxWidth(),
        contentAlignment = Alignment.Center
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Spacer(modifier = Modifier.weight(1f))
            Box(modifier = Modifier.fillMaxWidth().height(40.dp).border(width = 1.dp, color = MaterialTheme.colorScheme.primary, shape = RectangleShape))
            Spacer(modifier = Modifier.weight(1f))
        }
        
        LazyColumn(
            state = listState,
            flingBehavior = flingBehavior,
            contentPadding = PaddingValues(vertical = 40.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            itemsIndexed(items) { index, item ->
                val isSelected = index == selectedIndex
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(40.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = item,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontFamily = FontFamily.Monospace,
                        fontSize = if (isSelected) 24.sp else 18.sp
                    )
                }
            }
        }
    }
}
