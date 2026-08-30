import sys
import re

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add isMultiDay
if "var isMultiDay by remember" not in content:
    content = content.replace("var monthlyType by remember { mutableStateOf(draft.monthlyType) }", "var monthlyType by remember { mutableStateOf(draft.monthlyType) }\n    var isMultiDay by remember { mutableStateOf(false) }")

old_pickers = """            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                // Start Time
                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
                val startText = formatTime(startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        TimePickerDialog(
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
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("Start Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(startText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                }

                // End Time
                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
                val endText = formatTime(endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE), uiState.use24HourFormat)
                OutlinedCard(
                    modifier = Modifier.weight(1f).clickable {
                        TimePickerDialog(
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
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("End Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(endText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                }
            }"""

new_pickers = """            Row(
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Multi-Day Event", fontSize = 16.sp, fontWeight = FontWeight.Medium)
                androidx.compose.material3.Switch(checked = isMultiDay, onCheckedChange = { isMultiDay = it })
            }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                // Start Time
                val startCal = Calendar.getInstance().apply { timeInMillis = startTime }
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
                        }
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("Start Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(startText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                        if (isMultiDay) {
                            Text(startDateText, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                        }
                    }
                }

                // End Time
                val endCal = Calendar.getInstance().apply { timeInMillis = endTime }
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
                        }
                    }
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("End Time", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))
                        Text(endText, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                        
                        // Show "Tomorrow" or Date
                        val startDayCal = Calendar.getInstance().apply {
                            timeInMillis = startTime
                            set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0); set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
                        }
                        val endDayCal = Calendar.getInstance().apply {
                            timeInMillis = endTime
                            set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0); set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0)
                        }
                        
                        if (isMultiDay) {
                            Text(endDateText, fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                        } else if (endDayCal.timeInMillis > startDayCal.timeInMillis) {
                            Text("Tomorrow", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                        }
                    }
                }
            }"""

if old_pickers in content:
    content = content.replace(old_pickers, new_pickers)
else:
    print("Could not find old_pickers block.")
    sys.exit(1)

# Also disable save if validation fails (already endTime > startTime validation might be present? Let's check)
# It's at the top of Save button block
validation_pattern = r'''(if \(title\.isBlank\(\)\) \{\s*Toast\.makeText\(context, "Title cannot be empty", Toast\.LENGTH_SHORT\)\.show\(\)\s*return@Button\s*\})'''
content = re.sub(validation_pattern, r'\g<1>\n                    if (endTime <= startTime) {\n                        Toast.makeText(context, "End time must be after start time", Toast.LENGTH_SHORT).show()\n                        return@Button\n                    }', content)


with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)
