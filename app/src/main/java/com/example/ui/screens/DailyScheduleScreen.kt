@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
package com.example.ui.screens
import androidx.compose.runtime.getValue

import androidx.compose.ui.tooling.preview.Preview

import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.pointer.PointerInputChange
import androidx.compose.ui.input.pointer.positionChange
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.awaitLongPressOrCancellation
import androidx.compose.foundation.gestures.drag
import kotlinx.coroutines.CancellationException



import android.app.DatePickerDialog
import android.widget.Toast
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.PagerState
import androidx.compose.foundation.pager.PageSize
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Today
import androidx.compose.material.icons.filled.LocationSearching
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Cancel
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.FastForward
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.outlined.DateRange
import androidx.compose.material.icons.outlined.RadioButtonUnchecked
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind

import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.DailyScheduleTask
import com.example.data.ScheduleStatus
import com.example.ui.utils.getLabelColor
import com.example.ui.utils.getLabelName
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.Calendar

fun getStartOfDayMillis(timeMillis: Long): Long {
    val cal = Calendar.getInstance()
    cal.timeInMillis = timeMillis
    cal.set(Calendar.HOUR_OF_DAY, 0)
    cal.set(Calendar.MINUTE, 0)
    cal.set(Calendar.SECOND, 0)
    cal.set(Calendar.MILLISECOND, 0)
    return cal.timeInMillis
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DailyScheduleScreen(viewModel: MainViewModel, uiState: UiState, onMenuClick: () -> Unit) {
    val coroutineScope = rememberCoroutineScope()
    val pagerState = rememberPagerState(initialPage = 50000, pageCount = { 100000 })
    val anchorDateMillis = remember { getStartOfDayMillis(System.currentTimeMillis()) }
    val actualTodayMillis = getStartOfDayMillis(System.currentTimeMillis())
    val actualTodayPage = 50000 + ((actualTodayMillis - anchorDateMillis) / (24 * 60 * 60 * 1000L)).toInt()
    
    val todayMillis = anchorDateMillis // Keep variable name for rest of code compatibility
    val dayOffset = pagerState.currentPage - (50000)
    val selectedDateMillis = todayMillis + dayOffset * 24 * 60 * 60 * 1000L
    
        var showDatePicker by remember { mutableStateOf(false) }
    var isNowLineVisible by remember { mutableStateOf(true) }
    var reschedulingSchedule by remember { mutableStateOf<DailyScheduleTask?>(null) }
    val context = LocalContext.current
    val density = LocalDensity.current
    val configuration = LocalConfiguration.current
    val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }
    val screenWidthDp = configuration.screenWidthDp
    
            
    val haptic = LocalHapticFeedback.current
    
    // Task Drag State
    var dragTaskId by remember { mutableStateOf<String?>(null) }
    var dragStartTimeMillis by remember { mutableStateOf(0L) }
    var dragEndTimeMillis by remember { mutableStateOf(0L) }
    var dragLaneIndex by remember { mutableStateOf(0) }
    var dragOriginalLane by remember { mutableStateOf(0) }
    var isDragColliding by remember { mutableStateOf(false) }
    var accumulatedDragX by remember { mutableStateOf(0f) }
    var accumulatedDragY by remember { mutableStateOf(0f) }
    
    // Ghost Block State
    var isCreatingGhost by remember { mutableStateOf(false) }
    var ghostStartTimeMillis by remember { mutableStateOf(0L) }
    var ghostEndTimeMillis by remember { mutableStateOf(0L) }
    var ghostLaneIndex by remember { mutableStateOf(0) }
    var ghostInitialDragX by remember { mutableStateOf(0f) }
    var isGhostColliding by remember { mutableStateOf(false) }

    val todayScrollState = rememberScrollState()
    var scrollToNowTrigger by remember { mutableStateOf(0) }
    
    // Listen for scrollToNowTrigger to scroll today's scroll state
    LaunchedEffect(scrollToNowTrigger) {
        if (scrollToNowTrigger > 0) {
            val cal = Calendar.getInstance()
            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
            val xOffsetPx = with(density) { (currentMinutes * 2.0f).dp.toPx() }
            val screenWidthPx = with(density) { configuration.screenWidthDp.dp.toPx() }
            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
            todayScrollState.animateScrollTo(maxOf(0, targetScroll))
            // Also ensure we are on today's page
            pagerState.animateScrollToPage(actualTodayPage)
        }
    }

    val verticalScrollState = rememberScrollState()
    
    val isToday = selectedDateMillis == getStartOfDayMillis(System.currentTimeMillis())
    
    
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    val dateFormatted = java.text.SimpleDateFormat("MMMM d, yyyy", java.util.Locale.getDefault()).format(java.util.Date(selectedDateMillis))
                    Text(dateFormatted) 
                },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                },
                actions = {
                    IconButton(onClick = { showDatePicker = true }) {
                        Icon(Icons.Default.DateRange, contentDescription = "Calendar")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                    titleContentColor = MaterialTheme.colorScheme.onBackground
                )
            )
        },
        floatingActionButton = {
            Column(horizontalAlignment = Alignment.End, verticalArrangement = Arrangement.spacedBy(16.dp)) {
                androidx.compose.animation.AnimatedVisibility(
                    visible = !isNowLineVisible || pagerState.currentPage != actualTodayPage,
                    enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.scaleIn(),
                    exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.scaleOut()
                ) {
                    androidx.compose.material3.SmallFloatingActionButton(
                        onClick = { 
                            // We can't scroll to a specific pixel in HorizontalPager directly if it snaps, 
                            // but we can scroll to the page. 
                            coroutineScope.launch {
                                scrollToNowTrigger++
                            }
                        },
                        containerColor = MaterialTheme.colorScheme.primary,
                        contentColor = MaterialTheme.colorScheme.background
                    ) {
                        Icon(androidx.compose.material.icons.Icons.Default.Today, contentDescription = "Now")
                    }
                }
                FloatingActionButton(onClick = { 
                    viewModel.clearDailyScheduleDraft()
                    viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                }, containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.background) {
                    Icon(Icons.Default.Add, contentDescription = "Add Schedule")
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        Column(modifier = Modifier.padding(padding).fillMaxSize()) {
            // Header: Date Navigator
            DateNavigator(pagerState, todayMillis, coroutineScope, actualTodayPage)
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Body: Daily Agenda View (2D Canvas)
            val startOfDay = selectedDateMillis
            val endOfDay = selectedDateMillis + 24 * 60 * 60 * 1000L - 1L

            val schedulesForDate = uiState.dailySchedules.filter {
                it.startTime <= endOfDay && it.endTime > startOfDay
            }.sortedBy { it.startTime }
            


            
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    
        ) {
            
                
                HorizontalPager(
                    state = pagerState,
                    modifier = Modifier.fillMaxSize()
                ) { page ->
                    val pageDayOffset = page - (50000)
                    val pageDateMillis = todayMillis + pageDayOffset * 24 * 60 * 60 * 1000L
                    val startOfDay = pageDateMillis
                    val endOfDay = pageDateMillis + 24 * 60 * 60 * 1000L - 1L
                    val schedulesForDate = uiState.dailySchedules.filter {
                        it.startTime <= endOfDay && it.endTime > startOfDay
                    }.sortedBy { it.startTime }
                    
                    val pageScrollState = if (page == actualTodayPage) todayScrollState else rememberScrollState()
                    
                    // Automatically scroll to current time if this is today's page (initial load)
                    LaunchedEffect(Unit) {
                        if (page == actualTodayPage && scrollToNowTrigger == 0) {
                            val cal = Calendar.getInstance()
                            val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                            val xOffsetPx = with(density) { (currentMinutes * 2.0f).dp.toPx() }
                            val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                            pageScrollState.scrollTo(maxOf(0, targetScroll))
                        }
                    }
                    
                    
                    Box(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {
                // Timeline Ruler
                androidx.compose.foundation.layout.Box(modifier = Modifier) {
                    TimelineRuler(uiState.use24HourFormat)
                }
                

                   
                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .padding(top = 32.dp)
                        .width((24 * 60 * 2.0).dp)
                ) {
                    val viewportHeight = maxHeight
                    
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(verticalScrollState)
                    ) {
                        val requiredLanes = schedulesForDate.maxOfOrNull { it.laneIndex + 1 } ?: 0
                        val contentHeight = (requiredLanes * 80).dp
                        
                        val actualHeight = maxOf(viewportHeight, contentHeight)
                        val totalLanesToDraw = (actualHeight.value / 80).toInt() + 1
                        
                        Box(modifier = Modifier.width((24 * 60 * 2.0).dp).height(actualHeight)) {
                            TimelineGrid(totalLanesToDraw)
                        
                        for (schedule in schedulesForDate) {
                            val isDragging = dragTaskId == schedule.id
                            
                            val lane = if (isDragging) dragLaneIndex else schedule.laneIndex
                            val effectiveStartTime = if (isDragging) dragStartTimeMillis else schedule.startTime
                            val effectiveEndTime = if (isDragging) dragEndTimeMillis else schedule.endTime
                            
                            val actualStart = if (isDragging) effectiveStartTime else maxOf(startOfDay, effectiveStartTime)
                            val actualEnd = if (isDragging) effectiveEndTime else minOf(endOfDay + 1, effectiveEndTime)
                            
                            val startMinutes = if (isDragging) {
                                ((effectiveStartTime - startOfDay) / 60000L).toInt()
                            } else {
                                val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                                if (effectiveStartTime < startOfDay) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            }
                            
                            val endMinutes = if (isDragging) {
                                ((effectiveEndTime - startOfDay) / 60000L).toInt()
                            } else {
                                if (effectiveEndTime > endOfDay) 24 * 60 else {
                                    val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                                    endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                                }
                            }
                            
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            
                            val xOffset = (startMinutes * 2.0f).dp
                            val yOffset = (lane * 80 + 4).dp
                            val width = (durationMinutes * 2.0f).dp
                            
                            val isBleedLeft = effectiveStartTime < startOfDay
                            val isBleedRight = effectiveEndTime > endOfDay
                            
                            val isWarning = isDragging && isDragColliding
                            
                            val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60

                            ScheduleBlock(
                                alignTextEnd = alignTextEnd,
                                isWarning = isWarning,
                                elevation = if (isDragging) 8.dp else 0.dp,
                                isBleedLeft = isBleedLeft,
                                isBleedRight = isBleedRight,
                                schedule = if (isDragging) schedule.copy(startTime = effectiveStartTime, endTime = effectiveEndTime) else schedule,
                                coloredLabelsEnabled = uiState.coloredLabelsEnabled,
                                use24HourFormat = uiState.use24HourFormat,
                                enableRadioMenu = uiState.enableDailyScheduleRadioMenu,
                                pageDateMillis = pageDateMillis,
                                modifier = Modifier
                                    .offset(x = xOffset, y = yOffset)
                                    .height(72.dp)
                                    .pointerInput(schedule.id) {
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { _ ->
                                                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                                dragTaskId = schedule.id
                                                dragStartTimeMillis = schedule.startTime
                                                dragEndTimeMillis = schedule.endTime
                                                dragLaneIndex = schedule.laneIndex
                                                dragOriginalLane = schedule.laneIndex
                                                accumulatedDragX = 0f
                                                accumulatedDragY = 0f
                                                isDragColliding = false
                                            },
                                            onDrag = { change, dragAmount ->
                                                change.consume()
                                                accumulatedDragX += dragAmount.x
                                                accumulatedDragY += dragAmount.y
                                                
                                                val pxPerMinute = 2.0f * density.density
                                                val dragMinutes = (accumulatedDragX / pxPerMinute).toInt()
                                                val snappedDragMinutes = kotlin.math.round(dragMinutes / 5f).toInt() * 5
                                                
                                                dragStartTimeMillis = schedule.startTime + snappedDragMinutes * 60000L
                                                dragEndTimeMillis = schedule.endTime + snappedDragMinutes * 60000L
                                                
                                                val laneHeightPx = 80.dp.toPx()
                                                val dragLanes = kotlin.math.round(accumulatedDragY / laneHeightPx).toInt()
                                                dragLaneIndex = maxOf(0, dragOriginalLane + dragLanes)
                                                
                                                isDragColliding = schedulesForDate.any { 
                                                    it.id != schedule.id && 
                                                    it.laneIndex == dragLaneIndex && 
                                                    it.startTime < dragEndTimeMillis && 
                                                    it.endTime > dragStartTimeMillis 
                                                }
                                            },
                                            onDragEnd = {
                                                if (dragTaskId != null) {
                                                    if (isDragColliding) {
                                                        // Invalid drop
                                                    } else {
                                                        // Valid drop
                                                        val updated = schedule.copy(
                                                            startTime = dragStartTimeMillis,
                                                            endTime = dragEndTimeMillis,
                                                            laneIndex = dragLaneIndex,
                                                            seriesId = null,
                                                            recurrenceType = null,
                                                            seriesEndDate = null
                                                        )
                                                        viewModel.updateDailySchedule(updated)
                                                    }
                                                    dragTaskId = null
                                                }
                                            },
                                            onDragCancel = {
                                                dragTaskId = null
                                            }
                                        )
                                    },
                                blockWidth = width,
                                onClick = {
                                    val recType = try { if (schedule.recurrenceType != null) com.example.data.RecurrenceType.valueOf(schedule.recurrenceType) else com.example.data.RecurrenceType.DAILY } catch(e: Exception) { com.example.data.RecurrenceType.DAILY }
                                    viewModel.updateDailyScheduleDraft(
                                        com.example.data.DailyScheduleDraft(
                                            title = schedule.title,
                                            startTime = schedule.startTime,
                                            endTime = schedule.endTime,
                                            label = schedule.label,
                                            editingId = schedule.id,
                                            seriesId = schedule.seriesId,
                                            isRecurring = schedule.seriesId != null,
                                            recurrenceType = recType
                                        )
                                    )
                                    viewModel.setTimerMode(com.example.viewmodel.TimerMode.CREATE_DAILY_SCHEDULE)
                                },
                                onStatusChange = { newStatus ->
                                    viewModel.updateDailySchedule(schedule.copy(status = newStatus.name, isFinished = (newStatus == ScheduleStatus.COMPLETED || newStatus == ScheduleStatus.SKIPPED || newStatus == ScheduleStatus.DROPPED)))
                                },
                                onReschedule = {
                                    reschedulingSchedule = schedule
                                }
                            )
                        }
                        

                        if (isCreatingGhost) {
                            val startMinutes = ((ghostStartTimeMillis - startOfDay) / 60000L).toInt()
                            val endMinutes = ((ghostEndTimeMillis - startOfDay) / 60000L).toInt()
                            val durationMinutes = maxOf(10, endMinutes - startMinutes)
                            val startCal = Calendar.getInstance().apply { timeInMillis = ghostStartTimeMillis }
                            val ghostXOffset = (startMinutes * 2.0f).dp
                            val ghostYOffset = (ghostLaneIndex * 80 + 4).dp
                            val ghostWidth = (durationMinutes * 2.0f).dp
                            
                            val isWarning = isGhostColliding
                            val borderColor = if (isWarning) Color.Red else MaterialTheme.colorScheme.primary
                            val bgColor = if (isWarning) Color.Red.copy(alpha = 0.3f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.1f)
                            
                            Box(
                                modifier = Modifier
                                    .offset(x = ghostXOffset, y = ghostYOffset)
                                    .width(ghostWidth)
                                    .height(72.dp)
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(bgColor)
                                    .drawBehind {
                                        val stroke = androidx.compose.ui.graphics.drawscope.Stroke(
                                            width = 2.dp.toPx(),
                                            pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                                        )
                                        drawRoundRect(
                                            color = borderColor,
                                            style = stroke,
                                            cornerRadius = androidx.compose.ui.geometry.CornerRadius(8.dp.toPx(), 8.dp.toPx())
                                        )
                                    }
                            
                            ) {
                                val startStr = getSemanticTime(ghostStartTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                val endStr = getSemanticTime(ghostEndTimeMillis, pageDateMillis, uiState.use24HourFormat)
                                androidx.compose.material3.Text(
                                    text = "$startStr - $endStr",
                                    color = if (isWarning) androidx.compose.ui.graphics.Color.Red else androidx.compose.material3.MaterialTheme.colorScheme.primary,
                                    style = androidx.compose.material3.MaterialTheme.typography.labelSmall,
                                    modifier = androidx.compose.ui.Modifier.align(androidx.compose.ui.Alignment.Center)
                                )
                            }
                        }
                    }
                }
                
                val outlineColor = androidx.compose.material3.MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
                // Boundary lines
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxHeight()
                        .width(2.dp)
                        .align(androidx.compose.ui.Alignment.CenterStart)
                        .drawBehind {
                            drawLine(
                                color = outlineColor,
                                start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                strokeWidth = 2.dp.toPx(),
                                pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                            )
                        }
                )
                
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .fillMaxHeight()
                        .width(2.dp)
                        .align(androidx.compose.ui.Alignment.CenterEnd)
                        .drawBehind {
                            drawLine(
                                color = outlineColor,
                                start = androidx.compose.ui.geometry.Offset(0f, 0f),
                                end = androidx.compose.ui.geometry.Offset(0f, size.height),
                                strokeWidth = 2.dp.toPx(),
                                pathEffect = androidx.compose.ui.graphics.PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
                            )
                        }
                )
                
            }
            
            // Current Time Indicator
            if (page == actualTodayPage) {
                val cal = java.util.Calendar.getInstance()
                val currentMinutes = cal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + cal.get(java.util.Calendar.MINUTE)
                val xOffset = (currentMinutes * 2.0f).dp
                
                androidx.compose.foundation.layout.Box(
                    modifier = androidx.compose.ui.Modifier
                        .offset(x = xOffset)
                        .width(2.dp)
                        .fillMaxHeight()
                        .background(androidx.compose.ui.graphics.Color.Red)
                        .onGloballyPositioned { coordinates ->
                            val windowBounds = coordinates.boundsInWindow()
                            isNowLineVisible = windowBounds.right > 0 && windowBounds.left < screenWidthPx
                        }
                )
            }
            
        }
    }
    }
    }
    }
    if (showDatePicker) {
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = selectedDateMillis,
            onDateSelected = { newMillis ->
                val daysDiff = ((newMillis - todayMillis) / (24 * 60 * 60 * 1000L)).toInt()
                val targetPage = (50000) + daysDiff
                coroutineScope.launch {
                    pagerState.animateScrollToPage(targetPage)
                }
                showDatePicker = false
            },
            onDismiss = {
                showDatePicker = false
            }
        )
    }

    if (reschedulingSchedule != null) {
        val scheduleToReschedule = reschedulingSchedule!!
        
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = scheduleToReschedule.startTime,
            onDateSelected = { newStartOfDay ->
                val oldStartCal = Calendar.getInstance().apply { timeInMillis = scheduleToReschedule.startTime }
                val oldEndCal = Calendar.getInstance().apply { timeInMillis = scheduleToReschedule.endTime }
                
                val updatedStartCal = Calendar.getInstance().apply {
                    timeInMillis = newStartOfDay
                    set(Calendar.HOUR_OF_DAY, oldStartCal.get(Calendar.HOUR_OF_DAY))
                    set(Calendar.MINUTE, oldStartCal.get(Calendar.MINUTE))
                }
                
                val duration = scheduleToReschedule.endTime - scheduleToReschedule.startTime
                val updatedEndCal = Calendar.getInstance().apply {
                    timeInMillis = updatedStartCal.timeInMillis + duration
                }
                
                viewModel.updateDailySchedule(
                    scheduleToReschedule.copy(
                        startTime = updatedStartCal.timeInMillis,
                        endTime = updatedEndCal.timeInMillis,
                        seriesId = null,
                        recurrenceType = null,
                        seriesEndDate = null
                    )
                )
                reschedulingSchedule = null
            },
            onDismiss = {
                reschedulingSchedule = null
            }
        )
    }
}

@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
@Composable
fun DateNavigator(pagerState: PagerState, todayMillis: Long, coroutineScope: kotlinx.coroutines.CoroutineScope, actualTodayPage: Int) {
    val listState = rememberLazyListState()
    
    val configuration = androidx.compose.ui.platform.LocalConfiguration.current
    val screenWidth = configuration.screenWidthDp
    val itemWidth = 56 // dp
    val spacing = 8 // dp
    val centerOffsetPx = with(androidx.compose.ui.platform.LocalDensity.current) {
        ((screenWidth / 2f) - (itemWidth / 2f)).dp.toPx().toInt()
    }

    var isFirstLaunch by remember { mutableStateOf(true) }

    // Scroll to center when pagerState.currentPage changes
    LaunchedEffect(pagerState.currentPage) {
        val startOffset = -500
        val targetIndex = pagerState.currentPage - (50000) - startOffset
        if (targetIndex in 0..1000) {
            if (isFirstLaunch) {
                listState.scrollToItem(
                    index = targetIndex,
                    scrollOffset = -centerOffsetPx
                )
                isFirstLaunch = false
            } else {
                listState.animateScrollToItem(
                    index = targetIndex,
                    scrollOffset = -centerOffsetPx
                )
            }
        }
    }
    
    LazyRow(
        state = listState,
        modifier = Modifier.fillMaxWidth(),
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Just generate a window of -14 to +14 days around the current page
        // Wait, if it's infinite, why restrict to 14? We can just use an infinite LazyRow or a large range.
        // For simplicity, let's just make it a large range or centered around the current page.
        // Actually, let's use a large range like 1000 days.
        val startOffset = -500
        val totalItems = 1000
        
        items(totalItems) { index ->
            val dayOffset = startOffset + index
            val dateMillis = todayMillis + dayOffset * 24 * 60 * 60 * 1000L
            val cal = Calendar.getInstance().apply { timeInMillis = dateMillis }
            val dayOfWeek = when (cal.get(Calendar.DAY_OF_WEEK)) {
                Calendar.SUNDAY -> "Sun"
                Calendar.MONDAY -> "Mon"
                Calendar.TUESDAY -> "Tue"
                Calendar.WEDNESDAY -> "Wed"
                Calendar.THURSDAY -> "Thu"
                Calendar.FRIDAY -> "Fri"
                Calendar.SATURDAY -> "Sat"
                else -> ""
            }
            val dayOfMonth = cal.get(Calendar.DAY_OF_MONTH).toString()
            val monthStr = when (cal.get(Calendar.MONTH)) {
                Calendar.JANUARY -> "Jan"
                Calendar.FEBRUARY -> "Feb"
                Calendar.MARCH -> "Mar"
                Calendar.APRIL -> "Apr"
                Calendar.MAY -> "May"
                Calendar.JUNE -> "Jun"
                Calendar.JULY -> "Jul"
                Calendar.AUGUST -> "Aug"
                Calendar.SEPTEMBER -> "Sep"
                Calendar.OCTOBER -> "Oct"
                Calendar.NOVEMBER -> "Nov"
                Calendar.DECEMBER -> "Dec"
                else -> ""
            }
            
            val absolutePage = (50000) + dayOffset
            val isSelected = pagerState.currentPage == absolutePage
            val isToday = absolutePage == actualTodayPage
            
            Column(
                modifier = Modifier
                    .width(56.dp)
                    .height(84.dp)
                    .clip(RoundedCornerShape(32.dp))
                    .background(
                        if (isSelected) MaterialTheme.colorScheme.primary 
                        else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    )
                    .border(
                        if (isToday && !isSelected) BorderStroke(1.dp, MaterialTheme.colorScheme.primary) 
                        else BorderStroke(0.dp, Color.Transparent),
                        RoundedCornerShape(32.dp)
                    )
                    .clickable { 
                        coroutineScope.launch {
                            pagerState.animateScrollToPage(absolutePage)
                        }
                    },
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = monthStr,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfMonth,
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = dayOfWeek,
                    style = MaterialTheme.typography.labelSmall,
                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}


@Composable
fun TimelineRuler(use24HourFormat: Boolean) {
    val totalMinutes = 24 * 60
    val totalWidth = (totalMinutes * 2.0).dp
    
    Box(
        modifier = Modifier
            .width(totalWidth)
            .height(32.dp)
            .background(MaterialTheme.colorScheme.surface)
    ) {
        for (hour in 0..24) {
            val offset = (hour * 60 * 2.0).dp
            // Major tick
            Box(
                modifier = Modifier
                    .offset(x = offset)
                    .width(2.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f))
            )
            // Label
            if (hour < 24) {
                Text(
                    text = formatTime(hour, 0, use24HourFormat),
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                    modifier = Modifier.offset(x = offset + 4.dp, y = 2.dp)
                )
            }
            
            // Minor tick at 30 min
            if (hour < 24) {
                val minorOffset = offset + (30 * 2.0).dp
                Box(
                    modifier = Modifier
                        .offset(x = minorOffset)
                        .width(1.dp)
                        .fillMaxHeight(0.5f)
                        .align(Alignment.BottomStart)
                        .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f))
                )
            }
        }
    }
}

@Composable
fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 2.0).dp
        // Major tick line (thicker)
        Box(
            modifier = Modifier
                .offset(x = offset)
                .width(2.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f))
        )
        // Minor tick line (thinner)
        if (hour < 24) {
            val minorOffset = offset + (30 * 2.0).dp
            Box(
                modifier = Modifier
                    .offset(x = minorOffset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
            )
        }
    }
    
    // Horizontal lanes dividers
    for (lane in 0..totalLanes) {
        val offset = (lane * 80).dp
        Box(
            modifier = Modifier
                .offset(y = offset)
                .fillMaxWidth()
                .height(1.dp)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
        )
    }
}

@Composable
fun NowLine(modifier: Modifier = Modifier) {
    var currentTime by remember { mutableStateOf(System.currentTimeMillis()) }
    
    LaunchedEffect(Unit) {
        while(true) {
            delay(60000)
            currentTime = System.currentTimeMillis()
        }
    }
    
    val cal = Calendar.getInstance().apply { timeInMillis = currentTime }
    val minutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
    val xOffset = (minutes * 2.0f).dp
    
    Box(
        modifier = modifier
            .offset(x = xOffset)
            .width(2.dp)
            .fillMaxHeight()
            .background(Color.Red)
    )
}

@Composable
fun ScheduleBlock(
    alignTextEnd: Boolean = false,
    schedule: DailyScheduleTask,
    coloredLabelsEnabled: Boolean,
    use24HourFormat: Boolean,
    enableRadioMenu: Boolean = true,
    isBleedLeft: Boolean,
    isBleedRight: Boolean,
    isWarning: Boolean = false,
    elevation: androidx.compose.ui.unit.Dp = 0.dp,
    modifier: Modifier,
    blockWidth: androidx.compose.ui.unit.Dp,
    pageDateMillis: Long,
    onClick: () -> Unit,
    onStatusChange: (ScheduleStatus) -> Unit,
    onReschedule: () -> Unit
) {
    val isUncategorized = schedule.label.isBlank()
    val baseTagColor = getLabelColor(schedule.label, coloredLabelsEnabled)
    val tagColor = if (baseTagColor != Color.Transparent) baseTagColor else androidx.compose.material3.MaterialTheme.colorScheme.primary
    var showStatusMenu by remember { mutableStateOf(false) }
    
    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = getSemanticTime(schedule.startTime, pageDateMillis, use24HourFormat)
    val endStr = getSemanticTime(schedule.endTime, pageDateMillis, use24HourFormat)
    
    val status = try { ScheduleStatus.valueOf(schedule.status) } catch (e: Exception) { ScheduleStatus.NOT_DONE }
    
    val onSurfaceColor = MaterialTheme.colorScheme.onSurface
    
    val targetBorderColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else if (isUncategorized) {
        onSurfaceColor
    } else {
        val borderOpacity = if (status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.4f else 1.0f
        tagColor.copy(alpha = borderOpacity)
    }

    val targetBackgroundColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray.copy(alpha = 0.20f)
    } else if (isUncategorized) {
        onSurfaceColor.copy(alpha = 0.03f)
    } else {
        val bgOpacity = if (status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.08f else 0.20f
        tagColor.copy(alpha = bgOpacity)
    }

    val targetTextColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else {
        onSurfaceColor
    }
    
    val targetSubTextColor = if (status == ScheduleStatus.COMPLETED) {
        Color.Gray
    } else {
        MaterialTheme.colorScheme.onSurfaceVariant
    }

    val blockBorderColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetBorderColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "blockBorderColor"
    )
    val blockBackgroundColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetBackgroundColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "blockBackgroundColor"
    )
    val textColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetTextColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "textColor"
    )
    val subTextColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetSubTextColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "subTextColor"
    )
    
    val targetIconBorderColor = if (status == ScheduleStatus.COMPLETED && isUncategorized) {
        Color.Gray
    } else if (isUncategorized) {
        onSurfaceColor
    } else {
        Color.Transparent
    }
    
    val iconBorderColor by androidx.compose.animation.animateColorAsState(
        targetValue = targetIconBorderColor,
        animationSpec = androidx.compose.animation.core.tween(durationMillis = 200),
        label = "iconBorderColor"
    )

    val blockBorderWidth = if (isUncategorized) 3.dp else 2.dp

    val shape = RoundedCornerShape(
        topStart = if (isBleedLeft) 0.dp else 8.dp,
        bottomStart = if (isBleedLeft) 0.dp else 8.dp,
        topEnd = if (isBleedRight) 0.dp else 8.dp,
        bottomEnd = if (isBleedRight) 0.dp else 8.dp
    )
    Box(
        modifier = modifier.shadow(elevation, shape, clip = false)
    ) {
        
        Box(
            modifier = Modifier
                .width(blockWidth)
                .fillMaxHeight()
                .clip(shape)
                .background(blockBackgroundColor)
                .drawBehind {
                    val stroke = androidx.compose.ui.graphics.drawscope.Stroke(blockBorderWidth.toPx())
                    val halfStroke = blockBorderWidth.toPx() / 2f
                    val cornerRadius = 8.dp.toPx()
                    
                    val path = androidx.compose.ui.graphics.Path().apply {
                        if (isBleedLeft) {
                            moveTo(0f, halfStroke)
                        } else {
                            moveTo(cornerRadius, halfStroke)
                        }
                        
                        // Top edge
                        if (isBleedRight) {
                            lineTo(size.width, halfStroke)
                        } else {
                            lineTo(size.width - cornerRadius, halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, halfStroke, size.width - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = -90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Right edge
                        if (!isBleedRight) {
                            lineTo(size.width - halfStroke, size.height - cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(size.width - 2 * cornerRadius, size.height - 2 * cornerRadius + halfStroke, size.width - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 0f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(size.width, size.height - halfStroke)
                        }
                        
                        // Bottom edge
                        if (isBleedLeft) {
                            lineTo(0f, size.height - halfStroke)
                        } else {
                            lineTo(cornerRadius, size.height - halfStroke)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, size.height - 2 * cornerRadius + halfStroke, 2 * cornerRadius - halfStroke, size.height - halfStroke),
                                startAngleDegrees = 90f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        }
                        
                        // Left edge
                        if (!isBleedLeft) {
                            lineTo(halfStroke, cornerRadius)
                            arcTo(
                                rect = androidx.compose.ui.geometry.Rect(halfStroke, halfStroke, 2 * cornerRadius - halfStroke, 2 * cornerRadius - halfStroke),
                                startAngleDegrees = 180f,
                                sweepAngleDegrees = 90f,
                                forceMoveTo = false
                            )
                        } else {
                            moveTo(0f, halfStroke)
                        }
                    }
                    drawPath(path, blockBorderColor, style = stroke)
                }
                .clickable { onClick() }
        )
        
        // Floating Label for Dragging
        if (elevation > 0.dp) {
            Box(
                modifier = Modifier
                    .offset(y = (-24).dp)
                    .align(Alignment.TopCenter)
                    .background(if (isWarning) Color.Red else MaterialTheme.colorScheme.primary, RoundedCornerShape(4.dp))
                    .padding(horizontal = 6.dp, vertical = 2.dp)
            ) {
                Text(
                    text = "$startStr - $endStr",
                    color = MaterialTheme.colorScheme.onPrimary,
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold
                )
            }
        }
        
        // Content layer (allowed to bleed horizontally)
        Row(
            modifier = Modifier
                .width(blockWidth)
                .wrapContentWidth(unbounded = true, align = if (alignTextEnd) Alignment.End else Alignment.Start)
                .fillMaxHeight()
                .padding(horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(
                modifier = Modifier
                    .padding(end = 8.dp)
                    .clickable { onClick() },
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = schedule.title, 
                    fontWeight = FontWeight.Bold, 
                    fontSize = 15.sp, 
                    color = textColor,
                    maxLines = 1,
                    softWrap = false
                )
                if (schedule.label.isNotBlank()) {
                    Text(
                        text = getLabelName(schedule.label), 
                        fontSize = 12.sp, 
                        color = subTextColor,
                        maxLines = 1,
                        softWrap = false
                    )
                }
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = "$startStr - $endStr", 
                    fontSize = 11.sp, 
                    color = subTextColor,
                    maxLines = 1,
                    softWrap = false
                )
            }
            
            // Status Icon appended to the right of the text
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clip(CircleShape)
                    .background(if (isUncategorized) Color.Transparent else if (status == ScheduleStatus.COMPLETED) Color.Gray.copy(alpha = 0.2f) else MaterialTheme.colorScheme.surfaceVariant)
                    .then(if (isUncategorized) Modifier.border(2.dp, iconBorderColor, CircleShape) else Modifier)
                    .clickable { 
                        if (enableRadioMenu) {
                            showStatusMenu = true 
                        } else {
                            val nextStatus = if (status == ScheduleStatus.NOT_DONE) ScheduleStatus.COMPLETED else ScheduleStatus.NOT_DONE
                            onStatusChange(nextStatus)
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = when (status) {
                        ScheduleStatus.COMPLETED -> Icons.Default.CheckCircle
                        ScheduleStatus.SKIPPED -> Icons.Default.FastForward
                        ScheduleStatus.DROPPED -> Icons.Default.Cancel
                        else -> Icons.Outlined.RadioButtonUnchecked
                    },
                    contentDescription = "Status",
                    tint = textColor,
                    modifier = Modifier.size(18.dp)
                )
                
                DropdownMenu(
                    expanded = showStatusMenu,
                    onDismissRequest = { showStatusMenu = false }
                ) {
                    ScheduleStatus.values().forEach { statusOption ->
                        DropdownMenuItem(
                            text = { Text(statusOption.name) },
                            onClick = {
                                onStatusChange(statusOption)
                                showStatusMenu = false
                            }
                        )
                    }
                    androidx.compose.material3.HorizontalDivider()
                    DropdownMenuItem(
                        text = { Text("Reschedule") },
                        onClick = {
                            onReschedule()
                            showStatusMenu = false
                        }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScheduleCreateSheet(
    use24HourFormat: Boolean,
    initialSchedule: DailyScheduleTask?,
    initialDateMillis: Long,
    categories: List<String>,
    onDismiss: () -> Unit,
    onSave: (String, Long, Long, String, Set<Int>) -> Unit,
    onDelete: () -> Unit
) {
    var title by remember { mutableStateOf(initialSchedule?.title ?: "") }
    var startTime by remember { mutableStateOf(initialSchedule?.startTime ?: initialDateMillis) }
    var endTime by remember { mutableStateOf(initialSchedule?.endTime ?: (initialDateMillis + 3600000L)) }
    var recurringDays by remember { mutableStateOf(emptySet<Int>()) }
    
    
    var selectedTag by remember { mutableStateOf(initialSchedule?.label ?: "") }
    var showStartTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    val context = LocalContext.current
    
    val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
    val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), use24HourFormat)
    val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), use24HourFormat)
    
    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = if (initialSchedule != null) "Edit Schedule" else "New Schedule",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
            
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Task Title") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                // Start Time
                if (showStartTimePicker) {
                    val startCalNow = Calendar.getInstance().apply { timeInMillis = startTime }
                    com.example.ui.components.UniversalTimePickerDialog(
                        initialHour = startCalNow.get(Calendar.HOUR_OF_DAY),
                        initialMinute = startCalNow.get(Calendar.MINUTE),
                        is24Hour = use24HourFormat,
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
                        showStartTimePicker = true
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("Start Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(startText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                }
                
                // End Time
                if (showEndTimePicker) {
                    val endCalNow = Calendar.getInstance().apply { timeInMillis = endTime }
                    com.example.ui.components.UniversalTimePickerDialog(
                        initialHour = endCalNow.get(Calendar.HOUR_OF_DAY),
                        initialMinute = endCalNow.get(Calendar.MINUTE),
                        is24Hour = use24HourFormat,
                        onTimeSelected = { hourOfDay, minute ->
                            val newCal = Calendar.getInstance().apply {
                                timeInMillis = endTime
                                set(Calendar.HOUR_OF_DAY, hourOfDay)
                                set(Calendar.MINUTE, minute)
                            }
                            if (newCal.timeInMillis < startTime) {
                                newCal.add(Calendar.DAY_OF_YEAR, 1)
                            }
                            endTime = maxOf(startTime, newCal.timeInMillis)
                            showEndTimePicker = false
                        },
                        onDismiss = { showEndTimePicker = false }
                    )
                }

                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        showEndTimePicker = true
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("End Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(endText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                }
            }
            
            Text("Category Tag", fontSize = 14.sp, fontWeight = FontWeight.Medium)
            val labels = categories.ifEmpty { listOf("WORK", "STUDY", "HEALTH", "LEISURE", "CHORES") }
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                item {
                    val isNoneSelected = selectedTag.isBlank()
                    Box(
                        modifier = Modifier
                            .height(36.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isNoneSelected) MaterialTheme.colorScheme.surfaceVariant else Color.Transparent)
                            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
                            .clickable { selectedTag = "" }
                            .padding(horizontal = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Close, contentDescription = "None", modifier = Modifier.size(16.dp).padding(end = 4.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
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
            
            Spacer(modifier = Modifier.height(16.dp))
            
            if (initialSchedule == null) {
                Text("Repeat (Next 4 weeks)", fontSize = 14.sp, fontWeight = FontWeight.Medium)
                Spacer(modifier = Modifier.height(8.dp))
                val daysOfWeek = listOf(
                    Calendar.SUNDAY to "S",
                    Calendar.MONDAY to "M",
                    Calendar.TUESDAY to "T",
                    Calendar.WEDNESDAY to "W",
                    Calendar.THURSDAY to "T",
                    Calendar.FRIDAY to "F",
                    Calendar.SATURDAY to "S"
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    daysOfWeek.forEach { (dayValue, label) ->
                        val isSelected = recurringDays.contains(dayValue)
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .aspectRatio(1f)
                                .clip(CircleShape)
                                .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                .clickable { 
                                    recurringDays = if (isSelected) recurringDays - dayValue else recurringDays + dayValue
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
                Spacer(modifier = Modifier.height(16.dp))
            }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                if (initialSchedule != null) {
                    OutlinedButton(
                        onClick = onDelete,
                        modifier = Modifier.weight(1f)
                    ) {
                        Text("Delete", color = MaterialTheme.colorScheme.error)
                    }
                }
                
                Button(
                    onClick = {
                        if (title.isBlank()) {
                            Toast.makeText(context, "Title cannot be empty", Toast.LENGTH_SHORT).show()
                            return@Button
                        }
                        if (endTime <= startTime) {
                            Toast.makeText(context, "End time must be after start time", Toast.LENGTH_SHORT).show()
                            return@Button
                        }
                        onSave(title, startTime, endTime, selectedTag, recurringDays)
                    },
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Save")
                }
            }
        }
    }
}



fun getSemanticTime(timeMillis: Long, pageDateMillis: Long, use24HourFormat: Boolean): String {
    val cal = java.util.Calendar.getInstance().apply { timeInMillis = timeMillis }
    val hour = cal.get(java.util.Calendar.HOUR_OF_DAY)
    val minute = cal.get(java.util.Calendar.MINUTE)
    
    val timeOnly = formatTime(hour, minute, use24HourFormat)
    
    val timestampStartOfDay = getStartOfDayMillis(timeMillis)
    val pageStartOfDay = getStartOfDayMillis(pageDateMillis)
    
    val diffMillis = timestampStartOfDay - pageStartOfDay
    val delta = Math.round(diffMillis.toDouble() / (24 * 60 * 60 * 1000L)).toInt()
    
    return when (delta) {
        0 -> timeOnly
        -1 -> "$timeOnly Yesterday"
        1 -> "$timeOnly Tomorrow"
        else -> {
            val day = cal.get(java.util.Calendar.DAY_OF_MONTH)
            val suffix = when {
                day in 11..13 -> "th"
                day % 10 == 1 -> "st"
                day % 10 == 2 -> "nd"
                day % 10 == 3 -> "rd"
                else -> "th"
            }
            val month = cal.getDisplayName(java.util.Calendar.MONTH, java.util.Calendar.LONG, java.util.Locale.getDefault())
            "$timeOnly, ${day}${suffix} $month"
        }
    }
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


@Preview(showBackground = true, widthDp = 800, heightDp = 400)
@Composable
fun TimelineGravityPreview() {
    val mockTasks = com.example.data.MockDataGenerator.getMockTasks()
    val todayStart = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }.timeInMillis
    
    val endOfDay = todayStart + 24 * 60 * 60 * 1000L - 1L

    androidx.compose.foundation.layout.Box(modifier = Modifier.fillMaxSize().horizontalScroll(rememberScrollState())) {
        androidx.compose.foundation.layout.Box(modifier = Modifier) {
            TimelineRuler(use24HourFormat = true)
        }
        
        androidx.compose.foundation.layout.BoxWithConstraints(
            modifier = Modifier
                .fillMaxHeight()
                .width((24 * 60 * 2.0).dp)
        ) {
            val requiredLanes = mockTasks.maxOfOrNull { it.laneIndex + 1 } ?: 0
            
            TimelineGrid(totalLanes = maxOf(4, requiredLanes))
            
            mockTasks.forEach { schedule ->
                val actualStart = maxOf(todayStart, schedule.startTime)
                val actualEnd = minOf(endOfDay + 1, schedule.endTime)
                
                val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                val startMinutes = if (schedule.startTime < todayStart) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                
                val endMinutes = if (schedule.endTime > endOfDay) 24 * 60 else {
                    val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                    endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                }
                
                val durationMinutes = maxOf(10, endMinutes - startMinutes)
                
                val xOffset = (startMinutes * 2.0f).dp
                val yOffset = (schedule.laneIndex * 80 + 4).dp
                val width = (durationMinutes * 2.0f).dp
                
                val isBleedLeft = schedule.startTime < todayStart
                val isBleedRight = schedule.endTime > endOfDay
                
                val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60

                ScheduleBlock(
                    alignTextEnd = alignTextEnd,
                    isWarning = false,
                    modifier = Modifier.offset(x = xOffset, y = yOffset),
                    schedule = schedule,
                    coloredLabelsEnabled = true,
                    use24HourFormat = true,
                    enableRadioMenu = true,
                    isBleedLeft = isBleedLeft,
                    isBleedRight = isBleedRight,
                    pageDateMillis = todayStart,
                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {},
                    onReschedule = {}
                )
            }
        }
    }
}
