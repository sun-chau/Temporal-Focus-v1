import re

with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'r') as f:
    content = f.read()

target = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DateTimePickerDialog(
    initialTime: Long,
    onDismiss: () -> Unit,
    onTimeSelected: (Long) -> Unit
) {
    var showTimePicker by remember { mutableStateOf(false) }
    
    val datePickerState = rememberDatePickerState(initialSelectedDateMillis = initialTime)
    
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
}"""

replacement = """@OptIn(ExperimentalMaterial3Api::class)
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
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'w') as f:
    f.write(content)
