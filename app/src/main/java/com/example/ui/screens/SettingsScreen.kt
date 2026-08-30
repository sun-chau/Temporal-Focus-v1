package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.clickable
import androidx.compose.foundation.background
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons

import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close

import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.example.viewmodel.MainViewModel
import com.example.viewmodel.UiState
import com.example.viewmodel.ChronometerLayout




@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Appearance & Theming") },
                supportingContent = { Text("Colors, categories, and tags") },
                leadingContent = { Icon(Icons.Default.Palette, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_APPEARANCE) }
            )
            ListItem(
                headlineContent = { Text("Feature Customisation") },
                supportingContent = { Text("Chronometer layouts, slots, visibility") },
                leadingContent = { Icon(Icons.Default.Widgets, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_FEATURE) }
            )
            ListItem(
                headlineContent = { Text("Notifications & Sounds") },
                supportingContent = { Text("Tones and vibrations") },
                leadingContent = { Icon(Icons.Default.Notifications, contentDescription = null) },
                modifier = Modifier.alpha(0.5f)
            )
            ListItem(
                headlineContent = { Text("Security & Privacy") },
                supportingContent = { Text("App password, journal lock") },
                leadingContent = { Icon(Icons.Default.Security, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SECURITY_SETTINGS) }
            )
            ListItem(
                headlineContent = { Text("Data Management") },
                supportingContent = { Text("Export, import, reset") },
                leadingContent = { Icon(Icons.Default.Storage, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_DATA) }
            )
            ListItem(
                headlineContent = { Text("Support & About") },
                supportingContent = { Text("App info, logs, feedback") },
                leadingContent = { Icon(Icons.Default.Info, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_SUPPORT) }
            )
            ListItem(
                headlineContent = { Text("Developer Mode") },
                supportingContent = { Text("Advanced tools") },
                leadingContent = { Icon(Icons.Default.Code, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.DEVELOPER_OPTIONS) }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsAppearanceScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Appearance & Theming") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Launcher Icon") },
                supportingContent = { Text("Tap to set the home screen icon color.") },
                trailingContent = { Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_LAUNCHER_ICON) }
            )
            ListItem(
                headlineContent = { Text("Theme and Color Customization") },
                supportingContent = { Text("Change the app's primary theme color") },
                trailingContent = { Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.COLOR_CUSTOMIZATION) }
            )
            ListItem(
                headlineContent = { Text("Colored Categories") },
                supportingContent = { Text("Enable dynamic colors for categories across the app") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.coloredLabelsEnabled,
                        onCheckedChange = { viewModel.toggleColoredLabelsEnabled(it) }
                    )
                }
            )
            ListItem(
                headlineContent = { Text("Colored Tags") },
                supportingContent = { Text("Enable dynamic colors for tags across the app") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.coloredLabelsEnabled,
                        onCheckedChange = { viewModel.toggleColoredLabelsEnabled(it) }
                    )
                }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsFeatureScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Feature Customisation") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            ListItem(
                headlineContent = { Text("Time Format") },
                supportingContent = { Text("24-hour format or 12 hour AM/PM format") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.AccessTime, contentDescription = null) },
                trailingContent = { 
                    Row(
                        modifier = Modifier
                            .background(MaterialTheme.colorScheme.surfaceVariant, androidx.compose.foundation.shape.RoundedCornerShape(16.dp))
                            .padding(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .clickable { viewModel.setUse24HourFormat(false) }
                                .background(if (!uiState.use24HourFormat) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text("12", color = if (!uiState.use24HourFormat) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        }
                        Box(
                            modifier = Modifier
                                .clickable { viewModel.setUse24HourFormat(true) }
                                .background(if (uiState.use24HourFormat) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text("24", color = if (uiState.use24HourFormat) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        }
                    }
                }
            )
            ListItem(
                headlineContent = { Text("Daily Schedule") },
                supportingContent = { Text("Time format, missed status, task radio options") },
                leadingContent = { Icon(Icons.Default.CalendarToday, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_DAILY_SCHEDULE) }
            )
            ListItem(
                headlineContent = { Text("Deadlines") },
                supportingContent = { Text("Layouts, slots, unit visibility") },
                leadingContent = { Icon(Icons.Default.Notifications, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_DEADLINES) }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsDailyScheduleScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var showAutoStatusDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Daily Schedule") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Default Status if Missed") },
                supportingContent = { Text("Automatically mark past tasks as this status") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.Update, contentDescription = null) },
                trailingContent = {
                    androidx.compose.material3.Surface(
                        color = MaterialTheme.colorScheme.primaryContainer,
                        shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = uiState.autoStatusIfMissed,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                            style = MaterialTheme.typography.labelMedium
                        )
                    }
                },
                modifier = Modifier.clickable { showAutoStatusDialog = true }
            )
            ListItem(
                headlineContent = { Text("Task Card Radio Menu") },
                supportingContent = { Text("Enable or disable options when you click the radio icon in task card") },
                leadingContent = { Icon(Icons.Default.RadioButtonChecked, contentDescription = null) },
                trailingContent = { ThemeSwitch(checked = uiState.enableDailyScheduleRadioMenu, onCheckedChange = { viewModel.setEnableDailyScheduleRadioMenu(it) }) }
            )
        }
    }

    if (showAutoStatusDialog) {
        AlertDialog(
            onDismissRequest = { showAutoStatusDialog = false },
            title = { Text("Status if Missed") },
            text = {
                Column {
                    listOf("NOT_DONE", "COMPLETED", "SKIPPED").forEach { status ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    viewModel.setAutoStatusIfMissed(status)
                                    showAutoStatusDialog = false
                                }
                                .padding(vertical = 12.dp)
                        ) {
                            RadioButton(
                                selected = uiState.autoStatusIfMissed == status,
                                onClick = null
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(text = status)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showAutoStatusDialog = false }) {
                    Text("Close")
                }
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsDeadlinesScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var showSlotsDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Deadlines") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Deadlines Stage Slots") },
                supportingContent = { Text("Display " + if (uiState.maxStageSlots == -1) "all" else "up to ${uiState.maxStageSlots} timers") },
                leadingContent = { Icon(Icons.Default.Layers, contentDescription = null) },
                modifier = Modifier.clickable { showSlotsDialog = true }
            )
            ListItem(
                headlineContent = { Text("Layout Preference") },
                supportingContent = { Text("Vertical or Horizontal list") },
                leadingContent = { Icon(Icons.Default.ViewList, contentDescription = null) },
                trailingContent = {
                    Row(
                        modifier = Modifier.width(140.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        UnitToggleButton(
                            text = "V",
                            selected = uiState.layoutPreference == com.example.viewmodel.ChronometerLayout.VERTICAL,
                            onToggle = { viewModel.setLayoutPreference(com.example.viewmodel.ChronometerLayout.VERTICAL) },
                            modifier = Modifier.weight(1f)
                        )
                        UnitToggleButton(
                            text = "H",
                            selected = uiState.layoutPreference == com.example.viewmodel.ChronometerLayout.HORIZONTAL,
                            onToggle = { viewModel.setLayoutPreference(com.example.viewmodel.ChronometerLayout.HORIZONTAL) },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            )
            ListItem(
                headlineContent = { Text("Unit Visibility") },
                supportingContent = { Text("Toggle display of years, months, days, etc.") },
                leadingContent = { Icon(Icons.Default.Visibility, contentDescription = null) }
            )
            
            ListItem(
                headlineContent = { Text("Years") },
                trailingContent = { ThemeSwitch(checked = uiState.showYears, onCheckedChange = { viewModel.toggleUnitVisibility("years") }) }
            )
            ListItem(
                headlineContent = { Text("Months") },
                trailingContent = { ThemeSwitch(checked = uiState.showMonths, onCheckedChange = { viewModel.toggleUnitVisibility("months") }) }
            )
            ListItem(
                headlineContent = { Text("Days") },
                trailingContent = { ThemeSwitch(checked = uiState.showDays, onCheckedChange = { viewModel.toggleUnitVisibility("days") }) }
            )
            ListItem(
                headlineContent = { Text("Hours") },
                trailingContent = { ThemeSwitch(checked = uiState.showHours, onCheckedChange = { viewModel.toggleUnitVisibility("hours") }) }
            )
            ListItem(
                headlineContent = { Text("Minutes") },
                trailingContent = { ThemeSwitch(checked = uiState.showMinutes, onCheckedChange = { viewModel.toggleUnitVisibility("minutes") }) }
            )
            ListItem(
                headlineContent = { Text("Seconds") },
                trailingContent = { ThemeSwitch(checked = uiState.showSeconds, onCheckedChange = { viewModel.toggleUnitVisibility("seconds") }) }
            )
        }
    }

    if (showSlotsDialog) {
        AlertDialog(
            onDismissRequest = { showSlotsDialog = false },
            title = { Text("Stage Slots") },
            text = {
                Column {
                    listOf(-1, 3, 5, 7, 10).forEach { slot ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    viewModel.setMaxStageSlots(slot)
                                    showSlotsDialog = false
                                }
                                .padding(vertical = 12.dp)
                        ) {
                            RadioButton(
                                selected = uiState.maxStageSlots == slot,
                                onClick = null
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(text = if (slot == -1) "Show All" else "$slot Slots")
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showSlotsDialog = false }) {
                    Text("Close")
                }
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsNotificationsScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Notifications & Sounds") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Pomodoro Phase Tone") },
                supportingContent = { Text("Play a tone when pomodoro phase changes") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.pomodoroPhaseAlerts,
                        onCheckedChange = { viewModel.togglePomodoroPhaseAlerts(it) }
                    )
                }
            )
            ListItem(
                headlineContent = { Text("Pomodoro Phase Vibration") },
                supportingContent = { Text("Vibrate when pomodoro phase changes") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.pomodoroPhaseVibrationEnabled,
                        onCheckedChange = { viewModel.togglePomodoroPhaseVibration(it) }
                    )
                }
            )
            ListItem(
                headlineContent = { Text("Deadline Tone") },
                supportingContent = { Text("Play a tone when chronometer deadline is reached") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.chronometerDeadlinesAlerts,
                        onCheckedChange = { viewModel.toggleChronometerDeadlinesAlerts(it) }
                    )
                }
            )
            ListItem(
                headlineContent = { Text("Deadline Vibration") },
                supportingContent = { Text("Vibrate when chronometer deadline is reached") },
                trailingContent = {
                    ThemeSwitch(
                        checked = uiState.chronometerDeadlineVibrationEnabled,
                        onCheckedChange = { viewModel.toggleChronometerDeadlineVibration(it) }
                    )
                }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsDataScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var showClearHistoryDialog by remember { mutableStateOf(false) }
    var showFactoryResetDialog by remember { mutableStateOf(false) }
    val clipboardManager = androidx.compose.ui.platform.LocalClipboardManager.current
    val context = androidx.compose.ui.platform.LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Data Management") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("Export Data") },
                supportingContent = { Text("Save your timers and history to a file") },
                leadingContent = { Icon(Icons.Default.Download, contentDescription = null) },
                modifier = Modifier.clickable {
                    val data = viewModel.exportData()
                    clipboardManager.setText(androidx.compose.ui.text.AnnotatedString(data))
                    android.widget.Toast.makeText(context, "Data exported to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                }
            )
            ListItem(
                headlineContent = { Text("Import Data") },
                supportingContent = { Text("Restore timers and history from a file") },
                leadingContent = { Icon(Icons.Default.Upload, contentDescription = null) },
                modifier = Modifier.clickable {
                    val text = clipboardManager.getText()?.text
                    if (text != null && text.isNotBlank()) {
                        viewModel.importData(text)
                        android.widget.Toast.makeText(context, "Data imported successfully", android.widget.Toast.LENGTH_SHORT).show()
                    } else {
                        android.widget.Toast.makeText(context, "Clipboard is empty", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            )
            ListItem(
                headlineContent = { Text("Clear History") },
                supportingContent = { Text("Delete all completed timers and pomodoro sessions") },
                leadingContent = { Icon(Icons.Default.Delete, contentDescription = null) },
                modifier = Modifier.clickable { showClearHistoryDialog = true }
            )
            ListItem(
                headlineContent = { Text("Factory Reset User Data", color = MaterialTheme.colorScheme.error) },
                supportingContent = { Text("Delete all data and settings") },
                leadingContent = { Icon(Icons.Default.Warning, contentDescription = null, tint = MaterialTheme.colorScheme.error) },
                modifier = Modifier.clickable { showFactoryResetDialog = true }
            )
        }
    }

    if (showClearHistoryDialog) {
        ModalBottomSheet(
            onDismissRequest = { showClearHistoryDialog = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text(
                    text = "Clear History",
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Are you sure you want to delete all completed timers? This action cannot be undone.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(32.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showClearHistoryDialog = false }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(
                        onClick = {
                            viewModel.clearHistory()
                            showClearHistoryDialog = false
                        }
                    ) {
                        Text("Clear", color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        }
    }

    if (showFactoryResetDialog) {
        ModalBottomSheet(
            onDismissRequest = { showFactoryResetDialog = false },
            dragHandle = null,
            shape = androidx.compose.foundation.shape.RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp)
            ) {
                Text(
                    text = "Factory Reset",
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Are you sure you want to delete all your data and settings? This action cannot be undone.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.error
                )
                Spacer(modifier = Modifier.height(32.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = { showFactoryResetDialog = false }) {
                        Text("Cancel")
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    TextButton(
                        onClick = {
                            viewModel.factoryResetUserData()
                            showFactoryResetDialog = false
                        }
                    ) {
                        Text("Reset", color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsSupportScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Support & About") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            ListItem(
                headlineContent = { Text("About") },
                supportingContent = { Text("App version and information") },
                leadingContent = { Icon(Icons.Default.Info, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_ABOUT) }
            )
            ListItem(
                headlineContent = { Text("Update Logs") },
                supportingContent = { Text("View recent changes and updates") },
                leadingContent = { Icon(Icons.Default.History, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.UPDATE_LOG) }
            )
            ListItem(
                headlineContent = { Text("Help") },
                supportingContent = { Text("View help and documentation") },
                leadingContent = { Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_HELP) }
            )
            ListItem(
                headlineContent = { Text("Feedback") },
                supportingContent = { Text("Send feedback and report issues") },
                leadingContent = { Icon(Icons.Default.Feedback, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_FEEDBACK) }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsAboutScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("About") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.Default.Info, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsHelpScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Help") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsFeedbackScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Feedback") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.Default.Feedback, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.primary)
            Spacer(modifier = Modifier.height(16.dp))
            Text("Coming Soon", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@Composable
fun SettingsCategoryHeader(title: String) {
    Text(
        text = title.uppercase(),
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
    )
}

@Composable
fun UnitToggleButton(text: String, selected: Boolean, onToggle: () -> Unit, modifier: Modifier = Modifier) {
    val containerColor = if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.2f) else androidx.compose.ui.graphics.Color.Transparent
    val contentColor = MaterialTheme.colorScheme.primary
    val borderColor = MaterialTheme.colorScheme.primary.copy(alpha = if (selected) 1f else 0.5f)
    
    Surface(
        modifier = modifier,
        shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp),
        color = containerColor,
        contentColor = contentColor,
        border = androidx.compose.foundation.BorderStroke(1.dp, borderColor),
        onClick = onToggle
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.padding(vertical = 12.dp)) {
            Text(text = text, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
        }
    }
}

@Composable
fun ThemeSwitch(
    checked: Boolean,
    onCheckedChange: ((Boolean) -> Unit)?,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) {
    androidx.compose.material3.Switch(
        checked = checked,
        onCheckedChange = onCheckedChange,
        modifier = modifier,
        enabled = enabled,
        colors = androidx.compose.material3.SwitchDefaults.colors(
            checkedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
            checkedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
            checkedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.primary,
            uncheckedThumbColor = androidx.compose.material3.MaterialTheme.colorScheme.onSurface,
            uncheckedTrackColor = androidx.compose.material3.MaterialTheme.colorScheme.surfaceVariant,
            uncheckedIconColor = androidx.compose.material3.MaterialTheme.colorScheme.surface
        ),
        thumbContent = if (checked) {
            {
                androidx.compose.material3.Icon(
                    imageVector = androidx.compose.material.icons.Icons.Filled.Check,
                    contentDescription = null,
                    modifier = Modifier.size(androidx.compose.material3.SwitchDefaults.IconSize),
                )
            }
        } else {
            {
                androidx.compose.material3.Icon(
                    imageVector = androidx.compose.material.icons.Icons.Filled.Close,
                    contentDescription = null,
                    modifier = Modifier.size(androidx.compose.material3.SwitchDefaults.IconSize),
                )
            }
        }
    )
}


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LauncherIconScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var pendingIcon by remember { mutableStateOf<String?>(null) }
    
    val themes = listOf(
        "orange" to "Baseline/Default",
        "obsidian" to "Obsidian Dark",
        "daylight" to "Daylight Clear",
        "midnight" to "Midnight Minimalist",
        "nordic" to "Nordic Frost",
        "forest" to "Forest Canopy",
        "crimson" to "Crimson Twilight",
        "amber" to "Amber Glow",
        "monochrome" to "Monochrome"
    )
    
    val icons = mapOf(
        "orange" to com.example.R.drawable.ic_launcher_foreground_orange,
        "obsidian" to com.example.R.drawable.ic_launcher_foreground_obsidian,
        "daylight" to com.example.R.drawable.ic_launcher_foreground_daylight,
        "midnight" to com.example.R.drawable.ic_launcher_foreground_midnight,
        "nordic" to com.example.R.drawable.ic_launcher_foreground_nordic,
        "forest" to com.example.R.drawable.ic_launcher_foreground_forest,
        "crimson" to com.example.R.drawable.ic_launcher_foreground_crimson,
        "amber" to com.example.R.drawable.ic_launcher_foreground_amber,
        "monochrome" to com.example.R.drawable.ic_launcher_foreground_monochrome
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Launcher Icon") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
            columns = androidx.compose.foundation.lazy.grid.GridCells.Fixed(3),
            contentPadding = PaddingValues(16.dp),
            modifier = Modifier.fillMaxSize().padding(padding)
        ) {
            items(themes.size) { index ->
                val (id, name) = themes[index]
                val isActive = uiState.launcherIcon == id
                
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .padding(8.dp)
                        .clickable {
                            if (!isActive) {
                                pendingIcon = id
                            }
                        }
                ) {
                    Box(
                        modifier = Modifier
                            .size(72.dp)
                            .background(
                                color = if (isActive) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent,
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp)
                            )
                            .padding(4.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        androidx.compose.foundation.Image(
                            painter = androidx.compose.ui.res.painterResource(id = icons[id] ?: com.example.R.drawable.ic_launcher_foreground_orange),
                            contentDescription = name,
                            modifier = Modifier.size(64.dp)
                        )
                        if (isActive) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = "Active",
                                tint = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.align(Alignment.BottomEnd).size(24.dp).background(androidx.compose.ui.graphics.Color.White, androidx.compose.foundation.shape.CircleShape)
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = name,
                        style = MaterialTheme.typography.bodySmall,
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                        maxLines = 2
                    )
                }
            }
        }
    }
    
    if (pendingIcon != null) {
        AlertDialog(
            onDismissRequest = { pendingIcon = null },
            title = { Text("Change Launcher Icon") },
            text = { Text("Changing the home screen icon will briefly restart the launcher. Are you sure you want to apply the ${themes.find { it.first == pendingIcon }?.second} icon?") },
            confirmButton = {
                TextButton(
                    onClick = {
                        val iconId = pendingIcon!!
                        pendingIcon = null
                        
                        viewModel.setLauncherIcon(iconId)
                        
                        
                        val pm = context.packageManager
                        val packageName = context.packageName
                        
                        val allAliases = listOf(
                            "MainActivityOrange",
                            "MainActivityObsidian",
                            "MainActivityDaylight",
                            "MainActivityMidnight",
                            "MainActivityNordic",
                            "MainActivityForest",
                            "MainActivityCrimson",
                            "MainActivityAmber",
                            "MainActivityMonochrome"
                        )
                        
                        val targetAlias = "MainActivity" + iconId.replaceFirstChar { it.uppercase() }
                        
                        // We must disable MainActivity if target is not orange?
                        // Wait, if target is orange, do we enable MainActivity and disable all aliases?
                        // "The application's core MainActivity starts and persists with the default Orange icon as its primary <activity> declaration... Below the main activity in the Manifest, an <activity-alias> tag must be declared for every single new icon variant listed in Section 2... Default State: Crucially, all activity aliases must have android:enabled="false" set in their initial manifest declaration."
                        // This implies orange has an alias too ("MainActivityOrange")! 
                        // Wait, Section 2 table: Baseline/Default -> @mipmap/ic_launcher_orange
                        // And Section 4 says: "all activity aliases must have android:enabled='false' set in their initial manifest declaration"
                        // That means orange alias is ALSO false initially.
                        
                        // So if we select orange, we can EITHER enable MainActivity and disable all aliases, OR disable MainActivity and enable MainActivityOrange.
                        // Let's just disable whatever was active and enable the new one.
                        
                        // Disable MainActivity to remove the default icon from launcher
                        pm.setComponentEnabledSetting(
                            android.content.ComponentName(packageName, "com.example.MainActivity"),
                            if (iconId == "orange") android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_ENABLED else android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                            android.content.pm.PackageManager.DONT_KILL_APP
                        )
                        
                        for (alias in allAliases) {
                            val componentName = android.content.ComponentName(packageName, "com.example.$alias")
                            pm.setComponentEnabledSetting(
                                componentName,
                                if (alias == targetAlias && iconId != "orange") android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_ENABLED else android.content.pm.PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                                android.content.pm.PackageManager.DONT_KILL_APP
                            )
                        }

                    }
                ) {
                    Text("Apply")
                }
            },
            dismissButton = {
                TextButton(onClick = { pendingIcon = null }) {
                    Text("Cancel")
                }
            }
        )
    }
}
