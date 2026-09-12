package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.outlined.Alarm
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import com.example.util.parseTerminalCommand
import androidx.compose.animation.AnimatedVisibility
import java.text.SimpleDateFormat
import java.util.Locale
import androidx.compose.foundation.text.KeyboardActions
import com.example.ui.components.UniversalDatePickerDialog
import com.example.ui.components.UniversalTimePickerDialog
import java.util.Calendar
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import kotlinx.coroutines.delay

@Composable
fun HomeScreen(
    viewModel: MainViewModel,
    uiState: UiState,
    onMenuClick: () -> Unit,
    onProfileClick: () -> Unit
) {
    val context = LocalContext.current
    
    var rawInput by remember { mutableStateOf("") }
    val parsedState by remember { derivedStateOf { parseTerminalCommand(rawInput) } }
    
    var deadlineTimeMillis by remember { mutableStateOf<Long?>(null) }
    var showDatePicker by remember { mutableStateOf(false) }
    var showTimePicker by remember { mutableStateOf(false) }
    var tempDateMillis by remember { mutableStateOf(0L) }
    val focusRequester = remember { FocusRequester() }
    
    val activeTasks by viewModel.activeTasks.collectAsState()
    val quickDeadlines = activeTasks.filter { it.labels == "Reminder" }.sortedBy { it.deadlineDateTime ?: Long.MAX_VALUE }

    var currentTime by remember { mutableStateOf(System.currentTimeMillis()) }
    LaunchedEffect(Unit) {
        while (true) {
            delay(1000L)
            currentTime = System.currentTimeMillis()
        }
    }

    val activeTask = remember(uiState.dailySchedules, currentTime) {
        uiState.dailySchedules.firstOrNull { it.startTime <= currentTime && it.endTime > currentTime }
    }
    val standbyTask = remember(uiState.dailySchedules, currentTime) {
        uiState.dailySchedules
            .filter { it.startTime > currentTime }
            .minByOrNull { it.startTime }
    }
    
    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .windowInsetsPadding(WindowInsets.safeDrawing.only(WindowInsetsSides.Top))
                .padding(horizontal = 8.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onMenuClick) {
                Icon(
                    imageVector = Icons.Default.Menu,
                    contentDescription = "Menu",
                    modifier = Modifier.size(28.dp),
                    tint = MaterialTheme.colorScheme.onSurface
                )
            }
            
            Box(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                com.example.ui.screens.GlobalHeader(uiState, onTimeClick = { viewModel.setTimerMode(com.example.viewmodel.TimerMode.LANDSCAPE_CHRONOGRAPH) })
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))

        // Protocol HUD: [ NOW ] Active Protocol & [ NEXT ] Standby Protocol
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            val outlineColor = MaterialTheme.colorScheme.outline
            if (activeTask != null) {
                val startStr = TimeFormatUtils.formatTimeOnly(activeTask.startTime, uiState.use24HourFormat)
                val endStr = TimeFormatUtils.formatTimeOnly(activeTask.endTime, uiState.use24HourFormat)
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(120.dp)
                        .background(MaterialTheme.colorScheme.primary, RectangleShape)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "[ ACTIVE ]",
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                    Text(
                        text = "$startStr - $endStr",
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Medium,
                        fontSize = 14.sp,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                    Text(
                        text = activeTask.title.uppercase(Locale.getDefault()),
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 16.sp,
                        maxLines = 1,
                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                }
            } else {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(120.dp)
                        .background(Color.Transparent, RectangleShape)
                        .drawBehind {
                            val stroke = Stroke(
                                width = 1.dp.toPx(),
                                pathEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                            )
                            drawRect(
                                color = outlineColor,
                                style = stroke
                            )
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "[ NO ACTIVE PROTOCOL ]",
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            if (standbyTask != null) {
                val standbyStartStr = TimeFormatUtils.formatTimeOnly(standbyTask.startTime, uiState.use24HourFormat)
                val standbyEndStr = TimeFormatUtils.formatTimeOnly(standbyTask.endTime, uiState.use24HourFormat)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(80.dp)
                        .background(Color.Transparent, RectangleShape)
                        .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RectangleShape)
                        .padding(horizontal = 14.dp, vertical = 10.dp)
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            text = "[ STANDBY ]",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Text(
                            text = "$standbyStartStr - $standbyEndStr",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
                        )
                        Text(
                            text = standbyTask.title.uppercase(Locale.getDefault()),
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            if (quickDeadlines.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillParentMaxSize(), contentAlignment = Alignment.Center) {
                        Text(
                            text = "[ NO ACTIVE REMINDERS ]",
                            fontFamily = FontFamily.Monospace,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            } else {
                items(quickDeadlines, key = { it.id }) { task ->
                    com.example.ui.components.TerminalReminderRow(
                        task = task,
                        use24HourFormat = uiState.use24HourFormat,
                        onComplete = { viewModel.markTaskComplete(it) }
                    )
                }
            }
        }
        
        // The Tactical Feedback HUD
        AnimatedVisibility(visible = parsedState.epochMillis != null || parsedState.priority != "Normal") {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                if (parsedState.epochMillis != null) {
                    val format = SimpleDateFormat("HH:mm MMM dd", Locale.getDefault())
                    val timeStr = format.format(parsedState.epochMillis)
                    Text(
                        text = "[ @ $timeStr ]",
                        fontFamily = FontFamily.Monospace,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier
                            .border(1.dp, MaterialTheme.colorScheme.primary, RectangleShape)
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
                if (parsedState.priority != "Normal") {
                    val color = if (parsedState.priority == "CRITICAL") MaterialTheme.colorScheme.error else Color(0xFFFFA000) // Amber for MID
                    Text(
                        text = "[ ! ${parsedState.priority} ]",
                        fontFamily = FontFamily.Monospace,
                        style = MaterialTheme.typography.labelMedium,
                        color = color,
                        modifier = Modifier
                            .border(1.dp, color, RectangleShape)
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }
        }
        
        // The Terminal Input Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.surface)
                .border(1.dp, MaterialTheme.colorScheme.outline, RectangleShape)
                .padding(horizontal = 8.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = rawInput,
                onValueChange = { rawInput = it },
                modifier = Modifier
                    .weight(1f)
                    .focusRequester(focusRequester),
                placeholder = { 
                    Text(
                        "> QUICK REMINDER...", 
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                    ) 
                },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                keyboardActions = KeyboardActions(
                    onDone = {
                        val finalTime = parsedState.epochMillis ?: deadlineTimeMillis
                        if (parsedState.cleanTitle.isNotBlank()) {
                            viewModel.addQuickDeadline(parsedState.cleanTitle, finalTime, parsedState.priority)
                            rawInput = ""
                            deadlineTimeMillis = null
                        }
                    }
                ),
                shape = RectangleShape,
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color.Transparent,
                    unfocusedContainerColor = Color.Transparent,
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent
                )
            )
            
            IconButton(onClick = { showDatePicker = true }) {
                Icon(
                    imageVector = Icons.Outlined.Alarm,
                    contentDescription = "Set Deadline",
                    tint = if (deadlineTimeMillis != null) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
                )
            }
            
            IconButton(
                onClick = {
                    val finalTime = parsedState.epochMillis ?: deadlineTimeMillis
                    viewModel.addQuickDeadline(parsedState.cleanTitle, finalTime, parsedState.priority)
                    rawInput = ""
                    deadlineTimeMillis = null
                },
                enabled = parsedState.cleanTitle.isNotBlank()
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Send, 
                    contentDescription = "Save",
                    tint = if (parsedState.cleanTitle.isNotBlank()) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)
                )
            }
        }
    }
    
    if (showDatePicker) {
        UniversalDatePickerDialog(
            initialDateMillis = System.currentTimeMillis(),
            onDateSelected = { dateMillis ->
                tempDateMillis = dateMillis
                showDatePicker = false
                showTimePicker = true
            },
            onDismiss = { showDatePicker = false }
        )
    }
    
    if (showTimePicker) {
        UniversalTimePickerDialog(
            initialHour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY),
            initialMinute = Calendar.getInstance().get(Calendar.MINUTE),
            is24Hour = uiState.use24HourFormat,
            onDismiss = { showTimePicker = false },
            onTimeSelected = { hour, minute ->
                val cal = Calendar.getInstance()
                cal.timeInMillis = tempDateMillis
                cal.set(Calendar.HOUR_OF_DAY, hour)
                cal.set(Calendar.MINUTE, minute)
                cal.set(Calendar.SECOND, 0)
                cal.set(Calendar.MILLISECOND, 0)
                
                deadlineTimeMillis = cal.timeInMillis
                showTimePicker = false
                focusRequester.requestFocus()
            }
        )
    }
}
