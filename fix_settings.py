import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# We need to replace the entire SettingsFeatureScreen with the new structure.
# Let's find SettingsFeatureScreen
start_idx = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SettingsFeatureScreen")
end_idx = content.find("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SettingsNotificationsScreen")

original_feature_screen = content[start_idx:end_idx]

new_feature_screen = """@OptIn(ExperimentalMaterial3Api::class)
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
                headlineContent = { Text("Daily Schedule") },
                supportingContent = { Text("Time format, missed status, task radio options") },
                leadingContent = { Icon(Icons.Default.CalendarToday, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_DAILY_SCHEDULE) }
            )
            ListItem(
                headlineContent = { Text("Reminders") },
                supportingContent = { Text("Layouts, slots, unit visibility") },
                leadingContent = { Icon(Icons.Default.Notifications, contentDescription = null) },
                modifier = Modifier.clickable { viewModel.setTimerMode(com.example.viewmodel.TimerMode.SETTINGS_REMINDERS) }
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
                headlineContent = { Text("Time Format") },
                supportingContent = { Text("24-hour format or 12 hour AM/PM format") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.AccessTime, contentDescription = null) },
                trailingContent = { 
                    Row(
                        modifier = Modifier
                            .background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(16.dp))
                            .padding(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .clickable { viewModel.setUse24HourFormat(false) }
                                .background(if (!uiState.use24HourFormat) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, RoundedCornerShape(12.dp))
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text("12", color = if (!uiState.use24HourFormat) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                        Box(
                            modifier = Modifier
                                .clickable { viewModel.setUse24HourFormat(true) }
                                .background(if (uiState.use24HourFormat) MaterialTheme.colorScheme.primary else androidx.compose.ui.graphics.Color.Transparent, RoundedCornerShape(12.dp))
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text("24", color = if (uiState.use24HourFormat) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            )
            ListItem(
                headlineContent = { Text("Default Status if Missed") },
                supportingContent = { Text("Automatically mark past tasks as this status") },
                leadingContent = { Icon(androidx.compose.material.icons.Icons.Default.Update, contentDescription = null) },
                trailingContent = {
                    androidx.compose.material3.Surface(
                        color = MaterialTheme.colorScheme.primaryContainer,
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(
                            text = uiState.autoStatusIfMissed,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            color = MaterialTheme.colorScheme.onPrimaryContainer,
                            fontWeight = FontWeight.Bold,
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
fun SettingsRemindersScreen(viewModel: MainViewModel, uiState: UiState, onBack: () -> Unit) {
    var showSlotsDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Reminders") },
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
                headlineContent = { Text("Reminders Stage Slots") },
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

"""

content = content.replace(original_feature_screen, new_feature_screen)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
