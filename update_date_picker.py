import re

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'r') as f:
    content = f.read()

# 1. Add UniversalDatePickerDialog import
content = content.replace(
    'import com.example.ui.components.UniversalTimePickerDialog',
    'import com.example.ui.components.UniversalTimePickerDialog\nimport com.example.ui.components.UniversalDatePickerDialog'
)

# 2. Add showDatePicker and tempDateMillis variables
content = content.replace(
    'var showTimePicker by remember { mutableStateOf(false) }',
    'var showTimePicker by remember { mutableStateOf(false) }\n    var showDatePicker by remember { mutableStateOf(false) }\n    var tempDateMillis by remember { mutableStateOf(0L) }'
)

# 3. Change icon button action
content = content.replace(
    'IconButton(onClick = { showTimePicker = true }) {',
    'IconButton(onClick = { showDatePicker = true }) {'
)

# 4. Add DatePickerDialog block and update TimePickerDialog block
old_time_picker_block = """    if (showTimePicker) {
        UniversalTimePickerDialog(
            initialHour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY),
            initialMinute = Calendar.getInstance().get(Calendar.MINUTE),
            is24Hour = true,
            onDismiss = { showTimePicker = false },
            onTimeSelected = { hour, minute ->
                val cal = Calendar.getInstance()
                cal.set(Calendar.HOUR_OF_DAY, hour)
                cal.set(Calendar.MINUTE, minute)
                cal.set(Calendar.SECOND, 0)
                cal.set(Calendar.MILLISECOND, 0)
                
                if (cal.timeInMillis < System.currentTimeMillis()) {
                    cal.add(Calendar.DAY_OF_YEAR, 1)
                }
                
                deadlineTimeMillis = cal.timeInMillis
                showTimePicker = false
                focusRequester.requestFocus()
            }
        )
    }"""

new_date_and_time_picker_blocks = """    if (showDatePicker) {
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
            is24Hour = true,
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
    }"""

content = content.replace(old_time_picker_block, new_date_and_time_picker_blocks)

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'w') as f:
    f.write(content)
