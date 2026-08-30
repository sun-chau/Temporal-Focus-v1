package com.example.ui.screens
import androidx.compose.material.icons.filled.AttachFile
import androidx.compose.material.icons.filled.Add

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.lazy.LazyRow

import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FilterList
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.outlined.*
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.outlined.MoreVert

import androidx.compose.material.icons.filled.ChevronLeft
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.KeyboardArrowLeft
import androidx.compose.material.icons.filled.KeyboardArrowRight

import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.PushPin
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.material.icons.outlined.Info
import androidx.compose.material.icons.outlined.Alarm
import androidx.compose.material.icons.filled.ViewAgenda
import androidx.compose.material.icons.filled.ViewCarousel
import androidx.compose.material.icons.filled.TouchApp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.launch

import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.content.Context
import android.content.ContextWrapper
import android.app.Activity
import java.util.Calendar
import com.example.data.TimerTask
import com.example.ui.components.StatCard
import com.example.viewmodel.ChronometerLayout
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import com.example.ui.utils.getLabelColor
import com.example.ui.utils.getLabelName
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.TimeUnit

@Composable
fun ChronometerScreen(viewModel: MainViewModel, uiState: UiState, onMenuClick: () -> Unit) {
    val allActiveTasks by viewModel.activeTasks.collectAsState()
    val activeTasks = allActiveTasks.filter { it.labels != "Reminder" }
    val completedTasks by viewModel.completedTasks.collectAsState()
    
    var showStats by remember { mutableStateOf(false) }
    var showCreateOverlay by remember { mutableStateOf(false) }
    var isPeeking by remember { mutableStateOf(false) }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp)
        ) {
            
            // Top Menu Row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .windowInsetsPadding(WindowInsets.safeDrawing.only(WindowInsetsSides.Top))
                    .padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.Start,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onMenuClick, modifier = Modifier.offset(x = (-12).dp)) {
                    Icon(
                        imageVector = Icons.Default.Menu,
                        contentDescription = "Menu",
                        modifier = Modifier.size(28.dp),
                        tint = MaterialTheme.colorScheme.onSurface
                    )
                }
            }

            
            // Header Row
            Column(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    var showStageFilterDialog by remember { mutableStateOf(false) }
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .clickable { showStageFilterDialog = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.FilterList, contentDescription = "Filter Stage", tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(20.dp))
                    }
                    
                    if (showStageFilterDialog) {
                        StageFilterDialog(
                            uiState = uiState,
                            activeTasks = activeTasks,
                            onDismiss = { showStageFilterDialog = false },
                            viewModel = viewModel
                        )
                    }

                    val isVertical = uiState.layoutPreference == ChronometerLayout.VERTICAL
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .clickable {
                                if (isVertical) {
                                    viewModel.setLayoutPreference(ChronometerLayout.HORIZONTAL)
                                } else {
                                    viewModel.setLayoutPreference(ChronometerLayout.VERTICAL)
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            if (isVertical) Icons.Default.ViewCarousel else Icons.Default.ViewAgenda,
                            contentDescription = "Toggle Layout",
                            tint = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.size(20.dp)
                        )
                    }

                    Box(
                        modifier = Modifier
                            .size(46.dp)
                            .border(1.dp, MaterialTheme.colorScheme.primary, CircleShape)
                            .padding(3.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.primary)
                                .clickable { viewModel.setCreatingChronometer(true) },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Add, contentDescription = "Create", tint = MaterialTheme.colorScheme.background, modifier = Modifier.size(40.dp))
                        }
                    }

                    Box(
                        modifier = Modifier
                            .height(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .padding(horizontal = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        val activeSlots = if (uiState.isUrgentMode) {
                            activeTasks.sortedBy { it.targetDateTime }.let { if (uiState.maxStageSlots == -1) it else it.take(uiState.maxStageSlots) }.size
                        } else {
                            activeTasks.count { uiState.selectedDisplayIds.contains(it.id) }
                        }
                        Text("$activeSlots/${activeTasks.size}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }

                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                            .pointerInput(Unit) {
                                detectTapGestures(
                                    onPress = {
                                        isPeeking = true
                                        showStats = true
                                        tryAwaitRelease()
                                        if (isPeeking) {
                                            isPeeking = false
                                            showStats = false
                                        }
                                    },
                                    onTap = {
                                        isPeeking = false
                                        showStats = !showStats
                                    }
                                )
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.TouchApp,
                            contentDescription = "Stats",
                            tint = MaterialTheme.colorScheme.secondary,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }
                
            Spacer(modifier = Modifier.height(16.dp))

            // Task List
            val displayTasks = if (uiState.isUrgentMode) {
                activeTasks.sortedBy { it.targetDateTime }.let { if (uiState.maxStageSlots == -1) it else it.take(uiState.maxStageSlots) }
            } else {
                activeTasks.filter { uiState.selectedDisplayIds.contains(it.id) }
            }
            
            if (displayTasks.isEmpty()) {
                Box(
                    modifier = Modifier.weight(1f).fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha=0.05f), RoundedCornerShape(24.dp))
                            .padding(vertical = 48.dp, horizontal = 24.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.PushPin,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(48.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            if (activeTasks.isEmpty()) "No active deadlines ticking" else "No deadlines on stage",
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            fontSize = 18.sp
                        )
                        Spacer(Modifier.height(8.dp))
                        Text(
                            if (activeTasks.isEmpty()) "Generate a target deadline timer to start mapping your urgency\nmilestones on the stage." else "You have active timers, but none are pinned to the stage.\nManage timers to pin them or switch to urgent mode.",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 14.sp,
                            textAlign = TextAlign.Center
                        )
                        Spacer(Modifier.height(24.dp))
                        Button(
                            onClick = { viewModel.setCreatingChronometer(true) },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant,
                                contentColor = MaterialTheme.colorScheme.primary
                            )
                        ) {
                            Text("+ Create First Timer", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            } else {
                if (uiState.layoutPreference == ChronometerLayout.VERTICAL) {
                    val listState = rememberLazyListState()
                    val firstVisibleIndex by remember { derivedStateOf { listState.firstVisibleItemIndex } }
                    Row(modifier = Modifier.weight(1f)) {
                        LazyColumn(state = listState, modifier = Modifier.weight(1f)) {
                            items(displayTasks) { task ->
                                ChronometerItem(task, uiState.currentDateTime, viewModel)
                                Spacer(modifier = Modifier.height(16.dp))
                            }
                            
                            item {
                                Spacer(modifier = Modifier.height(64.dp)) // padding for fab
                            }
                        }
                        
                        if (displayTasks.size > 1) {
                            Spacer(modifier = Modifier.width(8.dp))
                            Column(
                                modifier = Modifier.fillMaxHeight().padding(bottom = 64.dp),
                                verticalArrangement = Arrangement.Center,
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                if (displayTasks.size >= 50) {
                                    val progress = if (displayTasks.isEmpty()) 0f else firstVisibleIndex.toFloat() / displayTasks.size
                                    Box(modifier = Modifier.width(4.dp).height(200.dp).background(MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f), RoundedCornerShape(2.dp))) {
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .height((200f * (1f / displayTasks.size)).coerceAtLeast(10f).dp)
                                                .offset(y = (progress * 200).dp)
                                                .background(MaterialTheme.colorScheme.primary, RoundedCornerShape(2.dp))
                                        )
                                    }
                                } else {
                                    displayTasks.forEachIndexed { index, _ ->
                                        val isSelected = index == firstVisibleIndex
                                        val animatedHeight by androidx.compose.animation.core.animateDpAsState(targetValue = if (isSelected) 24.dp else 8.dp, label = "height")
                                        val animatedColor by androidx.compose.animation.animateColorAsState(targetValue = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f), label = "color")
                                        Box(
                                            modifier = Modifier
                                                .padding(vertical = 4.dp)
                                                .width(6.dp)
                                                .height(animatedHeight)
                                                .clip(RoundedCornerShape(3.dp))
                                                .background(animatedColor)
                                        )
                                    }
                                }
                            }
                        }
                    }
                } else {
                    val pagerState = rememberPagerState(pageCount = { displayTasks.size })
                    val coroutineScope = rememberCoroutineScope()
                    
                    Column(modifier = Modifier.weight(1f)) {
                        HorizontalPager(
                            state = pagerState,
                            modifier = Modifier.fillMaxWidth()
                        ) { page ->
                            val task = displayTasks[page]
                            ChronometerItem(
                                task = task, 
                                currentTime = uiState.currentDateTime, 
                                viewModel = viewModel,
                                showNavChevrons = true,
                                onPrevClick = if (page > 0) { { coroutineScope.launch { pagerState.animateScrollToPage(page - 1) } } } else null,
                                onNextClick = if (page < displayTasks.size - 1) { { coroutineScope.launch { pagerState.animateScrollToPage(page + 1) } } } else null
                            )
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        // Pagination Indicators
                        Row(
                            Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.Center
                        ) {
                            repeat(displayTasks.size) { iteration ->
                                val color = if (pagerState.currentPage == iteration) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)
                                val width = if (pagerState.currentPage == iteration) 24.dp else 8.dp
                                Box(
                                    modifier = Modifier
                                        .padding(4.dp)
                                        .clip(RoundedCornerShape(50))
                                        .background(color)
                                        .height(8.dp)
                                        .width(width)
                                )
                            }
                        }
                        
                        LazyColumn(modifier = Modifier.fillMaxWidth()) {
                            item {
                                Spacer(modifier = Modifier.height(64.dp)) // padding for fab
                            }
                        }
                    }
                }
            }
        }
        
        // Info FAB
        if (showStats) {
            ChronometerStatsOverlay(uiState, activeTasks, onDismiss = { showStats = false }, isPeeking = isPeeking)
        }
        
        if (showCreateOverlay) {
            CreateChronometerOverlay(
                use24HourFormat = uiState.use24HourFormat,
                onDismiss = { showCreateOverlay = false },
                onCreate = { name, targetTime, createdAt, recurring, priority, deadline ->
                    viewModel.addTimerTask(
                        name = name, 
                        targetDate = targetTime, 
                        createdAt = createdAt, 
                        recurrenceType = recurring ?: "NONE",
                        priority = priority,
                        deadlineDateTime = deadline
                    )
                    showCreateOverlay = false
                }
            )
        }
    }
}

@Composable
fun ChronometerItem(
    task: TimerTask, 
    currentTime: Long, 
    viewModel: MainViewModel,
    showNavChevrons: Boolean = false,
    onPrevClick: (() -> Unit)? = null,
    onNextClick: (() -> Unit)? = null
) {
    val diff = task.targetDateTime - currentTime
    val isOverdue = diff < 0
    val absDiff = Math.abs(diff)
    
    val years = absDiff / 31536000000L
    val remainingAfterYears = absDiff % 31536000000L
    val months = remainingAfterYears / 2592000000L
    val remainingAfterMonths = remainingAfterYears % 2592000000L
    
    val days = TimeUnit.MILLISECONDS.toDays(remainingAfterMonths)
    val hours = TimeUnit.MILLISECONDS.toHours(remainingAfterMonths) % 24
    val minutes = TimeUnit.MILLISECONDS.toMinutes(remainingAfterMonths) % 60
    val seconds = TimeUnit.MILLISECONDS.toSeconds(remainingAfterMonths) % 60

    var showDescriptionDialog by remember { mutableStateOf(false) }
    var showCompletionDialog by remember { mutableStateOf(false) }
    var showShiftDialog by remember { mutableStateOf(false) }
    
    if (showDescriptionDialog) {
        AlertDialog(
            onDismissRequest = { showDescriptionDialog = false },
            title = { Text("Task Description") },
            text = {
                Column {
                    if (!task.description.isNullOrBlank()) {
                        Text(task.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(16.dp))
                    } else {
                        Text("No description provided.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(16.dp))
                    }
                    
                    if (!task.link.isNullOrEmpty() || !task.attachmentUri.isNullOrEmpty()) {
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            if (!task.link.isNullOrEmpty()) {
                                val uriHandler = androidx.compose.ui.platform.LocalUriHandler.current
                                Row(
                                    modifier = Modifier
                                        .clip(androidx.compose.foundation.shape.RoundedCornerShape(8.dp))
                                        .background(androidx.compose.material3.MaterialTheme.colorScheme.primaryContainer)
                                        .clickable { 
                                            try { uriHandler.openUri(task.link) } catch (e:Exception) {} 
                                        }
                                        .padding(8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(androidx.compose.material.icons.Icons.Default.Add, contentDescription = null, tint = androidx.compose.material3.MaterialTheme.colorScheme.onPrimaryContainer, modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(4.dp))
                                    Text("Link", color = androidx.compose.material3.MaterialTheme.colorScheme.onPrimaryContainer, fontSize = 12.sp, textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline)
                                }
                            }
                            if (!task.attachmentUri.isNullOrEmpty()) {
                                val context = androidx.compose.ui.platform.LocalContext.current
                                Row(
                                    modifier = Modifier
                                        .clip(androidx.compose.foundation.shape.RoundedCornerShape(8.dp))
                                        .background(androidx.compose.material3.MaterialTheme.colorScheme.tertiaryContainer)
                                        .clickable { 
                                            try {
                                                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW)
                                                intent.setData(android.net.Uri.parse(task.attachmentUri))
                                                intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                                context.startActivity(intent)
                                            } catch (e: Exception) {
                                                android.widget.Toast.makeText(context, "Cannot open file", android.widget.Toast.LENGTH_SHORT).show()
                                            }
                                        }
                                        .padding(8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(androidx.compose.material.icons.Icons.Default.AttachFile, contentDescription = null, tint = androidx.compose.material3.MaterialTheme.colorScheme.onTertiaryContainer, modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(4.dp))
                                    Text("File", color = androidx.compose.material3.MaterialTheme.colorScheme.onTertiaryContainer, fontSize = 12.sp)
                                }
                            }
                        }
                        Spacer(Modifier.height(16.dp))
                    }
                    
                    androidx.compose.material3.Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = androidx.compose.material3.CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text("More Information", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Start Date: ${SimpleDateFormat(if (viewModel.uiState.value.use24HourFormat) "MMM dd, yyyy HH:mm" else "MMM dd, yyyy hh:mm a", Locale.getDefault()).format(Date(task.createdAt))}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            Text("Target Date: ${SimpleDateFormat(if (viewModel.uiState.value.use24HourFormat) "MMM dd, yyyy HH:mm" else "MMM dd, yyyy hh:mm a", Locale.getDefault()).format(Date(task.targetDateTime))}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            
                            if (task.shiftedAmount > 0) {
                                val shiftMillis = task.shiftedAmount
                                val shiftHours = (shiftMillis / (1000 * 60 * 60))
                                val shiftMins = (shiftMillis / (1000 * 60)) % 60
                                val shiftStr = if (shiftHours > 0) "+${shiftHours}h ${shiftMins}m" else "+${shiftMins}m"
                                Text("Shifted: $shiftStr", color = MaterialTheme.colorScheme.primary, fontSize = 14.sp)
                            }
                            
                            val recurrenceRule = if (task.recurrenceType != com.example.data.RecurrenceType.NONE.name) {
                                "${task.recurrenceType}" + if (task.recurrenceType == com.example.data.RecurrenceType.CUSTOM.name && task.customDaysInterval != null) " (Every ${task.customDaysInterval} days)" else ""
                            } else "None"
                            Text("Recurrence Rule: $recurrenceRule", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            
                            val statusText = if (task.maxRepetitions != null && task.maxRepetitions > 0) {
                                "Completed: ${task.completionCount}/${task.maxRepetitions}"
                            } else if (task.recurrenceType != com.example.data.RecurrenceType.NONE.name) {
                                "Completed: ${task.completionCount}/∞"
                            } else {
                                "Completed: ${if (task.isCompleted) "1/1" else "0/1"}"
                            }
                            Text("Status: $statusText", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                            Text("ID: ${task.id}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showDescriptionDialog = false }) {
                    Text("Close")
                }
            },
            containerColor = MaterialTheme.colorScheme.surfaceVariant,
            titleContentColor = MaterialTheme.colorScheme.onSurface,
            textContentColor = MaterialTheme.colorScheme.onSurface
        )
    }

    val timeString = buildString {
        if (isOverdue) append("-")
        if (years > 0) append("${years}y ")
        if (months > 0) append("${months}m ")
        if (days > 0) append("${days}d ")
        append(String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds))
    }
    
    val textSize = when {
        timeString.length > 16 -> 32.sp
        timeString.length > 12 -> 38.sp
        else -> 48.sp
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha=0.05f), RoundedCornerShape(24.dp))
            .padding(24.dp)
    ) {
        Column {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(task.name, fontSize = 22.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                    Spacer(Modifier.width(8.dp))
                    val priorityColor = when (task.priority) {
                        "High" -> Color(0xFFE57373)
                        "Low" -> Color(0xFF81C784)
                        else -> MaterialTheme.colorScheme.onSurfaceVariant
                    }
                    Surface(
                        shape = RoundedCornerShape(4.dp),
                        color = priorityColor.copy(alpha = 0.2f),
                        border = androidx.compose.foundation.BorderStroke(1.dp, priorityColor),
                        modifier = Modifier.padding(top = 4.dp)
                    ) {
                        Text(task.priority, color = priorityColor, fontSize = 10.sp, modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp))
                    }
                }
                CircularMenu(
                    isOverdue = isOverdue,
                    onComplete = { 
                        if (isOverdue) {
                            showCompletionDialog = true
                        } else {
                            viewModel.markTaskComplete(task, "ON_TIME")
                        }
                    },
                    onEdit = { 
                        viewModel.setEditingTask(task)
                        viewModel.setCreatingChronometer(true)
                    },
                    onInfo = { showDescriptionDialog = true },
                    onDelete = { viewModel.deleteTask(task) },
                    onShift = { showShiftDialog = true }
                )
            }
            Spacer(Modifier.height(2.dp))
            val format = SimpleDateFormat(if (viewModel.uiState.value.use24HourFormat) "MMM dd, HH:mm:ss" else "MMM dd, hh:mm:ss a", Locale.getDefault())
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Outlined.AccessTime, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(14.dp))
                Spacer(Modifier.width(4.dp))
                Text("Target: ${format.format(Date(task.targetDateTime))}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                if (showNavChevrons) {
                    IconButton(
                        onClick = { onPrevClick?.invoke() },
                        enabled = onPrevClick != null,
                        modifier = Modifier.size(36.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Icon(Icons.Default.KeyboardArrowLeft, contentDescription = "Previous", tint = if (onPrevClick != null) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                    }
                }
                
                AutoResizedText(
                    text = timeString,
                    fontWeight = FontWeight.Bold,
                    fontFamily = FontFamily.Monospace,
                    maxLines = 1,
                    textAlign = TextAlign.Center,
                    color = if (isOverdue) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.weight(1f)
                )
                
                if (showNavChevrons) {
                    IconButton(
                        onClick = { onNextClick?.invoke() },
                        enabled = onNextClick != null,
                        modifier = Modifier.size(36.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Icon(Icons.Default.KeyboardArrowRight, contentDescription = "Next", tint = if (onNextClick != null) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f))
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                val tagsList = task.labels.split(",").filter { it.isNotBlank() }
                if (tagsList.isNotEmpty()) {
                    LazyRow(
                        modifier = Modifier.weight(1f).padding(end = 16.dp),
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        items(tagsList) { tag ->
                            val tagColor = getLabelColor(tag, viewModel.uiState.value.coloredLabelsEnabled)
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(4.dp))
                                    .background(if (tagColor != Color.Transparent) tagColor.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceVariant)
                                    .border(1.dp, if (tagColor != Color.Transparent) tagColor.copy(alpha = 0.5f) else Color.Transparent, RoundedCornerShape(4.dp))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(getLabelName(tag), color = if (tagColor != Color.Transparent) tagColor else MaterialTheme.colorScheme.onSurface, fontSize = 10.sp)
                            }
                        }
                    }
                } else {
                    Spacer(modifier = Modifier.weight(1f))
                }
                
                val totalDuration = task.targetDateTime - task.createdAt
                val elapsed = currentTime - task.createdAt
                val percent = if (totalDuration > 0) ((elapsed.toFloat() / totalDuration) * 100).toInt().coerceIn(0, 100) else 100
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (task.shiftedAmount > 0) {
                        val shiftMillis = task.shiftedAmount
                        val shiftHours = (shiftMillis / (1000 * 60 * 60))
                        val shiftMins = (shiftMillis / (1000 * 60)) % 60
                        val shiftStr = if (shiftHours > 0) "+${shiftHours}h ${shiftMins}m" else "+${shiftMins}m"
                        Text(shiftStr, color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.width(8.dp))
                    }
                    Text("${if(isOverdue) 100 else percent}% Elapsed", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            LinearProgressIndicator(
                progress = { if (isOverdue) 1f else ((currentTime - task.createdAt).toFloat() / (task.targetDateTime - task.createdAt)).coerceIn(0f, 1f) },
                modifier = Modifier.fillMaxWidth().height(4.dp).clip(RoundedCornerShape(2.dp)),
                color = if (isOverdue) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary,
                trackColor = MaterialTheme.colorScheme.surfaceVariant,
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("ID: ${task.id.toString().take(6)}...", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                Text("In Progress", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
    
    if (showShiftDialog) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background.copy(alpha = 0.8f))
                .clickable { showShiftDialog = false }
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant) // Dark grey
                    .clickable { /* prevent dismiss */ }
                    .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f), RoundedCornerShape(24.dp))
            ) {
                // Header
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Shift Due Date", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    IconButton(onClick = { showShiftDialog = false }, modifier = Modifier.size(24.dp)) {
                        Icon(Icons.Default.Clear, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                
                HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                
                @OptIn(ExperimentalLayoutApi::class)
                FlowRow(
                    modifier = Modifier.fillMaxWidth().padding(20.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    val shiftOptions = listOf(
                        "+15m" to 15 * 60 * 1000L,
                        "+30m" to 30 * 60 * 1000L,
                        "+1h" to 60 * 60 * 1000L,
                        "+5h" to 5 * 60 * 60 * 1000L,
                        "+10h" to 10 * 60 * 60 * 1000L,
                        "+12h" to 12 * 60 * 60 * 1000L,
                        "+1d" to 24 * 60 * 60 * 1000L,
                        "+2d" to 2 * 24 * 60 * 60 * 1000L,
                        "+3d" to 3 * 24 * 60 * 60 * 1000L,
                        "+5d" to 5 * 24 * 60 * 60 * 1000L,
                        "+1w" to 7 * 24 * 60 * 60 * 1000L,
                        "+2w" to 14 * 24 * 60 * 60 * 1000L,
                        "+3w" to 21 * 24 * 60 * 60 * 1000L,
                        "+1M" to 30 * 24 * 60 * 60 * 1000L,
                        "+3M" to 90 * 24 * 60 * 60 * 1000L,
                        "+6M" to 180 * 24 * 60 * 60 * 1000L,
                        "+9M" to 270 * 24 * 60 * 60 * 1000L,
                        "+1Y" to 365 * 24 * 60 * 60 * 1000L
                    )
                    shiftOptions.forEach { (label, duration) ->
                        Surface(
                            onClick = {
                                val shiftedAmount = duration
                                val newTargetTime = task.targetDateTime + shiftedAmount
                                val updatedTask = task.copy(
                                    targetDateTime = newTargetTime,
                                    shiftedAmount = task.shiftedAmount + shiftedAmount
                                )
                                viewModel.updateTask(updatedTask)
                                showShiftDialog = false
                            },
                            shape = RoundedCornerShape(16.dp),
                            color = MaterialTheme.colorScheme.surfaceVariant,
                            modifier = Modifier.height(32.dp)
                        ) {
                            Box(modifier = Modifier.padding(horizontal = 12.dp), contentAlignment = Alignment.Center) {
                                Text(label, style = MaterialTheme.typography.labelMedium)
                            }
                        }
                    }
                }
            }
        }
    }

    if (showCompletionDialog) {
        AlertDialog(
            onDismissRequest = { showCompletionDialog = false },
            title = { Text("Task Completion") },
            text = { Text("This task is overdue. How would you like to mark it?") },
            confirmButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    viewModel.markTaskComplete(task, "ON_TIME")
                }) {
                    Text("On time (just marked late)")
                }
            },
            dismissButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    viewModel.markTaskComplete(task, "LATE")
                }) {
                    Text("Definitely late")
                }
            }
        )
    }
}





@Composable
fun ChronometerStatsOverlay(uiState: UiState, activeTasks: List<TimerTask>, onDismiss: () -> Unit, isPeeking: Boolean = false) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background.copy(alpha = 0.8f))
            .clickable { if (!isPeeking) onDismiss() }
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(MaterialTheme.colorScheme.surfaceVariant)
                .clickable { /* prevent dismiss */ }
                .padding(24.dp)
        ) {
            // Header
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.BarChart, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface, modifier = Modifier.size(28.dp))
                Spacer(Modifier.width(12.dp))
                Column {
                    Text("Contextual Analytics", color = MaterialTheme.colorScheme.onSurface, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(4.dp))
                    Box(
                        modifier = Modifier
                            .border(1.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(50))
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                    ) {
                        Text("DEADLINES MODE", color = MaterialTheme.colorScheme.primary, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            
            // Top Stats Row
            Row(modifier = Modifier.fillMaxWidth()) {
                // Left Card
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(16.dp)
                ) {
                    Text("Total Active", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(4.dp))
                    Text("${activeTasks.size}", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(12.dp))
                // Right Card
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(16.dp)
                ) {
                    Text("Urgency Limit", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(4.dp))
                    Text("3 Max", color = MaterialTheme.colorScheme.primary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
            }
            
            Spacer(Modifier.height(24.dp))
            
            // Urgent Queue Section
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.FilterList, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(8.dp))
                Text("URGENT QUEUE (NEXT 3 DEADLINE TARGETS)", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(12.dp))
            
            val urgentTasks = activeTasks.sortedBy { it.targetDateTime }.take(3)
            val format = SimpleDateFormat(if (uiState.use24HourFormat) "M/d/yyyy HH:mm" else "M/d/yyyy hh:mm a", Locale.getDefault())
            
            if (urgentTasks.isEmpty()) {
                Text("No active tasks.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp, modifier = Modifier.padding(vertical = 8.dp))
            } else {
                urgentTasks.forEach { task ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 6.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            task.name, 
                            color = MaterialTheme.colorScheme.onSurface, 
                            fontWeight = FontWeight.Bold, 
                            maxLines = 1,
                            modifier = Modifier.weight(1f).padding(end = 8.dp)
                        )
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text(
                                format.format(Date(task.targetDateTime)), 
                                color = MaterialTheme.colorScheme.primary, 
                                fontSize = 11.sp,
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
            
            Spacer(Modifier.height(24.dp))
            
            // Footer
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
            Spacer(Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    "Peeking active: ${if(isPeeking) "Yes" else "No"}", 
                    color = MaterialTheme.colorScheme.onSurfaceVariant, 
                    fontSize = 11.sp, 
                    fontFamily = FontFamily.Monospace
                )
                Text(
                    if (isPeeking) "Release to close" else "Click outside to close", 
                    color = MaterialTheme.colorScheme.onSurfaceVariant, 
                    fontSize = 11.sp, 
                    fontFamily = FontFamily.Monospace
                )
            }
        }
    }
}

@Composable
fun CreateChronometerOverlay(
    use24HourFormat: Boolean,
    onDismiss: () -> Unit,
    onCreate: (name: String, targetTime: Long, createdAt: Long, recurring: String?, priority: String, deadlineDateTime: Long?) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var targetTime by remember { mutableStateOf(System.currentTimeMillis() + 3600000L) } // default +1 hour
    var createdAt by remember { mutableStateOf(System.currentTimeMillis()) }
    var recurring by remember { mutableStateOf<String?>(null) }
    var priority by remember { mutableStateOf("Normal") }
    var deadlineDateTime by remember { mutableStateOf<Long?>(null) }
    
    var showTargetPicker by remember { mutableStateOf(false) }
    var showCreatedPicker by remember { mutableStateOf(false) }
    var showPriorityMenu by remember { mutableStateOf(false) }
    var showDeadlineMenu by remember { mutableStateOf(false) }
    var showCustomDeadlinePicker by remember { mutableStateOf(false) }
    val context = LocalContext.current
    
    
    if (showTargetPicker) {
        DateTimePickerDialog(
            initialTime = targetTime,
            use24HourFormat = use24HourFormat,
            onDismiss = { showTargetPicker = false },
            onTimeSelected = { 
                targetTime = it
                showTargetPicker = false
            }
        )
    }
    
    if (showCreatedPicker) {
        DateTimePickerDialog(
            initialTime = createdAt,
            use24HourFormat = use24HourFormat,
            onDismiss = { showCreatedPicker = false },
            onTimeSelected = { 
                createdAt = it
                showCreatedPicker = false
            }
        )
    }

    if (showCustomDeadlinePicker) {
        DateTimePickerDialog(
            initialTime = deadlineDateTime ?: (targetTime - 3600000L),
            use24HourFormat = use24HourFormat,
            onDismiss = { showCustomDeadlinePicker = false },
            onTimeSelected = { 
                if (it > targetTime) {
                    android.widget.Toast.makeText(context, "Deadline cannot be after target", android.widget.Toast.LENGTH_SHORT).show()
                } else if (it < createdAt) {
                    android.widget.Toast.makeText(context, "Deadline cannot be before start time", android.widget.Toast.LENGTH_SHORT).show()
                } else {
                    deadlineDateTime = it
                    showCustomDeadlinePicker = false
                }
            }
        )
    }

    val formatDateTime = { time: Long ->
        SimpleDateFormat(if (use24HourFormat) "dd-MM-yyyy HH:mm" else "dd-MM-yyyy hh:mm a", Locale.getDefault()).format(Date(time))
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background.copy(alpha = 0.8f))
            .clickable { onDismiss() }
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(MaterialTheme.colorScheme.surfaceVariant) // Dark grey, like image
                .clickable { /* prevent dismiss */ }
                .border(1.dp, MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f), RoundedCornerShape(24.dp))
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("✨ ", fontSize = 20.sp)
                    Text("Create Deadline", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                }
                IconButton(onClick = onDismiss, modifier = Modifier.size(24.dp)) {
                    Icon(Icons.Default.Clear, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
            
            Column(modifier = Modifier.padding(20.dp).weight(1f, fill = false).verticalScroll(rememberScrollState())) {
                // Name
                Text("TIMER LABEL / TASK NAME", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    placeholder = { Text("e.g., Marketing Deck, Shift Target", color = MaterialTheme.colorScheme.onSurfaceVariant) },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f),
                        focusedTextColor = MaterialTheme.colorScheme.onSurface,
                        unfocusedTextColor = MaterialTheme.colorScheme.onSurface
                    ),
                    singleLine = true
                )
                
                Spacer(Modifier.height(20.dp))
                
                // Target Deadline
                Text("TARGET DEADLINE (ABSOLUTE)", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable { showTargetPicker = true }
                        .testTag("target_deadline_row")
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Edit, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(formatDateTime(targetTime), color = MaterialTheme.colorScheme.onSurface)
                    }
                    Icon(Icons.Default.Edit, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                }
                
                Spacer(Modifier.height(20.dp))
                
                // Quick Adjust
                Text("QUICK ADJUST TARGET (ADD OFFSETS)", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    val addTime = { ms: Long -> targetTime += ms }
                    val btnModifier = Modifier.weight(1f).height(40.dp)
                    val btnColors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant, 
                        contentColor = MaterialTheme.colorScheme.onSurface,
                        disabledContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                        disabledContentColor = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    
                    Button(onClick = { }, enabled = false, modifier = btnModifier, shape = RoundedCornerShape(8.dp), colors = btnColors, contentPadding = PaddingValues(0.dp)) {
                        Text("+15 Min", fontSize = 12.sp)
                    }
                    Spacer(Modifier.width(8.dp))
                    Button(onClick = { }, enabled = false, modifier = btnModifier, shape = RoundedCornerShape(8.dp), colors = btnColors, contentPadding = PaddingValues(0.dp)) {
                        Text("+1 Hour", fontSize = 12.sp)
                    }
                    Spacer(Modifier.width(8.dp))
                    Button(onClick = { }, enabled = false, modifier = btnModifier, shape = RoundedCornerShape(8.dp), colors = btnColors, contentPadding = PaddingValues(0.dp)) {
                        Text("+1 Day", fontSize = 12.sp)
                    }
                    Spacer(Modifier.width(8.dp))
                    Button(onClick = { }, enabled = false, modifier = btnModifier, shape = RoundedCornerShape(8.dp), colors = btnColors, contentPadding = PaddingValues(0.dp)) {
                        Text("+1 Week", fontSize = 12.sp)
                    }
                }
                
                Spacer(Modifier.height(20.dp))
                
                // Creation Date
                Text("CREATION DATE", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .clickable { showCreatedPicker = true }
                        .testTag("created_at_row")
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Edit, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(formatDateTime(createdAt), color = MaterialTheme.colorScheme.onSurface)
                    }
                    Icon(Icons.Default.Edit, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                }
                
                Spacer(Modifier.height(20.dp))
                
                // Recurring
                Text("RECURRING", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val context = LocalContext.current
                    Box(modifier = Modifier.weight(1f)) {
                        val priorityColor = when (priority) {
                            "High" -> Color(0xFFE57373)
                            "Normal" -> MaterialTheme.colorScheme.onSurfaceVariant
                            "Low" -> Color(0xFF81C784)
                            else -> MaterialTheme.colorScheme.onSurfaceVariant
                        }
                        OutlinedButton(
                            onClick = { showPriorityMenu = true },
                            modifier = Modifier.fillMaxWidth().height(48.dp),
                            shape = RoundedCornerShape(12.dp),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = priorityColor),
                            border = androidx.compose.foundation.BorderStroke(1.dp, priorityColor.copy(alpha = 0.5f))
                        ) {
                            Icon(Icons.Outlined.Info, contentDescription = "Priority", modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(8.dp))
                            Text(priority)
                        }
                        DropdownMenu(
                            expanded = showPriorityMenu,
                            onDismissRequest = { showPriorityMenu = false },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            DropdownMenuItem(
                                text = { Text("High", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { priority = "High"; showPriorityMenu = false }
                            )
                            DropdownMenuItem(
                                text = { Text("Normal", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { priority = "Normal"; showPriorityMenu = false }
                            )
                            DropdownMenuItem(
                                text = { Text("Low", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { priority = "Low"; showPriorityMenu = false }
                            )
                        }
                    }
                    Box(modifier = Modifier.weight(1f)) {
                        val deadlineText = if (deadlineDateTime != null) {
                            val diff = targetTime - deadlineDateTime!!
                            if (diff == 30 * 60 * 1000L) "30m before"
                            else if (diff == 60 * 60 * 1000L) "1h before"
                            else "Custom"
                        } else "Deadline"
                        val deadlineColor = if (deadlineDateTime != null) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                        OutlinedButton(
                            onClick = { showDeadlineMenu = true },
                            modifier = Modifier.fillMaxWidth().height(48.dp),
                            shape = RoundedCornerShape(12.dp),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = deadlineColor),
                            border = androidx.compose.foundation.BorderStroke(1.dp, deadlineColor.copy(alpha = 0.5f))
                        ) {
                            Icon(Icons.Outlined.Alarm, contentDescription = "Deadline", modifier = Modifier.size(16.dp))
                            Spacer(Modifier.width(8.dp))
                            Text(deadlineText)
                        }
                        DropdownMenu(
                            expanded = showDeadlineMenu,
                            onDismissRequest = { showDeadlineMenu = false },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            DropdownMenuItem(
                                text = { Text("30 mins before", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    val newDeadline = targetTime - (30 * 60 * 1000L)
                                    if (newDeadline >= createdAt) {
                                        deadlineDateTime = newDeadline
                                    } else {
                                        android.widget.Toast.makeText(context, "Cannot set before start time", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                    showDeadlineMenu = false 
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("1 hour before", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    val newDeadline = targetTime - (60 * 60 * 1000L)
                                    if (newDeadline >= createdAt) {
                                        deadlineDateTime = newDeadline
                                    } else {
                                        android.widget.Toast.makeText(context, "Cannot set before start time", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                    showDeadlineMenu = false 
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Custom...", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    showDeadlineMenu = false 
                                    showCustomDeadlinePicker = true
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Clear", color = MaterialTheme.colorScheme.onSurface) },
                                onClick = { 
                                    deadlineDateTime = null
                                    showDeadlineMenu = false 
                                }
                            )
                        }
                    }
                }
                
                Spacer(Modifier.height(20.dp))
                
                // Recurring
                Text("RECURRING", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    val recurringOptions = listOf("Daily", "Weekly", "Monthly", "Annually", "Custom")
                    recurringOptions.forEach { opt ->
                        val isSelected = recurring == opt
                        val isDisabled = opt == "Custom"
                        val bgColor = if (isSelected) MaterialTheme.colorScheme.primary.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceVariant
                        val textColor = if (isDisabled) MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f) else if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                        val borderColor = if (isSelected) MaterialTheme.colorScheme.primary else Color.Transparent
                        
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .height(40.dp)
                                .padding(horizontal = 2.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(bgColor)
                                .border(1.dp, borderColor, RoundedCornerShape(8.dp))
                                .clickable(enabled = !isDisabled) { recurring = if (isSelected) null else opt },
                            contentAlignment = Alignment.Center
                        ) {
                            Text(opt, color = textColor, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
            
            HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
            
            // Footer
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                horizontalArrangement = Arrangement.End
            ) {
                Button(
                    onClick = onDismiss,
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.height(48.dp)
                ) {
                    Text("Cancel")
                }
                Spacer(Modifier.width(16.dp))
                Button(
                    onClick = { onCreate(if (name.isBlank()) "Untitled Task" else name, targetTime, createdAt, recurring, priority, deadlineDateTime) },
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.height(48.dp)
                ) {
                    Text("+ Create Timer", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateTimePickerDialog(
    initialTime: Long,
    use24HourFormat: Boolean,
    onDismiss: () -> Unit,
    onTimeSelected: (Long) -> Unit
) {
    var showTimePicker by remember { mutableStateOf(false) }
    val datePickerState = rememberDatePickerState(initialSelectedDateMillis = initialTime)
    
    val timePickerState = rememberTimePickerState(
        initialHour = java.util.Calendar.getInstance().apply { timeInMillis = initialTime }.get(java.util.Calendar.HOUR_OF_DAY),
        initialMinute = java.util.Calendar.getInstance().apply { timeInMillis = initialTime }.get(java.util.Calendar.MINUTE),
        is24Hour = use24HourFormat
    )

    if (showTimePicker) {
        AlertDialog(
            onDismissRequest = onDismiss,
            title = { Text("Select Time") },
            text = { TimePicker(state = timePickerState) },
            confirmButton = {
                TextButton(onClick = {
                    val selectedDateMillis = datePickerState.selectedDateMillis ?: initialTime
                    val cal = java.util.Calendar.getInstance().apply { timeInMillis = selectedDateMillis }
                    cal.set(java.util.Calendar.HOUR_OF_DAY, timePickerState.hour)
                    cal.set(java.util.Calendar.MINUTE, timePickerState.minute)
                    onTimeSelected(cal.timeInMillis)
                }) {
                    Text("OK")
                }
            },
            dismissButton = {
                TextButton(onClick = onDismiss) {
                    Text("Cancel")
                }
            }
        )
    } else {
        DatePickerDialog(
            onDismissRequest = onDismiss,
            confirmButton = {
                TextButton(onClick = { showTimePicker = true }) {
                    Text("Next")
                }
            },
            dismissButton = {
                TextButton(onClick = onDismiss) {
                    Text("Cancel")
                }
            }
        ) {
            DatePicker(state = datePickerState)
        }
    }
}


@Composable
fun AutoResizedText(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = Color.Unspecified,
    fontFamily: FontFamily? = null,
    fontWeight: FontWeight? = null,
    textAlign: TextAlign? = null,
    maxLines: Int = 1
) {
    var multiplier by remember { mutableStateOf(1f) }
    
    Text(
        text = text,
        modifier = modifier,
        color = color,
        fontFamily = fontFamily,
        fontWeight = fontWeight,
        textAlign = textAlign,
        maxLines = maxLines,
        fontSize = 48.sp * multiplier,
        onTextLayout = {
            if (it.hasVisualOverflow) {
                multiplier *= 0.9f
            }
        }
    )
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StageFilterDialog(
    uiState: UiState,
    activeTasks: List<TimerTask>,
    onDismiss: () -> Unit,
    viewModel: MainViewModel
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface,
        dragHandle = { BottomSheetDefaults.DragHandle() },
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 32.dp)
        ) {
            Text(
                "Stage Configuration",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            // Segmented Toggle
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                    .padding(4.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(8.dp))
                        .clickable { viewModel.toggleUrgentMode(true) }
                        .background(if (uiState.isUrgentMode) MaterialTheme.colorScheme.primary else Color.Transparent)
                        .padding(vertical = 12.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        "Auto Urgency",
                        color = if (uiState.isUrgentMode) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = FontWeight.SemiBold
                    )
                }
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .clip(RoundedCornerShape(8.dp))
                        .clickable { viewModel.toggleUrgentMode(false) }
                        .background(if (!uiState.isUrgentMode) MaterialTheme.colorScheme.primary else Color.Transparent)
                        .padding(vertical = 12.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        "Manual Pinned",
                        color = if (!uiState.isUrgentMode) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            if (uiState.isUrgentMode) {
                // Auto Urgency UI
                Surface(
                    color = MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.5f),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Info,
                            contentDescription = "Info",
                            tint = MaterialTheme.colorScheme.onTertiaryContainer
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            "Urgency Engine Override Active: The application is dynamically displaying the ${if (uiState.maxStageSlots == -1) "all" else uiState.maxStageSlots} nearest target deadlines.",
                            color = MaterialTheme.colorScheme.onTertiaryContainer,
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }
            } else {
                // Manual Pinned UI
                Surface(
                    color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.3f),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Outlined.Info,
                            contentDescription = "Info",
                            tint = MaterialTheme.colorScheme.onSecondaryContainer
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            "Custom Manual Pinning Active: Select up to ${if (uiState.maxStageSlots == -1) "unlimited" else uiState.maxStageSlots} timers from the list below to pin them onto your main Stage.",
                            color = MaterialTheme.colorScheme.onSecondaryContainer,
                            style = MaterialTheme.typography.bodyMedium
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                LazyColumn(
                    modifier = Modifier.fillMaxWidth().heightIn(max = 400.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(activeTasks, key = { it.id }) { task ->
                        val isPinned = uiState.selectedDisplayIds.contains(task.id)
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .border(
                                    width = if (isPinned) 2.dp else 1.dp,
                                    color = if (isPinned) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline.copy(alpha = 0.3f),
                                    shape = RoundedCornerShape(12.dp)
                                )
                                .background(
                                    if (isPinned) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.2f) 
                                    else Color.Transparent
                                )
                                .clickable { viewModel.toggleDisplayId(task.id) }
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = task.name,
                                style = MaterialTheme.typography.titleMedium,
                                color = if (isPinned) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant,
                                fontWeight = if (isPinned) FontWeight.Bold else FontWeight.Normal,
                                modifier = Modifier.weight(1f)
                            )
                            if (isPinned) {
                                Surface(
                                    color = MaterialTheme.colorScheme.primary,
                                    shape = CircleShape
                                ) {
                                    Text(
                                        "📌 Pinned",
                                        color = MaterialTheme.colorScheme.onPrimary,
                                        style = MaterialTheme.typography.labelSmall,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            } else {
                                Surface(
                                    color = Color.Transparent,
                                    shape = CircleShape,
                                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha=0.5f))
                                ) {
                                    Text(
                                        "Unpinned",
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        style = MaterialTheme.typography.labelSmall,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
