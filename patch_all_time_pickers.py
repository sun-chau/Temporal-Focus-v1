import re

# Patch 1: DailyScheduleScreen.kt
with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'r') as f:
    content = f.read()

target1 = """    var selectedTag by remember { mutableStateOf(initialSchedule?.tag ?: "") }"""
replacement1 = """    var selectedTag by remember { mutableStateOf(initialSchedule?.tag ?: "") }
    var showStartTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }"""
content = content.replace(target1, replacement1)

target2 = """                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        android.app.TimePickerDialog(
                            context,
                            { _, hourOfDay, minute ->
                                val newCal = Calendar.getInstance().apply {
                                    timeInMillis = startTime
                                    set(Calendar.HOUR_OF_DAY, hourOfDay)
                                    set(Calendar.MINUTE, minute)
                                }
                                startTime = newCal.timeInMillis
                            },
                            startCal.get(Calendar.HOUR_OF_DAY),
                            startCal.get(Calendar.MINUTE),
                            true
                        ).show()
                    }
                )"""

replacement2 = """                if (showStartTimePicker) {
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
                            startTime = newCal.timeInMillis
                            showStartTimePicker = false
                        },
                        onDismiss = { showStartTimePicker = false }
                    )
                }

                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        showStartTimePicker = true
                    }
                )"""
content = content.replace(target2, replacement2)


target3 = """                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        android.app.TimePickerDialog(
                            context,
                            { _, hourOfDay, minute ->
                                val newCal = Calendar.getInstance().apply {
                                    timeInMillis = endTime
                                    set(Calendar.HOUR_OF_DAY, hourOfDay)
                                    set(Calendar.MINUTE, minute)
                                }
                                endTime = newCal.timeInMillis
                            },
                            endCal.get(Calendar.HOUR_OF_DAY),
                            endCal.get(Calendar.MINUTE),
                            true
                        ).show()
                    }
                )"""

replacement3 = """                if (showEndTimePicker) {
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
                            endTime = newCal.timeInMillis
                            showEndTimePicker = false
                        },
                        onDismiss = { showEndTimePicker = false }
                    )
                }

                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        showEndTimePicker = true
                    }
                )"""
content = content.replace(target3, replacement3)

with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'w') as f:
    f.write(content)


# Patch 2: CreateDailyScheduleScreen.kt
with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

target1 = """    var showStartDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }"""
replacement1 = """    var showStartDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showStartTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndTimePicker by remember { androidx.compose.runtime.mutableStateOf(false) }"""
content = content.replace(target1, replacement1)

target2 = """                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
                val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val startDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(startCal.time)
                
                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        val timePicker = TimePickerDialog(
                            context,
                            { _, hourOfDay, minute ->
                                val newCal = Calendar.getInstance().apply {
                                    timeInMillis = startTime
                                    set(Calendar.HOUR_OF_DAY, hourOfDay)
                                    set(Calendar.MINUTE, minute)
                                }
                                val diff = endTime - startTime
                                startTime = newCal.timeInMillis
                                endTime = startTime + maxOf(0L, diff)
                            },
                            startCal.get(Calendar.HOUR_OF_DAY),
                            startCal.get(Calendar.MINUTE),
                            uiState.use24HourFormat
                        )
                        if (isMultiDay) {
                            showStartDatePicker = true
                        } else {
                            timePicker.show()
                        }
                    }
                )"""

replacement2 = """                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
                val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val startDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(startCal.time)
                
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
                )"""
content = content.replace(target2, replacement2)


target3 = """                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
                val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val endDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(endCal.time)
                
                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        val timePicker = TimePickerDialog(
                            context,
                            { _, hourOfDay, minute ->
                                val newCal = Calendar.getInstance().apply {
                                    timeInMillis = if (isMultiDay) endTime else startTime
                                    set(Calendar.HOUR_OF_DAY, hourOfDay)
                                    set(Calendar.MINUTE, minute)
                                }
                                if (!isMultiDay && newCal.timeInMillis < startTime) {
                                    newCal.add(Calendar.DAY_OF_YEAR, 1)
                                }
                                endTime = newCal.timeInMillis
                            },
                            endCal.get(Calendar.HOUR_OF_DAY),
                            endCal.get(Calendar.MINUTE),
                            uiState.use24HourFormat
                        )
                        if (isMultiDay) {
                            showEndDatePicker = true
                        } else {
                            timePicker.show()
                        }
                    }
                )"""

replacement3 = """                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
                val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                val endDateText = java.text.SimpleDateFormat("MMM dd", java.util.Locale.getDefault()).format(endCal.time)
                
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
                )"""
content = content.replace(target3, replacement3)

target4 = """                android.app.TimePickerDialog(
                    context,
                    { _, hourOfDay, minute ->
                        val newCal = Calendar.getInstance().apply {
                            timeInMillis = startTime
                            set(Calendar.HOUR_OF_DAY, hourOfDay)
                            set(Calendar.MINUTE, minute)
                        }
                        val d = endTime - startTime
                        startTime = newCal.timeInMillis
                        endTime = startTime + maxOf(0L, d)
                    },
                    startCal.get(Calendar.HOUR_OF_DAY),
                    startCal.get(Calendar.MINUTE),
                    uiState.use24HourFormat
                ).show()"""

replacement4 = """                showStartTimePicker = true"""
content = content.replace(target4, replacement4)

target5 = """                android.app.TimePickerDialog(
                    context,
                    { _, hourOfDay, minute ->
                        val newCal = Calendar.getInstance().apply {
                            timeInMillis = endTime
                            set(Calendar.HOUR_OF_DAY, hourOfDay)
                            set(Calendar.MINUTE, minute)
                        }
                        endTime = newCal.timeInMillis
                    },
                    endCal.get(Calendar.HOUR_OF_DAY),
                    endCal.get(Calendar.MINUTE),
                    uiState.use24HourFormat
                ).show()"""

replacement5 = """                showEndTimePicker = true"""
content = content.replace(target5, replacement5)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)


# Patch 3: ChronometerScreen.kt
with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'r') as f:
    content = f.read()

target_chrono1 = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateTimePickerDialog(
    initialTime: Long,
    onDismiss: () -> Unit,
    onTimeSelected: (Long) -> Unit
) {
    var showTimePicker by remember { mutableStateOf(false) }
    var selectedDateMillis by remember { mutableStateOf(initialTime) }

    val initialCal = java.util.Calendar.getInstance().apply { timeInMillis = initialTime }
    val timePickerState = rememberTimePickerState(
        initialHour = initialCal.get(java.util.Calendar.HOUR_OF_DAY),
        initialMinute = initialCal.get(java.util.Calendar.MINUTE),
        is24Hour = false
    )

    if (showTimePicker) {
        AlertDialog(
            onDismissRequest = onDismiss,
            title = { Text("Select Time") },
            text = { TimePicker(state = timePickerState) },
            confirmButton = {
                TextButton(onClick = {
                    val finalCal = java.util.Calendar.getInstance().apply { timeInMillis = selectedDateMillis }
                    finalCal.set(java.util.Calendar.HOUR_OF_DAY, timePickerState.hour)
                    finalCal.set(java.util.Calendar.MINUTE, timePickerState.minute)
                    onTimeSelected(finalCal.timeInMillis)
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
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = initialTime,
            onDateSelected = { selected ->
                selectedDateMillis = selected
                showTimePicker = true
            },
            onDismiss = onDismiss
        )
    }
}"""

replacement_chrono1 = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateTimePickerDialog(
    initialTime: Long,
    is24Hour: Boolean,
    onDismiss: () -> Unit,
    onTimeSelected: (Long) -> Unit
) {
    var showTimePicker by remember { mutableStateOf(false) }
    var selectedDateMillis by remember { mutableStateOf(initialTime) }

    if (showTimePicker) {
        val initialCal = java.util.Calendar.getInstance().apply { timeInMillis = initialTime }
        com.example.ui.components.UniversalTimePickerDialog(
            initialHour = initialCal.get(java.util.Calendar.HOUR_OF_DAY),
            initialMinute = initialCal.get(java.util.Calendar.MINUTE),
            is24Hour = is24Hour,
            onTimeSelected = { hourOfDay, minute ->
                val finalCal = java.util.Calendar.getInstance().apply { timeInMillis = selectedDateMillis }
                finalCal.set(java.util.Calendar.HOUR_OF_DAY, hourOfDay)
                finalCal.set(java.util.Calendar.MINUTE, minute)
                onTimeSelected(finalCal.timeInMillis)
            },
            onDismiss = onDismiss
        )
    } else {
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = initialTime,
            onDateSelected = { selected ->
                selectedDateMillis = selected
                showTimePicker = true
            },
            onDismiss = onDismiss
        )
    }
}"""

content = content.replace(target_chrono1, replacement_chrono1)

target_chrono2 = """    if (showTargetPicker) {
        DateTimePickerDialog(
            initialTime = targetTime,
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
            onDismiss = { showCreatedPicker = false },
            onTimeSelected = { 
                createdAt = it
                showCreatedPicker = false
            }
        )
    }

    if (showCustomReminderPicker) {
        DateTimePickerDialog(
            initialTime = reminderDateTime ?: (targetTime - 3600000L),
            onDismiss = { showCustomReminderPicker = false },
            onTimeSelected = { 
                if (it > targetTime) {
                    android.widget.Toast.makeText(context, "Reminder cannot be after target", android.widget.Toast.LENGTH_SHORT).show()
                } else {
                    reminderDateTime = it
                }
                showCustomReminderPicker = false
            }
        )
    }"""

replacement_chrono2 = """    if (showTargetPicker) {
        DateTimePickerDialog(
            initialTime = targetTime,
            is24Hour = uiState.use24HourFormat,
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
            is24Hour = uiState.use24HourFormat,
            onDismiss = { showCreatedPicker = false },
            onTimeSelected = { 
                createdAt = it
                showCreatedPicker = false
            }
        )
    }

    if (showCustomReminderPicker) {
        DateTimePickerDialog(
            initialTime = reminderDateTime ?: (targetTime - 3600000L),
            is24Hour = uiState.use24HourFormat,
            onDismiss = { showCustomReminderPicker = false },
            onTimeSelected = { 
                if (it > targetTime) {
                    android.widget.Toast.makeText(context, "Reminder cannot be after target", android.widget.Toast.LENGTH_SHORT).show()
                } else {
                    reminderDateTime = it
                }
                showCustomReminderPicker = false
            }
        )
    }"""
content = content.replace(target_chrono2, replacement_chrono2)

with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'w') as f:
    f.write(content)

