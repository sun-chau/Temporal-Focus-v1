import re

with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'r') as f:
    content = f.read()

rescheduling_target = """                val updatedEndCal = Calendar.getInstance().apply {
                    timeInMillis = newStartOfDay
                    set(Calendar.HOUR_OF_DAY, oldEndCal.get(Calendar.HOUR_OF_DAY))
                    set(Calendar.MINUTE, oldEndCal.get(Calendar.MINUTE))
                    if (oldEndCal.timeInMillis < oldStartCal.timeInMillis) {
                        add(Calendar.DAY_OF_YEAR, 1)
                    }
                }"""

rescheduling_replacement = """                val duration = scheduleToReschedule.endTime - scheduleToReschedule.startTime
                val updatedEndCal = Calendar.getInstance().apply {
                    timeInMillis = updatedStartCal.timeInMillis + duration
                }"""

start_picker_target = """                if (showStartTimePicker) {
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
                }"""

start_picker_replacement = """                if (showStartTimePicker) {
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
                }"""

end_picker_target = """                if (showEndTimePicker) {
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
                }"""

end_picker_replacement = """                if (showEndTimePicker) {
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
                }"""

content = content.replace(rescheduling_target, rescheduling_replacement)
content = content.replace(start_picker_target, start_picker_replacement)
content = content.replace(end_picker_target, end_picker_replacement)

with open('app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt', 'w') as f:
    f.write(content)
