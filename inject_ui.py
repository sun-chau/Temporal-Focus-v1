import re

with open("/tmp/ds_recurrence_ui.txt", "r") as f:
    lines = f.readlines()

# Clean up line numbers and extract the exact block
block_lines = []
for line in lines:
    idx = line.find('\t')
    if idx != -1:
        block_lines.append(line[idx+1:])

block = "".join(block_lines)
block = block.rstrip()
while block.endswith("}"):
    block = block[:-1].strip()

# Now block contains the UI. Let's add it to CreateChronometerScreen.kt
with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

# I need to wrap it inside the `item { ... }` since CreateChronometerScreen uses a LazyColumn.
wrapped_block = """            item {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Recurring Deadline", fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Switch(checked = isRecurring, onCheckedChange = { isRecurring = it })
                }
            }
            
            if (isRecurring) {
                item {
                    Text(text = dynamicString, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Medium)
                }
                
                item {
                    // Recurrence Count
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Number of occurrences: ", fontSize = 16.sp, modifier = Modifier.weight(1f))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                minusHolding = true
                                                tryAwaitRelease()
                                                minusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("-", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                            
                            Text(
                                text = if (occurrenceCount <= 0) "∞" else "$occurrenceCount",
                                fontWeight = FontWeight.Bold,
                                fontSize = 20.sp,
                                modifier = Modifier.widthIn(min = 40.dp),
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center
                            )
                            
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onPress = {
                                                plusHolding = true
                                                tryAwaitRelease()
                                                plusHolding = false
                                            }
                                        )
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Text("+", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
                
                item {
                    ScrollableTabRow(
                        selectedTabIndex = when (recurrenceType) {
                            RecurrenceType.DAILY -> 0
                            RecurrenceType.WEEKLY -> 1
                            RecurrenceType.MONTHLY -> 2
                            RecurrenceType.ANNUALLY -> 3
                            else -> 0
                        },
                        edgePadding = 0.dp
                    ) {
                        Tab(selected = recurrenceType == RecurrenceType.DAILY, onClick = { recurrenceType = RecurrenceType.DAILY }) { Text("Daily", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.WEEKLY, onClick = { recurrenceType = RecurrenceType.WEEKLY }) { Text("Weekly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.MONTHLY, onClick = { recurrenceType = RecurrenceType.MONTHLY }) { Text("Monthly", modifier = Modifier.padding(16.dp)) }
                        Tab(selected = recurrenceType == RecurrenceType.ANNUALLY, onClick = { recurrenceType = RecurrenceType.ANNUALLY }) { Text("Annually", modifier = Modifier.padding(16.dp)) }
                    }
                }
                
                item {
                    when (recurrenceType) {
                        RecurrenceType.DAILY -> {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                                Text("Every ", fontSize = 16.sp)
                                
                                Box(
                                    modifier = Modifier
                                        .size(48.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.surfaceVariant)
                                        .pointerInput(Unit) {
                                            detectTapGestures(
                                                onPress = {
                                                    dailyMinusHolding = true
                                                    tryAwaitRelease()
                                                    dailyMinusHolding = false
                                                }
                                            )
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("-", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                }
                                
                                Text(
                                    text = "$dailyInterval",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 20.sp,
                                    modifier = Modifier.widthIn(min = 40.dp),
                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                )
                                
                                Box(
                                    modifier = Modifier
                                        .size(48.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.surfaceVariant)
                                        .pointerInput(Unit) {
                                            detectTapGestures(
                                                onPress = {
                                                    dailyPlusHolding = true
                                                    tryAwaitRelease()
                                                    dailyPlusHolding = false
                                                }
                                            )
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("+", fontSize = 28.sp, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                }
                                
                                Text(" days", fontSize = 16.sp)
                            }
                        }
                        RecurrenceType.WEEKLY -> {
                            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                val days = listOf(
                                    java.util.Calendar.SUNDAY to "S", java.util.Calendar.MONDAY to "M",
                                    java.util.Calendar.TUESDAY to "T", java.util.Calendar.WEDNESDAY to "W",
                                    java.util.Calendar.THURSDAY to "T", java.util.Calendar.FRIDAY to "F",
                                    java.util.Calendar.SATURDAY to "S"
                                )
                                items(days) { (dayNum, dayLabel) ->
                                    val isSelected = weeklyDays.contains(dayNum)
                                    Box(
                                        modifier = Modifier
                                            .size(40.dp)
                                            .clip(CircleShape)
                                            .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                            .clickable {
                                                weeklyDays = if (isSelected) weeklyDays - dayNum else weeklyDays + dayNum
                                            },
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(dayLabel, color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                }
                            }
                        }
                        RecurrenceType.MONTHLY -> {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                var expandedType by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedType, onExpandedChange = { expandedType = it }) {
                                    OutlinedTextField(
                                        value = when(monthlyType) {
                                            com.example.data.MonthlyType.DATES -> "Select Dates"
                                            com.example.data.MonthlyType.LAST_DAY -> "Last day of month"
                                            com.example.data.MonthlyType.DAY_OF_WEEK -> "Day of the week"
                                        },
                                        onValueChange = {},
                                        readOnly = true,
                                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedType) },
                                        modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                                        DropdownMenuItem(text = { Text("Select Dates") }, onClick = { monthlyType = com.example.data.MonthlyType.DATES; expandedType = false })
                                        DropdownMenuItem(text = { Text("Last day of month") }, onClick = { monthlyType = com.example.data.MonthlyType.LAST_DAY; expandedType = false })
                                        DropdownMenuItem(text = { Text("Day of the week") }, onClick = { monthlyType = com.example.data.MonthlyType.DAY_OF_WEEK; expandedType = false })
                                    }
                                }
                                
                                if (monthlyType == com.example.data.MonthlyType.DATES) {
                                    var datesInput by remember { mutableStateOf(monthlyDates.joinToString(",")) }
                                    OutlinedTextField(
                                        value = datesInput,
                                        onValueChange = { 
                                            datesInput = it
                                            val parsed = parseDateString(it)
                                            monthlyDates = parsed
                                        },
                                        label = { Text("Dates (e.g., 1-5, 10, 15-20)") },
                                        modifier = Modifier.fillMaxWidth()
                                    )
                                } else if (monthlyType == com.example.data.MonthlyType.DAY_OF_WEEK) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        var expandedWeek by remember { mutableStateOf(false) }
                                        ExposedDropdownMenuBox(expanded = expandedWeek, onExpandedChange = { expandedWeek = it }, modifier = Modifier.weight(1f)) {
                                            OutlinedTextField(
                                                value = getWeekName(monthlyWeek),
                                                onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedWeek) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                            )
                                            ExposedDropdownMenu(expanded = expandedWeek, onDismissRequest = { expandedWeek = false }) {
                                                (1..5).forEach { w ->
                                                    DropdownMenuItem(text = { Text(getWeekName(w)) }, onClick = { monthlyWeek = w; expandedWeek = false })
                                                }
                                            }
                                        }
                                        var expandedDay by remember { mutableStateOf(false) }
                                        ExposedDropdownMenuBox(expanded = expandedDay, onExpandedChange = { expandedDay = it }, modifier = Modifier.weight(1f)) {
                                            OutlinedTextField(
                                                value = getDayOfWeekName(monthlyDayOfWeek),
                                                onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedDay) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                            )
                                            ExposedDropdownMenu(expanded = expandedDay, onDismissRequest = { expandedDay = false }) {
                                                (java.util.Calendar.SUNDAY..java.util.Calendar.SATURDAY).forEach { d ->
                                                    DropdownMenuItem(text = { Text(getDayOfWeekName(d)) }, onClick = { monthlyDayOfWeek = d; expandedDay = false })
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        RecurrenceType.ANNUALLY -> {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                var expandedMonth by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedMonth, onExpandedChange = { expandedMonth = it }) {
                                    OutlinedTextField(
                                        value = getMonthName(annuallyMonth),
                                        onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedMonth) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedMonth, onDismissRequest = { expandedMonth = false }) {
                                        (java.util.Calendar.JANUARY..java.util.Calendar.DECEMBER).forEach { m ->
                                            DropdownMenuItem(text = { Text(getMonthName(m)) }, onClick = { annuallyMonth = m; expandedMonth = false })
                                        }
                                    }
                                }
                                
                                var expandedType by remember { mutableStateOf(false) }
                                ExposedDropdownMenuBox(expanded = expandedType, onExpandedChange = { expandedType = it }) {
                                    OutlinedTextField(
                                        value = when(annuallyType) {
                                            com.example.data.AnnuallyType.DATES -> "Select Dates"
                                            com.example.data.AnnuallyType.END_OF_YEAR -> "End of year"
                                            com.example.data.AnnuallyType.DAY_OF_WEEK -> "Day of the week"
                                        },
                                        onValueChange = {},
                                        readOnly = true,
                                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedType) },
                                        modifier = Modifier.menuAnchor().fillMaxWidth()
                                    )
                                    ExposedDropdownMenu(expanded = expandedType, onDismissRequest = { expandedType = false }) {
                                        DropdownMenuItem(text = { Text("Select Dates") }, onClick = { annuallyType = com.example.data.AnnuallyType.DATES; expandedType = false })
                                        DropdownMenuItem(text = { Text("End of year") }, onClick = { annuallyType = com.example.data.AnnuallyType.END_OF_YEAR; expandedType = false })
                                        DropdownMenuItem(text = { Text("Day of the week") }, onClick = { annuallyType = com.example.data.AnnuallyType.DAY_OF_WEEK; expandedType = false })
                                    }
                                }
                                
                                if (annuallyType == com.example.data.AnnuallyType.DATES) {
                                    var datesInput by remember { mutableStateOf(annuallyDates.joinToString(",")) }
                                    OutlinedTextField(
                                        value = datesInput,
                                        onValueChange = { 
                                            datesInput = it
                                            val parsed = parseDateString(it)
                                            annuallyDates = parsed
                                        },
                                        label = { Text("Dates (e.g., 1-5, 10, 15-20)") },
                                        modifier = Modifier.fillMaxWidth()
                                    )
                                } else if (annuallyType == com.example.data.AnnuallyType.DAY_OF_WEEK) {
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        var expandedWeek by remember { mutableStateOf(false) }
                                        ExposedDropdownMenuBox(expanded = expandedWeek, onExpandedChange = { expandedWeek = it }, modifier = Modifier.weight(1f)) {
                                            OutlinedTextField(
                                                value = getWeekName(annuallyWeek),
                                                onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedWeek) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                            )
                                            ExposedDropdownMenu(expanded = expandedWeek, onDismissRequest = { expandedWeek = false }) {
                                                (1..5).forEach { w ->
                                                    DropdownMenuItem(text = { Text(getWeekName(w)) }, onClick = { annuallyWeek = w; expandedWeek = false })
                                                }
                                            }
                                        }
                                        var expandedDay by remember { mutableStateOf(false) }
                                        ExposedDropdownMenuBox(expanded = expandedDay, onExpandedChange = { expandedDay = it }, modifier = Modifier.weight(1f)) {
                                            OutlinedTextField(
                                                value = getDayOfWeekName(annuallyDayOfWeek),
                                                onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expandedDay) }, modifier = Modifier.menuAnchor().fillMaxWidth()
                                            )
                                            ExposedDropdownMenu(expanded = expandedDay, onDismissRequest = { expandedDay = false }) {
                                                (java.util.Calendar.SUNDAY..java.util.Calendar.SATURDAY).forEach { d ->
                                                    DropdownMenuItem(text = { Text(getDayOfWeekName(d)) }, onClick = { annuallyDayOfWeek = d; expandedDay = false })
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        else -> {}
                    }
                }
            }
"""

content = content + "\n" + wrapped_block + "\n        }\n    }\n}\n"

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
