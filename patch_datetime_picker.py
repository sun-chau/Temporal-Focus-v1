import re

with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun DateTimePickerDialog(\n    initialTime: Long,\n    onDismiss: () -> Unit,\n    onTimeSelected: (Long) -> Unit\n)',
    'fun DateTimePickerDialog(\n    initialTime: Long,\n    use24HourFormat: Boolean,\n    onDismiss: () -> Unit,\n    onTimeSelected: (Long) -> Unit\n)'
)

content = content.replace('is24Hour = false', 'is24Hour = use24HourFormat')

# Now add `use24HourFormat = use24HourFormat` where it's called inside `CreateChronometerOverlay`
# Wait, `CreateChronometerOverlay` already has `use24HourFormat`.
content = content.replace(
    'DateTimePickerDialog(\n            initialTime = targetTime,\n            onDismiss =',
    'DateTimePickerDialog(\n            initialTime = targetTime,\n            use24HourFormat = use24HourFormat,\n            onDismiss ='
)
content = content.replace(
    'DateTimePickerDialog(\n            initialTime = createdAt,\n            onDismiss =',
    'DateTimePickerDialog(\n            initialTime = createdAt,\n            use24HourFormat = use24HourFormat,\n            onDismiss ='
)
content = content.replace(
    'DateTimePickerDialog(\n            initialTime = deadlineDateTime ?: (targetTime - 3600000L),\n            onDismiss =',
    'DateTimePickerDialog(\n            initialTime = deadlineDateTime ?: (targetTime - 3600000L),\n            use24HourFormat = use24HourFormat,\n            onDismiss ='
)

with open('app/src/main/java/com/example/ui/screens/ChronometerScreen.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'r') as f:
    content2 = f.read()

content2 = content2.replace(
    'DateTimePickerDialog(\n            initialTime = targetTime,\n            onDismiss =',
    'DateTimePickerDialog(\n            initialTime = targetTime,\n            use24HourFormat = uiState.use24HourFormat,\n            onDismiss ='
)
content2 = content2.replace(
    'DateTimePickerDialog(\n            initialTime = createdAt,\n            onDismiss =',
    'DateTimePickerDialog(\n            initialTime = createdAt,\n            use24HourFormat = uiState.use24HourFormat,\n            onDismiss ='
)

with open('app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt', 'w') as f:
    f.write(content2)
