import re

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "r") as f:
    content = f.read()

# 1. Update imports
if "import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", 
                              "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior\nimport androidx.compose.foundation.lazy.itemsIndexed\nimport androidx.compose.foundation.lazy.rememberLazyListState\nimport androidx.compose.ui.unit.sp")

# 2. Add TerminalWheelPicker at the end of the file
picker_component = """
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun TerminalWheelPicker(
    items: List<String>,
    onItemSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val listState = rememberLazyListState()
    val flingBehavior = rememberSnapFlingBehavior(lazyListState = listState)
    
    val selectedIndex by remember {
        derivedStateOf {
            val layoutInfo = listState.layoutInfo
            val visibleItemsInfo = layoutInfo.visibleItemsInfo
            if (visibleItemsInfo.isEmpty()) return@derivedStateOf -1
            
            val viewportCenter = layoutInfo.viewportEndOffset / 2
            val closest = visibleItemsInfo.minByOrNull { Math.abs((it.offset + it.size / 2) - viewportCenter) }
            closest?.index ?: -1
        }
    }
    
    LaunchedEffect(selectedIndex) {
        if (selectedIndex in items.indices) {
            onItemSelected(items[selectedIndex])
        }
    }

    Box(
        modifier = modifier
            .height(120.dp)
            .fillMaxWidth(),
        contentAlignment = Alignment.Center
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Spacer(modifier = Modifier.weight(1f))
            Box(modifier = Modifier.fillMaxWidth().height(40.dp).border(width = 1.dp, color = MaterialTheme.colorScheme.primary, shape = RectangleShape))
            Spacer(modifier = Modifier.weight(1f))
        }
        
        LazyColumn(
            state = listState,
            flingBehavior = flingBehavior,
            contentPadding = PaddingValues(vertical = 40.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            itemsIndexed(items) { index, item ->
                val isSelected = index == selectedIndex
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(40.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = item,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontFamily = FontFamily.Monospace,
                        fontSize = if (isSelected) 24.sp else 18.sp
                    )
                }
            }
        }
    }
}
"""

if "fun TerminalWheelPicker" not in content:
    content += picker_component

# 3. Replace Add Deliverable Logic
old_add_sheet = """        var deliverableTitle by remember { mutableStateOf("") }
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

new_add_sheet = """        var deliverableTitle by remember { mutableStateOf("") }
        val hours = remember { (0..23).map { it.toString().padStart(2, '0') } }
        val minutes = remember { (0..55 step 5).map { it.toString().padStart(2, '0') } }
        val days = remember { (1..31).map { it.toString().padStart(2, '0') } }
        val months = remember { (1..12).map { it.toString().padStart(2, '0') } }
        val years = remember { (2026..2030).map { it.toString() } }
        var selDay by remember { mutableStateOf(days[0]) }
        var selMonth by remember { mutableStateOf(months[0]) }
        var selYear by remember { mutableStateOf(years[0]) }
        var selHour by remember { mutableStateOf(hours[0]) }
        var selMinute by remember { mutableStateOf(minutes[0]) }
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
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                     TerminalWheelPicker(items = days, onItemSelected = { selDay = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = months, onItemSelected = { selMonth = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = years, onItemSelected = { selYear = it }, modifier = Modifier.weight(1f))
                }
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                     TerminalWheelPicker(items = hours, onItemSelected = { selHour = it }, modifier = Modifier.weight(1f))
                     TerminalWheelPicker(items = minutes, onItemSelected = { selMinute = it }, modifier = Modifier.weight(1f))
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
                val hasChanges = deliverableTitle.isNotBlank()
                Button(
                    onClick = {
                        if (deliverableTitle.isNotBlank()) {
                            val format = java.text.SimpleDateFormat("yyyy-MM-dd HH:mm", java.util.Locale.getDefault())
                            val parsedEpoch = try {
                                format.parse("$selYear-$selMonth-$selDay $selHour:$selMinute")?.time ?: System.currentTimeMillis()
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

content = content.replace(old_add_sheet, new_add_sheet)

with open("app/src/main/java/com/example/ui/screens/AssignmentTrackerUI.kt", "w") as f:
    f.write(content)

