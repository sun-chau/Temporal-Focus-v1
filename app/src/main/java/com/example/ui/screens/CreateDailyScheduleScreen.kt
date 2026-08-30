package com.example.ui.screens

import android.app.TimePickerDialog
import android.widget.Toast
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import kotlinx.coroutines.delay
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.DeleteOutline
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.*
import com.example.ui.utils.getLabelColor
import com.example.ui.utils.getLabelName
import com.example.viewmodel.MainViewModel
import java.util.Calendar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateDailyScheduleScreen(
    viewModel: MainViewModel,
    uiState: com.example.viewmodel.UiState,
    onBack: () -> Unit,
    onDiscardAndBack: () -> Unit
) {
    val draft = uiState.dailyScheduleDraft
    val context = LocalContext.current
    val scrollState = rememberScrollState()

    var showStartDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showStartTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var title by remember { mutableStateOf(draft.title) }
    var startTime by remember { mutableStateOf(draft.startTime) }
    var endTime by remember { mutableStateOf(draft.endTime) }
    var selectedTag by remember { mutableStateOf(draft.label) }

    var isRecurring by remember { mutableStateOf(draft.isRecurring) }
    var recurrenceType by remember { mutableStateOf(draft.recurrenceType) }
    var dailyInterval by remember { mutableStateOf(draft.dailyInterval) }
    var weeklyDays by remember { mutableStateOf(draft.weeklyDays) }
    
    var monthlyType by remember { mutableStateOf(draft.monthlyType) }
    var isMultiDay by remember { 
        val startCal = Calendar.getInstance().apply { timeInMillis = draft.startTime }
        val endCal = Calendar.getInstance().apply { timeInMillis = draft.endTime }
        mutableStateOf(
            startCal.get(Calendar.YEAR) != endCal.get(Calendar.YEAR) ||
            startCal.get(Calendar.DAY_OF_YEAR) != endCal.get(Calendar.DAY_OF_YEAR)
        )
    }
    var monthlyDates by remember { mutableStateOf(draft.monthlyDates) }
    var monthlyWeek by remember { mutableStateOf(draft.monthlyWeek) }
    var monthlyDayOfWeek by remember { mutableStateOf(draft.monthlyDayOfWeek) }
    
    var occurrenceCount by remember { mutableStateOf(draft.occurrenceCount) }
    var editEntireSeries by remember { mutableStateOf(draft.editingId != null && draft.seriesId != null) }
    
    var minusHolding by remember { mutableStateOf(false) }
    var plusHolding by remember { mutableStateOf(false) }

    var dailyMinusHolding by remember { mutableStateOf(false) }
    var dailyPlusHolding by remember { mutableStateOf(false) }

    LaunchedEffect(dailyMinusHolding) {
        if (dailyMinusHolding) {
            if (dailyInterval > 1) dailyInterval--
            delay(500)
            while (dailyMinusHolding && dailyInterval > 1) {
                dailyInterval--
                delay(100)
            }
        }
    }

    LaunchedEffect(dailyPlusHolding) {
        if (dailyPlusHolding) {
            dailyInterval++
            delay(500)
            while (dailyPlusHolding) {
                dailyInterval++
                delay(100)
            }
        }
    }

    LaunchedEffect(minusHolding) {
        if (minusHolding) {
            if (occurrenceCount > 0) occurrenceCount--
            delay(500)
            while (minusHolding && occurrenceCount > 0) {
                occurrenceCount--
                delay(100)
            }
        }
    }

    LaunchedEffect(plusHolding) {
        if (plusHolding) {
            occurrenceCount++
            delay(500)
            while (plusHolding) {
                occurrenceCount++
                delay(100)
            }
        }
    }

    // Sync back to viewModel when back is pressed
    val saveDraft = {
        viewModel.updateDailyScheduleDraft(
            draft.copy(
                title = title,
                startTime = startTime,
                endTime = endTime,
                label = selectedTag,
                isRecurring = isRecurring,
                recurrenceType = recurrenceType,
                dailyInterval = dailyInterval,
                weeklyDays = weeklyDays,
                monthlyType = monthlyType,
                monthlyDates = monthlyDates,
                monthlyWeek = monthlyWeek,
                monthlyDayOfWeek = monthlyDayOfWeek,
                annuallyType = AnnuallyType.DATES,
                annuallyMonth = Calendar.JANUARY,
                annuallyDates = emptySet(),
                annuallyWeek = 1,
                annuallyDayOfWeek = Calendar.SUNDAY,
                occurrenceCount = occurrenceCount
            )
        )
    }

    val clearForm = {
        title = ""
        startTime = System.currentTimeMillis()
        endTime = System.currentTimeMillis() + 3600000
        selectedTag = ""
        isRecurring = false
        recurrenceType = RecurrenceType.DAILY
        dailyInterval = 1
        weeklyDays = emptySet()
        monthlyType = MonthlyType.DATES
        monthlyDates = emptySet()
        monthlyWeek = 1
        monthlyDayOfWeek = Calendar.SUNDAY
        occurrenceCount = 1
    }

    // Dynamic String logic
    val dynamicString = remember(
        isRecurring, recurrenceType, dailyInterval, weeklyDays,
        monthlyType, monthlyDates, monthlyWeek, monthlyDayOfWeek,
        occurrenceCount
    ) {
        if (!isRecurring) return@remember "Does not repeat"
        
        val countStr = if (occurrenceCount <= 0) " indefinitely." else if (occurrenceCount > 1) " for $occurrenceCount occurrences." else " once."
        
        when (recurrenceType) {
            RecurrenceType.DAILY -> {
                if (dailyInterval == 1) "Repeats every day$countStr"
                else "Repeats every $dailyInterval days$countStr"
            }
            RecurrenceType.WEEKLY -> {
                if (weeklyDays.isEmpty()) "Repeats weekly on no days$countStr"
                else {
                    val daysStr = weeklyDays.sorted().joinToString(", ") { getDayOfWeekName(it) }
                    "Repeats weekly on $daysStr$countStr"
                }
            }
            RecurrenceType.MONTHLY -> {
                val condition = when (monthlyType) {
                    MonthlyType.DATES -> {
                        if (monthlyDates.isEmpty()) "no dates"
                        else "dates ${monthlyDates.sorted().joinToString(", ")}"
                    }
                    MonthlyType.LAST_DAY -> "the last day of the month"
                    MonthlyType.DAY_OF_WEEK -> {
                        val weekName = getWeekName(monthlyWeek)
                        val dayName = getDayOfWeekName(monthlyDayOfWeek)
                        "the $weekName $dayName"
                    }
                }
                "Repeats every month on $condition$countStr"
            }
            else -> "Does not repeat"
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (draft.editingId == null) "New Schedule" else "Edit Schedule") },
                navigationIcon = {
                    IconButton(onClick = {
                        saveDraft()
                        onBack()
                    }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { clearForm() }) {
                        Icon(Icons.Default.DeleteOutline, contentDescription = "Discard/Clear Form")
                    }
                    IconButton(onClick = {
                        viewModel.clearDailyScheduleDraft()
                        onDiscardAndBack()
                    }) {
                        Icon(Icons.Default.Close, contentDescription = "Discard and Exit")
                    }
                    IconButton(onClick = {
                        if (title.isBlank()) {
                            Toast.makeText(context, "Title cannot be empty", Toast.LENGTH_SHORT).show()
                            return@IconButton
                        }
                        if (endTime <= startTime) {
                            Toast.makeText(context, "End time must be after start time", Toast.LENGTH_SHORT).show()
                            return@IconButton
                        }
                        
                        saveDraft() // sync current state
                        
                        // Grab the updated draft
                        val finalDraft = draft.copy(
                            title = title, startTime = startTime, endTime = endTime, label = selectedTag,
                            isRecurring = isRecurring, recurrenceType = recurrenceType, dailyInterval = dailyInterval,
                            weeklyDays = weeklyDays, monthlyType = monthlyType, monthlyDates = monthlyDates,
                            monthlyWeek = monthlyWeek, monthlyDayOfWeek = monthlyDayOfWeek,
                            annuallyType = AnnuallyType.DATES, annuallyMonth = Calendar.JANUARY, annuallyDates = emptySet(),
                            annuallyWeek = 1, annuallyDayOfWeek = Calendar.SUNDAY,
                            occurrenceCount = occurrenceCount
                        )
                        viewModel.saveAdvancedDailySchedule(finalDraft, editEntireSeries)
                        onDiscardAndBack()
                    }) {
                        Icon(Icons.Default.Check, contentDescription = "Save")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (draft.editingId != null && draft.seriesId != null) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Edit entire series", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    androidx.compose.material3.Switch(
                        checked = editEntireSeries,
                        onCheckedChange = { editEntireSeries = it }
                    )
                }
                HorizontalDivider(modifier = Modifier.padding(bottom = 8.dp))
            }

            // Task Details
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Task Title") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            Row(
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Multi-Day Event", fontSize = 16.sp, fontWeight = FontWeight.Medium)
                androidx.compose.material3.Switch(checked = isMultiDay, onCheckedChange = { isMultiDay = it })
            }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                // Start Time
                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
                val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val startDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(startCal.time)
                
                if (showStartDatePicker) {
                    com.example.ui.components.UniversalDatePickerDialog(
                        initialDateMillis = startTime,
                        onDateSelected = { newDateMillis ->
                            val diff = endTime - startTime
                            val oldCal = java.util.Calendar.getInstance().apply { timeInMillis = startTime }
                            val newCal = java.util.Calendar.getInstance().apply { timeInMillis = newDateMillis }
                            newCal.set(java.util.Calendar.HOUR_OF_DAY, oldCal.get(java.util.Calendar.HOUR_OF_DAY))
                            newCal.set(java.util.Calendar.MINUTE, oldCal.get(java.util.Calendar.MINUTE))
                            newCal.set(java.util.Calendar.SECOND, oldCal.get(java.util.Calendar.SECOND))
                            newCal.set(java.util.Calendar.MILLISECOND, oldCal.get(java.util.Calendar.MILLISECOND))
                            startTime = newCal.timeInMillis
                            endTime = startTime + maxOf(0L, diff)
                            showStartDatePicker = false
                        },
                        onDismiss = { showStartDatePicker = false }
                    )
                }
                if (showStartTimePicker) {
                    val startCalNow = Calendar.getInstance().apply { timeInMillis = startTime }
                    com.example.ui.components.UniversalTimePickerDialog(
                        initialHour = startCalNow.get(Calendar.HOUR_OF_DAY),
                        initialMinute = startCalNow.get(Calendar.MINUTE),
                        is24Hour = uiState.use24HourFormat,
                        onTimeSelected = { hourOfDay, minute ->
                            val newCal = Calendar.getInstance().apply {
                                timeInMillis = startTime
                                set(Calendar.HOUR_OF_DAY, hourOfDay)
                                set(Calendar.MINUTE, minute)
                            }
                            val diff = endTime - startTime
                            startTime = newCal.timeInMillis
                            endTime = startTime + maxOf(0L, diff)
                            showStartTimePicker = false
                        },
                        onDismiss = { showStartTimePicker = false }
                    )
                }

                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        if (isMultiDay) {
                            showStartDatePicker = true
                        } else {
                            showStartTimePicker = true
                        }
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("Start Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(startText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                        if (isMultiDay) {
                            Text(startDateText, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }

                // End Time
                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
                val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val endDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(endCal.time)
                
                if (showEndDatePicker) {
                    com.example.ui.components.UniversalDatePickerDialog(
                        initialDateMillis = endTime,
                        onDateSelected = { newDateMillis ->
                            val oldCal = java.util.Calendar.getInstance().apply { timeInMillis = endTime }
                            val newCal = java.util.Calendar.getInstance().apply { timeInMillis = newDateMillis }
                            newCal.set(java.util.Calendar.HOUR_OF_DAY, oldCal.get(java.util.Calendar.HOUR_OF_DAY))
                            newCal.set(java.util.Calendar.MINUTE, oldCal.get(java.util.Calendar.MINUTE))
                            newCal.set(java.util.Calendar.SECOND, oldCal.get(java.util.Calendar.SECOND))
                            newCal.set(java.util.Calendar.MILLISECOND, oldCal.get(java.util.Calendar.MILLISECOND))
                            endTime = maxOf(startTime, newCal.timeInMillis)
                            showEndDatePicker = false
                        },
                        onDismiss = { showEndDatePicker = false }
                    )
                }
                if (showEndTimePicker) {
                    val endCalNow = Calendar.getInstance().apply { timeInMillis = endTime }
                    com.example.ui.components.UniversalTimePickerDialog(
                        initialHour = endCalNow.get(Calendar.HOUR_OF_DAY),
                        initialMinute = endCalNow.get(Calendar.MINUTE),
                        is24Hour = uiState.use24HourFormat,
                        onTimeSelected = { hourOfDay, minute ->
                            val newCal = Calendar.getInstance().apply {
                                timeInMillis = if (isMultiDay) endTime else startTime
                                set(Calendar.HOUR_OF_DAY, hourOfDay)
                                set(Calendar.MINUTE, minute)
                            }
                            if (!isMultiDay && newCal.timeInMillis < startTime) {
                                newCal.add(Calendar.DAY_OF_YEAR, 1)
                            }
                            endTime = newCal.timeInMillis
                            showEndTimePicker = false
                        },
                        onDismiss = { showEndTimePicker = false }
                    )
                }

                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        if (isMultiDay) {
                            showEndDatePicker = true
                        } else {
                            showEndTimePicker = true
                        }
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("End Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(endText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                        
                        // Show "Tomorrow" or Date
                        val startDayCal = Calendar.getInstance().apply {
                            timeInMillis = startTime
                            set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0); set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
                        }
                        val endDayCal = Calendar.getInstance().apply {
                            timeInMillis = endTime
                            set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0); set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
                        }
                        
                        if (isMultiDay) {
                            Text(endDateText, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                        } else if (endDayCal.timeInMillis > startDayCal.timeInMillis) {
                            Text("Tomorrow", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                        }
                    }
                }
            }

            // Category Tag
            Text("Category Tag", fontSize = 14.sp, fontWeight = FontWeight.Medium)
            val labels = uiState.customLabels.toList()
            if (labels.isEmpty()) {
                Text(
                    text = "No categories available. Add categories in Profile & Labels to label your tasks.",
                    color = MaterialTheme.colorScheme.error,
                    fontSize = 14.sp
                )
            } else {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    item {
                        val isNoneSelected = selectedTag.isBlank()
                        Box(
                            modifier = Modifier
                                .height(36.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isNoneSelected) MaterialTheme.colorScheme.surfaceVariant else androidx.compose.ui.graphics.Color.Transparent)
                                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
                                .clickable { selectedTag = "" }
                                .padding(horizontal = 12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(androidx.compose.material.icons.Icons.Default.Close, contentDescription = "None", modifier = Modifier.size(16.dp).padding(end = 4.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                Text(
                                    text = "None",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                    items(labels) { label ->
                        val isSelected = selectedTag == label
                        val color = getLabelColor(label, true)
                        Box(
                            modifier = Modifier
                                .height(36.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isSelected) color else color.copy(alpha = 0.2f))
                                .clickable { selectedTag = if (selectedTag == label) "" else label }
                                .padding(horizontal = 12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = getLabelName(label),
                                color = if (isSelected) MaterialTheme.colorScheme.onSurface else color,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }

            androidx.compose.material3.HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))

            if (draft.editingId != null) {
                OutlinedButton(
                    onClick = {
                        viewModel.deleteDailyScheduleSync(draft.editingId, editEntireSeries)
                        viewModel.clearDailyScheduleDraft()
                        onDiscardAndBack()
                    },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error)
                ) {
                    Text("Delete Schedule", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold)
                }
            }

            // Recurring Section
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Recurring Schedule", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                Switch(checked = isRecurring, onCheckedChange = { isRecurring = it })
            }

            if (isRecurring) {
                Text(text = dynamicString, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Medium)
                
                // Recurrence Count
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Number of occurrences: ", fontSize = 16.sp, modifier = Modifier.weight(1f))
                    
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .pointerInput(Unit) {
                                    detectTapGestures(
                                        onPress = {
                                            minusHolding = true
                                            tryAwaitRelease()
                                            minusHolding = false
                                        }
                                    )
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text("-", fontSize = 36.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        }
                        
                        Text(
                            text = if (occurrenceCount <= 0) "∞" else "$occurrenceCount",
                            fontWeight = FontWeight.Bold,
                            fontSize = 24.sp,
                            modifier = Modifier.widthIn(min = 40.dp),
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                        
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .pointerInput(Unit) {
                                    detectTapGestures(
                                        onPress = {
                                            plusHolding = true
                                            tryAwaitRelease()
                                            plusHolding = false
                                        }
                                    )
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text("+", fontSize = 36.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        }
                    }
                }

                ScrollableTabRow(
                    selectedTabIndex = when (recurrenceType) {
                        RecurrenceType.DAILY -> 0
                        RecurrenceType.WEEKLY -> 1
                        RecurrenceType.MONTHLY -> 2
                        else -> 0
                    },
                    edgePadding = 0.dp
                ) {
                    Tab(selected = recurrenceType == RecurrenceType.DAILY, onClick = { recurrenceType = RecurrenceType.DAILY }, text = { Text("Daily") })
                    Tab(selected = recurrenceType == RecurrenceType.WEEKLY, onClick = { recurrenceType = RecurrenceType.WEEKLY }, text = { Text("Weekly") })
                    Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }, text = { Text("Monthly") })
                }

                Spacer(modifier = Modifier.height(8.dp))

                when (recurrenceType) {
                    RecurrenceType.DAILY -> {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Text("Every ", fontSize = 16.sp)
                            
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                dailyMinusHolding = true
                                                tryAwaitRelease()
                                                dailyMinusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("-", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                            
                            Text(
                                text = "$dailyInterval",
                                fontWeight = FontWeight.Bold,
                                fontSize = 20.sp,
                                modifier = Modifier.widthIn(min = 40.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                            
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                dailyPlusHolding = true
                                                tryAwaitRelease()
                                                dailyPlusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("+", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                            
                            Text(" days", fontSize = 16.sp)
                        }
                    }
                    RecurrenceType.WEEKLY -> {
                        val daysOfWeek = listOf(
                            Calendar.SUNDAY to "S", Calendar.MONDAY to "M", Calendar.TUESDAY to "T",
                            Calendar.WEDNESDAY to "W", Calendar.THURSDAY to "T", Calendar.FRIDAY to "F", Calendar.SATURDAY to "S"
                        )
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                            daysOfWeek.forEach { (dayValue, label) ->
                                val isSelected = weeklyDays.contains(dayValue)
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .aspectRatio(1f)
                                        .clip(CircleShape)
                                        .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                        .clickable {
                                            weeklyDays = if (isSelected) weeklyDays - dayValue else weeklyDays + dayValue
                                            if (weeklyDays.size == 7) {
                                                // All selected -> basically daily
                                                recurrenceType = RecurrenceType.DAILY
                                                dailyInterval = 1
                                            }
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = label,
                                        color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            }
                        }
                    }
                    RecurrenceType.MONTHLY -> {
                        var expandedType by remember { mutableStateOf(false) }
                        ExposedDropdownMenuBox(expanded = expandedType, onExpandedChange = { expandedType = it }) {
                            OutlinedTextField(
                                value = when(monthlyType) {
                                    MonthlyType.DATES -> "Select Dates"
                                    MonthlyType.LAST_DAY -> "Last day of the month"
                                    MonthlyType.DAY_OF_WEEK -> "Day of the week"
                                },
                                onValueChange = {},
                                readOnly = true,
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedType) },
                                modifier = Modifier.menuAnchor().fillMaxWidth()
                            )
                            ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                                DropdownMenuItem(text = { Text("Select Dates") }, onClick = { monthlyType = MonthlyType.DATES; expandedType = false })
                                DropdownMenuItem(text = { Text("Last day of the month") }, onClick = { monthlyType = MonthlyType.LAST_DAY; expandedType = false })
                                DropdownMenuItem(text = { Text("Day of the week") }, onClick = { monthlyType = MonthlyType.DAY_OF_WEEK; expandedType = false })
                            }
                        }
                        
                        if (monthlyType == MonthlyType.DATES) {
                            // Quick grid of 1-31
                            var datesInput by remember { mutableStateOf(monthlyDates.joinToString(",")) }
                            OutlinedTextField(
                                value = datesInput,
                                onValueChange = { 
                                    datesInput = it
                                    val parsed = parseDateString(it)
                                    monthlyDates = parsed
                                    if (monthlyDates.size == 31) {
                                        recurrenceType = RecurrenceType.DAILY
                                        dailyInterval = 1
                                    }
                                },
                                label = { Text("Dates (e.g., 1-5, 10, 15-20)") },
                                modifier = Modifier.fillMaxWidth()
                            )
                        } else if (monthlyType == MonthlyType.DAY_OF_WEEK) {
                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                var expandedWeek by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedWeek, onExpandedChange = { expandedWeek = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getWeekName(monthlyWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedWeek) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedWeek, onDismissRequest = { expandedWeek = false }) {
                                        (1..5).forEach { w ->
                                            DropdownMenuItem(text = { Text(getWeekName(w)) }, onClick = { monthlyWeek = w; expandedWeek = false })
                                        }
                                    }
                                }
                                var expandedDay by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedDay, onExpandedChange = { expandedDay = it }, modifier = Modifier.weight(1f)) {
                                    OutlinedTextField(
                                        value = getDayOfWeekName(monthlyDayOfWeek),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedDay) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedDay, onDismissRequest = { expandedDay = false }) {
                                        (Calendar.SUNDAY..Calendar.SATURDAY).forEach { d ->
                                            DropdownMenuItem(text = { Text(getDayOfWeekName(d)) }, onClick = { monthlyDayOfWeek = d; expandedDay = false })
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    else -> {}
                }
            }
        }
    }
}

fun getDayOfWeekName(day: Int): String {
    return when(day) {
        Calendar.SUNDAY -> "Sunday"
        Calendar.MONDAY -> "Monday"
        Calendar.TUESDAY -> "Tuesday"
        Calendar.WEDNESDAY -> "Wednesday"
        Calendar.THURSDAY -> "Thursday"
        Calendar.FRIDAY -> "Friday"
        Calendar.SATURDAY -> "Saturday"
        else -> ""
    }
}

fun getWeekName(week: Int): String {
    return when(week) {
        1 -> "First"
        2 -> "Second"
        3 -> "Third"
        4 -> "Fourth"
        5 -> "Last"
        else -> ""
    }
}

fun getMonthName(month: Int): String {
    return when(month) {
        Calendar.JANUARY -> "January"
        Calendar.FEBRUARY -> "February"
        Calendar.MARCH -> "March"
        Calendar.APRIL -> "April"
        Calendar.MAY -> "May"
        Calendar.JUNE -> "June"
        Calendar.JULY -> "July"
        Calendar.AUGUST -> "August"
        Calendar.SEPTEMBER -> "September"
        Calendar.OCTOBER -> "October"
        Calendar.NOVEMBER -> "November"
        Calendar.DECEMBER -> "December"
        else -> ""
    }
}

fun parseDateString(input: String): Set<Int> {
    val result = mutableSetOf<Int>()
    val parts = input.split(",")
    for (part in parts) {
        val trimmed = part.trim()
        if (trimmed.isEmpty()) continue
        if (trimmed.contains("-")) {
            val rangeParts = trimmed.split("-")
            if (rangeParts.size == 2) {
                val start = rangeParts[0].trim().toIntOrNull()
                val end = rangeParts[1].trim().toIntOrNull()
                if (start != null && end != null && start <= end) {
                    for (i in start..end) {
                        if (i in 1..31) result.add(i)
                    }
                }
            }
        } else {
            val single = trimmed.toIntOrNull()
            if (single != null && single in 1..31) {
                result.add(single)
            }
        }
    }
    return result
}


private fun formatTime(hourOfDay: Int, minute: Int, use24HourFormat: Boolean): String {
    return if (use24HourFormat) {
        String.format("%02d:%02d", hourOfDay, minute)
    } else {
        val hour = if (hourOfDay == 0) 12 else if (hourOfDay > 12) hourOfDay - 12 else hourOfDay
        val amPm = if (hourOfDay >= 12) "PM" else "AM"
        String.format("%02d:%02d %s", hour, minute, amPm)
    }
}
