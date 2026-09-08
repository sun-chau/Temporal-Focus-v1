import re

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
    content = f.read()

# 1. Update onClick status cycling
onClick_old = """                            onClick = {
                                val newStatus = when (task.status) {
                                    AssignmentStatus.PENDING -> AssignmentStatus.IN_PROGRESS
                                    AssignmentStatus.IN_PROGRESS -> AssignmentStatus.SUBMITTED
                                    AssignmentStatus.SUBMITTED -> AssignmentStatus.PENDING
                                }
                                val newTasks = payload.tasks.map { if (it.id == task.id) it.copy(status = newStatus) else it }
                                viewModel.updateAssignmentPayload(entity, payload.copy(tasks = newTasks))
                            },"""
onClick_new = """                            onClick = {
                                viewModel.cycleAssignmentStatus(entity, task.id)
                            },"""
content = content.replace(onClick_old, onClick_new)

# 2. Update countdown rendering
countdown_old = """                                val daysRemaining = ((task.deadlineEpoch - System.currentTimeMillis()) / (1000 * 60 * 60 * 24)).toInt()
                Column(
                    modifier = Modifier"""
countdown_new = """                                val timeDiffMillis = task.deadlineEpoch - System.currentTimeMillis()
                val hoursRemaining = timeDiffMillis / (1000 * 60 * 60)
                val daysRemaining = hoursRemaining / 24
                val countdownStr = if (java.lang.Math.abs(daysRemaining) > 0) "T-${daysRemaining} DAYS" else "T-${hoursRemaining} HOURS"
                val format = java.text.SimpleDateFormat("dd MMM HH:mm", java.util.Locale.getDefault())
                val absoluteTime = format.format(java.util.Date(task.deadlineEpoch)).uppercase()
                Column(
                    modifier = Modifier"""
content = content.replace(countdown_old, countdown_new)

text_countdown_old = """                        Text(
                            text = "T-${if (daysRemaining >= 0) daysRemaining else daysRemaining} DAYS",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            color = if (daysRemaining < 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
                        )"""
text_countdown_new = """                        Text(
                            text = "[ $absoluteTime | $countdownStr ]",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            color = if (timeDiffMillis < 0) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
                        )"""
content = content.replace(text_countdown_old, text_countdown_new)

# 3. Update Add Deliverable logic
add_logic_old = """        var deliverableTitle by remember { mutableStateOf("") }
        var daysUntilDeadline by remember { mutableStateOf("") }
        ModalBottomSheet(onDismissRequest = { showAddAssignment = false }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Deliverable", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = deliverableTitle,
                    onValueChange = { deliverableTitle = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                
                OutlinedTextField(
                    value = daysUntilDeadline,
                    onValueChange = { daysUntilDeadline = it.filter { char -> char.isDigit() } },
                    label = { Text("Days until deadline") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                val hasChanges = deliverableTitle.isNotBlank()
                Button(
                    onClick = {
                        val days = daysUntilDeadline.toLongOrNull() ?: 0L
                        if (deliverableTitle.isNotBlank()) {
                            val targetEpoch = System.currentTimeMillis() + (days * 24 * 60 * 60 * 1000)
                            val newTask = Deliverable(title = deliverableTitle, deadlineEpoch = targetEpoch)
                            viewModel.updateAssignmentPayload(entity, payload.copy(tasks = payload.tasks + newTask))
                            showAddAssignment = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape,
                    enabled = hasChanges
                ) {
                    Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                }
            }
        }"""
add_logic_new = """        var deliverableTitle by remember { mutableStateOf("") }
        var dateStr by remember { mutableStateOf("") }
        var timeStr by remember { mutableStateOf("") }
        var selectedPrio by remember { mutableStateOf(PriorityLevel.MID) }
        var selectedRecur by remember { mutableStateOf(Recurrence.NONE) }
        ModalBottomSheet(onDismissRequest = { showAddAssignment = false }) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .padding(bottom = 32.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text("Add Deliverable", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                OutlinedTextField(
                    value = deliverableTitle,
                    onValueChange = { deliverableTitle = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = dateStr,
                        onValueChange = { dateStr = it },
                        label = { Text("Date (DD-MM-YY)") },
                        modifier = Modifier.weight(1f),
                        singleLine = true
                    )
                    OutlinedTextField(
                        value = timeStr,
                        onValueChange = { timeStr = it },
                        label = { Text("Time (24H HH:MM)") },
                        modifier = Modifier.weight(1f),
                        singleLine = true
                    )
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    PriorityLevel.values().forEach { p ->
                        FilterChip(selected = selectedPrio == p, onClick = { selectedPrio = p }, label = { Text("[ $p ]") })
                    }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Recurrence.values().forEach { r ->
                        FilterChip(selected = selectedRecur == r, onClick = { selectedRecur = r }, label = { Text(if(r == Recurrence.NONE) "[ ONE-OFF ]" else "[ WEEKLY ]") })
                    }
                }
                val hasChanges = deliverableTitle.isNotBlank() && dateStr.isNotBlank() && timeStr.isNotBlank()
                Button(
                    onClick = {
                        if (deliverableTitle.isNotBlank()) {
                            val format = java.text.SimpleDateFormat("dd-MM-yy HH:mm", java.util.Locale.getDefault())
                            val parsedEpoch = try {
                                format.parse("$dateStr $timeStr")?.time ?: System.currentTimeMillis()
                            } catch (e: Exception) {
                                System.currentTimeMillis()
                            }
                            val newTask = Deliverable(
                                title = deliverableTitle, 
                                deadlineEpoch = parsedEpoch, 
                                priority = selectedPrio, 
                                recurrence = selectedRecur
                            )
                            viewModel.updateAssignmentPayload(entity, payload.copy(tasks = payload.tasks + newTask))
                            showAddAssignment = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RectangleShape,
                    enabled = hasChanges
                ) {
                    Text(if (hasChanges) "SAVE CHANGES" else "NO CHANGES", fontWeight = FontWeight.Bold)
                }
            }
        }"""
content = content.replace(add_logic_old, add_logic_new)

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
    f.write(content)

