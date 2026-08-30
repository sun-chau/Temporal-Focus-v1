import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

target = """    var title by remember { mutableStateOf(draft.title) }"""
replacement = """    var showStartDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var showEndDatePicker by remember { androidx.compose.runtime.mutableStateOf(false) }
    var title by remember { mutableStateOf(draft.title) }"""
content = content.replace(target, replacement)

target1 = """                        if (isMultiDay) {
                            android.app.DatePickerDialog(
                                context,
                                { _, year, month, dayOfMonth ->
                                    val newCal = Calendar.getInstance().apply {
                                        timeInMillis = startTime
                                        set(Calendar.YEAR, year)
                                        set(Calendar.MONTH, month)
                                        set(Calendar.DAY_OF_MONTH, dayOfMonth)
                                    }
                                    val diff = endTime - startTime
                                    startTime = newCal.timeInMillis
                                    endTime = startTime + maxOf(0L, diff)
                                    timePicker.show()
                                },
                                startCal.get(Calendar.YEAR),
                                startCal.get(Calendar.MONTH),
                                startCal.get(Calendar.DAY_OF_MONTH)
                            ).show()
                        } else {
                            timePicker.show()
                        }"""

replacement1 = """                        if (isMultiDay) {
                            showStartDatePicker = true
                        } else {
                            timePicker.show()
                        }"""
content = content.replace(target1, replacement1)

target2 = """                        if (isMultiDay) {
                            android.app.DatePickerDialog(
                                context,
                                { _, year, month, dayOfMonth ->
                                    val newCal = Calendar.getInstance().apply {
                                        timeInMillis = endTime
                                        set(Calendar.YEAR, year)
                                        set(Calendar.MONTH, month)
                                        set(Calendar.DAY_OF_MONTH, dayOfMonth)
                                    }
                                    endTime = newCal.timeInMillis
                                    timePicker.show()
                                },
                                endCal.get(Calendar.YEAR),
                                endCal.get(Calendar.MONTH),
                                endCal.get(Calendar.DAY_OF_MONTH)
                            ).show()
                        } else {
                            timePicker.show()
                        }"""

replacement2 = """                        if (isMultiDay) {
                            showEndDatePicker = true
                        } else {
                            timePicker.show()
                        }"""
content = content.replace(target2, replacement2)

target3 = """    // Content
    Scaffold("""

replacement3 = """    if (showStartDatePicker) {
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = startTime,
            onDateSelected = { selectedDate ->
                val newDateCal = Calendar.getInstance().apply { timeInMillis = selectedDate }
                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
                val finalCal = Calendar.getInstance().apply {
                    timeInMillis = startTime
                    set(Calendar.YEAR, newDateCal.get(Calendar.YEAR))
                    set(Calendar.MONTH, newDateCal.get(Calendar.MONTH))
                    set(Calendar.DAY_OF_MONTH, newDateCal.get(Calendar.DAY_OF_MONTH))
                }
                val diff = endTime - startTime
                startTime = finalCal.timeInMillis
                endTime = startTime + maxOf(0L, diff)
                showStartDatePicker = false
                
                android.app.TimePickerDialog(
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
                ).show()
            },
            onDismiss = { showStartDatePicker = false }
        )
    }

    if (showEndDatePicker) {
        com.example.ui.components.UniversalDatePickerDialog(
            initialDateMillis = endTime,
            onDateSelected = { selectedDate ->
                val newDateCal = Calendar.getInstance().apply { timeInMillis = selectedDate }
                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
                val finalCal = Calendar.getInstance().apply {
                    timeInMillis = endTime
                    set(Calendar.YEAR, newDateCal.get(Calendar.YEAR))
                    set(Calendar.MONTH, newDateCal.get(Calendar.MONTH))
                    set(Calendar.DAY_OF_MONTH, newDateCal.get(Calendar.DAY_OF_MONTH))
                }
                endTime = finalCal.timeInMillis
                showEndDatePicker = false
                
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
                    uiState.use24HourFormat
                ).show()
            },
            onDismiss = { showEndDatePicker = false }
        )
    }

    // Content
    Scaffold("""
content = content.replace(target3, replacement3)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
