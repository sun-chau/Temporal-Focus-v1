import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

start_time_picker_target = """                if (showStartTimePicker) {"""
start_date_picker_block = """                if (showStartDatePicker) {
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
                if (showStartTimePicker) {"""

content = content.replace(start_time_picker_target, start_date_picker_block)

end_time_picker_target = """                if (showEndTimePicker) {"""
end_date_picker_block = """                if (showEndDatePicker) {
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
                if (showEndTimePicker) {"""

content = content.replace(end_time_picker_target, end_date_picker_block)

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
