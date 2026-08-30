package com.example.ui.screens

import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.ui.window.Dialog
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Close
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import kotlinx.coroutines.delay
import com.example.ui.components.StatCard
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.PomodoroPhase
import com.example.viewmodel.UiState
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import androidx.compose.ui.text.withStyle



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PomodoroScreen(viewModel: MainViewModel, uiState: UiState, onMenuClick: () -> Unit) {
    var showSettingsDialog by remember { mutableStateOf(false) }
    var showInfoSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val infoSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)


    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            
            // Top Menu Row
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .windowInsetsPadding(WindowInsets.safeDrawing.only(WindowInsetsSides.Top))
                    .padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
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
                
                SystemTimeBar(use24HourFormat = uiState.use24HourFormat)
                
                IconButton(onClick = { showSettingsDialog = true }, modifier = Modifier.offset(x = 12.dp)) {
                    Icon(
                        imageVector = Icons.Default.Tune,
                        contentDescription = "Settings",
                        modifier = Modifier.size(28.dp),
                        tint = MaterialTheme.colorScheme.onSurface
                    )
                }
            }

            Spacer(modifier = Modifier.height(64.dp))
            // Main Timer Card
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(vertical = 48.dp, horizontal = 24.dp)
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally, 
                    modifier = Modifier.fillMaxWidth()
                ) {
                    val phaseColor = when (uiState.currentPhase) {
                        PomodoroPhase.FOCUS -> MaterialTheme.colorScheme.primary
                        PomodoroPhase.BREAK -> MaterialTheme.colorScheme.tertiary
                        PomodoroPhase.LONG_BREAK -> MaterialTheme.colorScheme.secondary
                    }
                    
                    // Phase indicator (Pill)
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(50))
                            .background(MaterialTheme.colorScheme.background)
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        val phaseText = when (uiState.currentPhase) {
                            PomodoroPhase.FOCUS -> "FOCUS (${uiState.currentSessionCount + 1}/${uiState.pomodoroTargetSessions})"
                            PomodoroPhase.BREAK -> "BREAK"
                            PomodoroPhase.LONG_BREAK -> "LONG BREAK"
                        }
                        Text(
                            text = phaseText,
                            color = phaseColor,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.sp
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    
                    // Massive Text Timer with Vertical Drag
                    var dragAccumulator by remember { mutableFloatStateOf(0f) }
                    val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current
                    
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .pointerInput(uiState.hasPomodoroStarted) {
                                if (!uiState.hasPomodoroStarted) {
                                    detectVerticalDragGestures(
                                    onDragStart = { dragAccumulator = 0f },
                                    onVerticalDrag = { change, dragAmount ->
                                        change.consume()
                                        // dragAmount > 0 is drag down (should decrement time)
                                        // dragAmount < 0 is drag up (should increment time)
                                        // so we negate dragAmount for accumulation
                                        dragAccumulator += -dragAmount
                                        
                                        // e.g. 15 pixels of drag = 1 minute
                                        val pixelsPerMinute = 25f 
                                        if (kotlin.math.abs(dragAccumulator) >= pixelsPerMinute) {
                                            val sign = kotlin.math.sign(dragAccumulator)
                                            val minutesDelta = sign.toInt()
                                            
                                            if (!uiState.hasPomodoroStarted) {
                                                when (uiState.currentPhase) {
                                                    PomodoroPhase.FOCUS -> viewModel.adjustBaseFocusTime(minutesDelta)
                                                    PomodoroPhase.BREAK -> viewModel.adjustBaseBreakTime(minutesDelta)
                                                    PomodoroPhase.LONG_BREAK -> viewModel.adjustLongBreakTime(minutesDelta)
                                                }
                                            }
                                            
                                            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.TextHandleMove)
                                            dragAccumulator -= sign * pixelsPerMinute
                                        }
                                    }
                                )
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        val mins = uiState.pomodoroTimeRemainingSeconds / 60
                        val secs = uiState.pomodoroTimeRemainingSeconds % 60
                        val timeString = String.format(Locale.US, "%02d:%02d", mins, secs)
                        
                        Text(
                            text = timeString,
                            color = if (uiState.isPomodoroRunning) phaseColor else phaseColor.copy(alpha = 0.15f),
                            fontSize = 110.sp,
                            fontWeight = FontWeight.Bold,
                            fontFamily = FontFamily.Monospace,
                            style = androidx.compose.ui.text.TextStyle(fontFeatureSettings = "tnum")
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(48.dp))
                    
                    // Centralized Actions
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        // Play/Pause
                        FilledIconButton(
                            onClick = { viewModel.togglePomodoroTimer() },
                            modifier = Modifier.size(72.dp),
                            colors = IconButtonDefaults.filledIconButtonColors(
                                containerColor = if (uiState.isPomodoroRunning) MaterialTheme.colorScheme.onSurface else phaseColor,
                                contentColor = if (uiState.isPomodoroRunning) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onPrimary
                            )
                        ) {
                            Icon(
                                imageVector = if (uiState.isPomodoroRunning) Icons.Default.Pause else Icons.Default.PlayArrow,
                                contentDescription = if (uiState.isPomodoroRunning) "Pause" else "Play",
                                modifier = Modifier.size(36.dp)
                            )
                        }
                    }
                }
            }

            TacticalStatsGrid(uiState, onInfoClick = { showInfoSheet = true })
            Spacer(modifier = Modifier.height(80.dp)) // space for FAB
        }
        

        if (showSettingsDialog) {
            ModalBottomSheet(
                onDismissRequest = { showSettingsDialog = false },
                sheetState = sheetState,
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp)
                        .padding(bottom = 32.dp, top = 8.dp)
                        .navigationBarsPadding()
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            if (!uiState.hasPomodoroStarted) "SETUP PHASE SETTINGS" else "LIVE SESSION CONTROLS",
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        IconButton(onClick = { showSettingsDialog = false }, modifier = Modifier.size(24.dp)) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = MaterialTheme.colorScheme.onSurface)
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    
                    if (!uiState.hasPomodoroStarted) {
                        Text(
                            "Hold +/- for rapid adjustment",
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f),
                            fontSize = 12.sp,
                            fontFamily = FontFamily.Monospace
                        )
                        Spacer(Modifier.height(24.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Base Focus", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Standard focus cycle", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustBaseFocusTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.baseFocusDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustBaseFocusTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Base Break", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Standard breather cycle", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustBaseBreakTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.baseBreakDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustBaseBreakTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Target Sessions", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("Sessions before long break", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustTargetSessions(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.pomodoroTargetSessions}", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustTargetSessions(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Long Break", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                                Text("After target sessions", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f), fontSize = 12.sp)
                            }
                            RepeatingIconButton(onClick = { viewModel.adjustLongBreakTime(-1) }) { Text("-", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                            Text("${uiState.longBreakDurationMinutes}m", color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 16.sp, modifier = Modifier.width(36.dp), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                            RepeatingIconButton(onClick = { viewModel.adjustLongBreakTime(1) }) { Text("+", color = MaterialTheme.colorScheme.onSurface, fontSize = 24.sp) }
                        }
                    } else {
                        // Live Session Controls
                        Spacer(Modifier.height(16.dp))
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            Button(onClick = { viewModel.addLiveExtraTime(-10 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-10m") }
                            Button(onClick = { viewModel.addLiveExtraTime(-5 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-5m") }
                            Button(onClick = { viewModel.addLiveExtraTime(-1 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("-1m") }
                        }
                        Spacer(Modifier.height(8.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            Button(onClick = { viewModel.addLiveExtraTime(1 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+1m") }
                            Button(onClick = { viewModel.addLiveExtraTime(5 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+5m") }
                            Button(onClick = { viewModel.addLiveExtraTime(10 * 60) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.onSurface)) { Text("+10m") }
                        }
                        
                        Spacer(Modifier.height(24.dp))
                        
                        // Undo Fail-Safe
                        val extraTimeMins = uiState.sessionExtraTimeSeconds / 60
                        val extraTimeLabel = if (extraTimeMins > 0) "+${extraTimeMins}m" else if (extraTimeMins < 0) "${extraTimeMins}m" else ""
                        
                        TextButton(
                            onClick = { viewModel.revertLiveExtraTime() },
                            enabled = uiState.sessionExtraTimeSeconds != 0L,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Revert to Original Target" + if (extraTimeLabel.isNotEmpty()) " ($extraTimeLabel)" else "")
                        }
                        
                        Spacer(Modifier.height(16.dp))
                        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                        Spacer(Modifier.height(16.dp))
                        
                        // Destructive Phase Overrides
                        OutlinedButton(
                            onClick = { 
                                viewModel.skipPomodoroPhase() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("End Early")
                        }
                        
                        Spacer(Modifier.height(8.dp))
                        
                        OutlinedButton(
                            onClick = { 
                                viewModel.resetPomodoro() 
                                showSettingsDialog = false
                            },
                            modifier = Modifier.fillMaxWidth(),
                            border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error),
                            colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("Reset Pomodoro")
                        }
                    }
                }
            }
        }
        
        if (showInfoSheet) {
            ModalBottomSheet(
                onDismissRequest = { showInfoSheet = false },
                sheetState = infoSheetState,
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp
            ) {
                TacticalInfoSheetContent()
            }
        }
    }
}

@Composable
fun RepeatingIconButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val isLongPress = remember { mutableStateOf(false) }
    
    LaunchedEffect(isPressed) {
        if (isPressed) {
            isLongPress.value = false
            delay(500)
            isLongPress.value = true
            while (true) {
                onClick()
                delay(100)
            }
        }
    }
    
    IconButton(
        onClick = {
            if (!isLongPress.value) {
                onClick()
            }
        },
        interactionSource = interactionSource,
        modifier = modifier
    ) {
        content()
    }
}


@Composable
private fun TacticalStatsGrid(uiState: com.example.viewmodel.UiState, onInfoClick: () -> Unit) {
    val currentTimeMillis = System.currentTimeMillis()
    
    // 1. ETA Math
    val pendingSessions = uiState.pomodoroTargetSessions - uiState.currentSessionCount
    val pendingFocusSeconds = if (uiState.currentPhase == com.example.viewmodel.PomodoroPhase.FOCUS) {
        maxOf(0, pendingSessions - 1) * uiState.baseFocusDurationMinutes * 60L
    } else {
        pendingSessions * uiState.baseFocusDurationMinutes * 60L
    }
    val pendingBreakSeconds = if (uiState.currentPhase == com.example.viewmodel.PomodoroPhase.BREAK) {
        maxOf(0, pendingSessions - 1) * uiState.baseBreakDurationMinutes * 60L
    } else {
        pendingSessions * uiState.baseBreakDurationMinutes * 60L
    }
    val terminalEtaMillis = currentTimeMillis + (uiState.pomodoroTimeRemainingSeconds + pendingFocusSeconds + pendingBreakSeconds) * 1000L
    val formattedTerminalEta = java.text.SimpleDateFormat(if (uiState.use24HourFormat) "HH:mm" else "hh:mm a", java.util.Locale.getDefault()).format(java.util.Date(terminalEtaMillis))

    // 2. Invested Math
    val investedMins = uiState.totalFocusTimeSeconds / 60
    val formattedInvested = String.format(java.util.Locale.US, "%02d:%02d", investedMins / 60, investedMins % 60)

    // 3. New Tactical Metrics
    val totalActiveSeconds = uiState.totalFocusTimeSeconds + uiState.totalBreakTimeSeconds
    val efficiency = if (totalActiveSeconds > 0) (uiState.totalFocusTimeSeconds.toFloat() / totalActiveSeconds * 100).toInt() else 0
    val interventions = uiState.liveAdjustmentCount

    val idealElapsed = (uiState.currentSessionCount * uiState.baseFocusDurationMinutes * 60L) + 
                       (uiState.totalBreaksTaken * uiState.baseBreakDurationMinutes * 60L)
    val actualElapsed = uiState.totalFocusTimeSeconds + uiState.totalBreakTimeSeconds
    val deviationMins = (actualElapsed - idealElapsed) / 60
    val formattedDeviation = if (deviationMins > 0) "+${deviationMins}M" else "${deviationMins}M"

    // 4. Compact Tactical Typography
    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 20.sp,
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f)
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 24.dp, bottom = 24.dp, start = 32.dp, end = 32.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("YIELD", style = textStyle)
            Text("${uiState.currentSessionCount}/${uiState.pomodoroTargetSessions}", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INVESTED", style = textStyle)
            Text(formattedInvested, style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("INTERVENTIONS", style = textStyle)
            Text("$interventions", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("EFFICIENCY", style = textStyle)
            Text("$efficiency%", style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("DEVIATION", style = textStyle)
            Text(formattedDeviation, style = textStyle)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("ETA", style = textStyle)
            Text(formattedTerminalEta, style = textStyle)
        }
        Spacer(modifier = Modifier.height(4.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
            IconButton(onClick = onInfoClick) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = "HUD Info",
                    tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f),
                    modifier = Modifier.size(24.dp)
                )
            }
        }
    }
}
@Composable
fun SystemTimeBar(use24HourFormat: Boolean) {
    var currentTime by remember { mutableLongStateOf(System.currentTimeMillis()) }
    
    LaunchedEffect(Unit) {
        while (true) {
            kotlinx.coroutines.delay(1000)
            currentTime = System.currentTimeMillis()
        }
    }
    
    val formatter = remember { java.text.SimpleDateFormat(if (use24HourFormat) "EEE, MMM d  •  HH:mm" else "EEE, MMM d  •  hh:mm a", java.util.Locale.getDefault()) }
    
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.15f))
            .padding(horizontal = 16.dp, vertical = 6.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = formatter.format(java.util.Date(currentTime)).uppercase(),
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
            fontSize = 11.sp,
            letterSpacing = 1.sp,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
        )
    }
}


@Composable
fun TacticalInfoSheetContent() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp)
            .padding(bottom = 32.dp, top = 8.dp)
            .navigationBarsPadding()
            .verticalScroll(rememberScrollState())
    ) {
        Text(
            "TACTICAL HUD METRICS",
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold
        )
        Spacer(Modifier.height(16.dp))
        
        InfoAccordionItem("YIELD", "Tracks your current session progress against your total goal.") {
            MathFraction(
                numerator = { MathText("S_{current}") },
                denominator = { MathText("S_{target}") }
            )
        }
        InfoAccordionItem("INVESTED", "The total accumulated time you have spent strictly in the focus phase.") {
            MathText("Σ t_{focus}")
        }
        InfoAccordionItem("INTERVENTIONS", "A discipline tracker measuring how many times you manually altered the timer during a live session.") {
            MathText("Σ N_{adjustments}")
        }
        InfoAccordionItem("EFFICIENCY", "Your focus-to-rest ratio expressed as a percentage.") {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("(", fontFamily = FontFamily.Serif, fontSize = 24.sp, color = MaterialTheme.colorScheme.onSurface)
                MathFraction(
                    numerator = { MathText("t_{focus}") },
                    denominator = { MathText("t_{active}") }
                )
                Text(") × 100", fontFamily = FontFamily.Serif, fontSize = 18.sp, color = MaterialTheme.colorScheme.onSurface)
            }
        }
        InfoAccordionItem("DEVIATION", "The overall schedule drift. It mathematically compares your actual elapsed time against a perfect, uninterrupted schedule.") {
            MathText("Δt = t_{actual} - t_{ideal}")
        }
        InfoAccordionItem("ETA", "The estimated real-world time your entire multi-session block will be completed.") {
            MathText("T_{eta} = T_{now} + t_{rem} + Σ t_{pending}")
        }
    }
}

@Composable
fun MathFraction(numerator: @Composable () -> Unit, denominator: @Composable () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 6.dp)) {
        numerator()
        HorizontalDivider(modifier = Modifier.padding(vertical = 4.dp).width(40.dp), color = MaterialTheme.colorScheme.onSurface, thickness = 1.dp)
        denominator()
    }
}

@Composable
fun MathText(formula: String) {
    val annotatedMath = androidx.compose.ui.text.buildAnnotatedString {
        var i = 0
        while (i < formula.length) {
            if (formula[i] == '_') {
                i++
                if (i < formula.length && formula[i] == '{') {
                    i++
                    val start = i
                    while (i < formula.length && formula[i] != '}') i++
                    val sub = formula.substring(start, i)
                    withStyle(androidx.compose.ui.text.SpanStyle(
                        baselineShift = androidx.compose.ui.text.style.BaselineShift.Subscript, 
                        fontSize = 12.sp,
                        fontStyle = androidx.compose.ui.text.font.FontStyle.Normal
                    )) {
                        append(sub)
                    }
                    if (i < formula.length) i++ // skip }
                }
            } else {
                val c = formula[i]
                if (c.isLetter() && c != 'Δ' && c != 'Σ') {
                    withStyle(androidx.compose.ui.text.SpanStyle(fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)) {
                        append(c.toString())
                    }
                } else {
                    append(c.toString())
                }
                i++
            }
        }
    }
    Text(
        text = annotatedMath,
        fontFamily = FontFamily.Serif,
        fontSize = 18.sp,
        color = MaterialTheme.colorScheme.onSurface,
        letterSpacing = 1.sp
    )
}

@Composable
fun InfoAccordionItem(title: String, description: String, formulaContent: @Composable () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Column(modifier = Modifier.fillMaxWidth().clickable { expanded = !expanded }.padding(vertical = 12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            Text(title, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Icon(
                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore, 
                contentDescription = null, 
                tint = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
            )
        }
        if (expanded) {
            Column(modifier = Modifier.padding(top = 8.dp)) {
                Text(description, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(12.dp))
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f))
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    formulaContent()
                }
                Spacer(Modifier.height(4.dp))
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
}
