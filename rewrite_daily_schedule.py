import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Make sure imports for LocalDensity and horizontalScroll exist
if "import androidx.compose.ui.platform.LocalDensity" not in content:
    content = content.replace("import androidx.compose.ui.platform.LocalContext", "import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.ui.platform.LocalDensity\nimport androidx.compose.ui.platform.LocalConfiguration")

if "import androidx.compose.foundation.horizontalScroll" not in content:
    content = content.replace("import androidx.compose.foundation.verticalScroll", "import androidx.compose.foundation.verticalScroll\nimport androidx.compose.foundation.horizontalScroll")

search_body_regex = re.compile(r'// Body: Daily Agenda View[\s\S]*?(?=\s*\}\s*\}\s*if\s*\(reschedulingSchedule)')

replace_body = '''// Body: Daily Agenda View (2D Canvas)
            val schedulesForDate = uiState.dailySchedules.filter {
                getStartOfDayMillis(it.startTime) == selectedDateMillis
            }.sortedBy { it.startTime }
            
            val horizontalScrollState = rememberScrollState()
            val verticalScrollState = rememberScrollState()
            val density = LocalDensity.current
            val configuration = LocalConfiguration.current
            val screenWidthDp = configuration.screenWidthDp
            
            val isToday = selectedDateMillis == getStartOfDayMillis(System.currentTimeMillis())
            
            LaunchedEffect(selectedDateMillis) {
                if (isToday) {
                    val cal = Calendar.getInstance()
                    val currentMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
                    val xOffsetPx = with(density) { (currentMinutes * 1.5f).dp.toPx() }
                    val screenWidthPx = with(density) { screenWidthDp.dp.toPx() }
                    
                    val targetScroll = (xOffsetPx - screenWidthPx / 2f).toInt()
                    horizontalScrollState.animateScrollTo(maxOf(0, targetScroll))
                } else {
                    horizontalScrollState.animateScrollTo(0)
                }
            }
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .horizontalScroll(horizontalScrollState)
            ) {
                // Timeline Ruler
                TimelineRuler()
                
                // Canvas Body
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                        .verticalScroll(verticalScrollState)
                ) {
                    val laneEndTimes = mutableListOf<Long>()
                    val scheduledLanes = mutableMapOf<DailyScheduleTask, Int>()
                    
                    for (schedule in schedulesForDate) {
                        var placed = false
                        for (i in laneEndTimes.indices) {
                            if (laneEndTimes[i] <= schedule.startTime) {
                                laneEndTimes[i] = schedule.endTime
                                scheduledLanes[schedule] = i
                                placed = true
                                break
                            }
                        }
                        if (!placed) {
                            scheduledLanes[schedule] = laneEndTimes.size
                            laneEndTimes.add(schedule.endTime)
                        }
                    }
                    
                    val totalLanes = maxOf(12, laneEndTimes.size)
                    val minHeight = (totalLanes * 80).dp
                    
                    Box(modifier = Modifier.width((24 * 60 * 1.5).dp).height(minHeight)) {
                        TimelineGrid(totalLanes)
                        
                        for (schedule in schedulesForDate) {
                            val lane = scheduledLanes[schedule] ?: 0
                            val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
                            val startMinutes = startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                            val durationMinutes = maxOf(10, ((schedule.endTime - schedule.startTime) / 60000).toInt())
                            
                            val xOffset = (startMinutes * 1.5f).dp
                            val yOffset = (lane * 80 + 4).dp
                            val width = (durationMinutes * 1.5f).dp
                            
                            ScheduleBlock(
                                schedule = schedule,
                                coloredTagsEnabled = uiState.coloredTagsEnabled,
                                modifier = Modifier
                                    .offset(x = xOffset, y = yOffset)
                                    .width(width)
                                    .height(72.dp),
                                onClick = { editingSchedule = schedule },
                                onStatusChange = { newStatus ->
                                    viewModel.updateDailySchedule(schedule.copy(status = newStatus.name))
                                }
                            )
                        }
                        
                        if (isToday) {
                            NowLine()
                        }
                    }
                }
            }
        }
    }'''

match = search_body_regex.search(content)
if match:
    content = content[:match.start()] + replace_body + content[match.end():]
else:
    print("Warning: Could not find the search body to replace.")

# Append the new composables at the end of the file if they don't exist
if "fun TimelineRuler" not in content:
    helpers = '''

@Composable
fun TimelineRuler() {
    val totalMinutes = 24 * 60
    val totalWidth = (totalMinutes * 1.5).dp
    
    Box(
        modifier = Modifier
            .width(totalWidth)
            .height(32.dp)
            .background(MaterialTheme.colorScheme.surface)
    ) {
        for (hour in 0..24) {
            val offset = (hour * 60 * 1.5).dp
            // Major tick
            Box(
                modifier = Modifier
                    .offset(x = offset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f))
            )
            // Label
            if (hour < 24) {
                Text(
                    text = String.format("%02d:00", hour),
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                    modifier = Modifier.offset(x = offset + 4.dp, y = 2.dp)
                )
            }
            
            // Minor tick at 30 min
            if (hour < 24) {
                val minorOffset = offset + (30 * 1.5).dp
                Box(
                    modifier = Modifier
                        .offset(x = minorOffset)
                        .width(1.dp)
                        .fillMaxHeight(0.5f)
                        .align(Alignment.BottomStart)
                        .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f))
                )
                Text(
                    text = "half",
                    fontSize = 8.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                    modifier = Modifier.offset(x = minorOffset + 2.dp, y = 14.dp)
                )
            }
        }
    }
}

@Composable
fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    val totalWidth = (totalMinutes * 1.5).dp
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 1.5).dp
        // Major tick line
        Box(
            modifier = Modifier
                .offset(x = offset)
                .width(1.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.08f))
        )
        // Minor tick line
        if (hour < 24) {
            val minorOffset = offset + (30 * 1.5).dp
            Box(
                modifier = Modifier
                    .offset(x = minorOffset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.04f))
            )
        }
    }
    
    // Horizontal lanes dividers
    for (lane in 0..totalLanes) {
        val offset = (lane * 80).dp
        Box(
            modifier = Modifier
                .offset(y = offset)
                .fillMaxWidth()
                .height(1.dp)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))
        )
    }
}

@Composable
fun NowLine(modifier: Modifier = Modifier) {
    var currentTime by remember { mutableStateOf(System.currentTimeMillis()) }
    
    LaunchedEffect(Unit) {
        while(true) {
            kotlinx.coroutines.delay(60000)
            currentTime = System.currentTimeMillis()
        }
    }
    
    val cal = Calendar.getInstance().apply { timeInMillis = currentTime }
    val minutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)
    val xOffset = (minutes * 1.5f).dp
    
    Box(
        modifier = modifier
            .offset(x = xOffset)
            .width(2.dp)
            .fillMaxHeight()
            .background(Color.Red)
    )
}

@Composable
fun ScheduleBlock(
    schedule: DailyScheduleTask,
    coloredTagsEnabled: Boolean,
    modifier: Modifier,
    onClick: () -> Unit,
    onStatusChange: (ScheduleStatus) -> Unit
) {
    val tagColor = getTagColor(schedule.tag, coloredTagsEnabled)
    var showStatusMenu by remember { mutableStateOf(false) }
    
    val startCal = Calendar.getInstance().apply { timeInMillis = schedule.startTime }
    val endCal = Calendar.getInstance().apply { timeInMillis = schedule.endTime }
    val startStr = String.format("%02d:%02d", startCal.get(Calendar.HOUR_OF_DAY), startCal.get(Calendar.MINUTE))
    val endStr = String.format("%02d:%02d", endCal.get(Calendar.HOUR_OF_DAY), endCal.get(Calendar.MINUTE))
    
    val status = try { ScheduleStatus.valueOf(schedule.status) } catch (e: Exception) { ScheduleStatus.NOT_STARTED }
    val opacity = if (status == ScheduleStatus.DONE || status == ScheduleStatus.SKIPPED || status == ScheduleStatus.DROPPED) 0.6f else 0.9f
    
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(tagColor.copy(alpha = opacity))
            .clickable { onClick() }
            .padding(8.dp)
    ) {
        Column(modifier = Modifier.padding(end = 28.dp).fillMaxSize()) {
            Text(
                text = schedule.title, 
                fontWeight = FontWeight.Bold, 
                fontSize = 14.sp, 
                color = Color.White,
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
            Text(
                text = getTagName(schedule.tag), 
                fontSize = 10.sp, 
                color = Color.White.copy(alpha = 0.8f),
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = "$startStr - $endStr", 
                fontSize = 10.sp, 
                color = Color.White.copy(alpha = 0.8f),
                maxLines = 1
            )
        }
        
        // Status Icon on the right
        Box(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .size(28.dp)
                .clip(CircleShape)
                .background(Color.Black.copy(alpha = 0.2f))
                .clickable { showStatusMenu = true },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = when (status) {
                    ScheduleStatus.DONE -> Icons.Default.CheckCircle
                    ScheduleStatus.SKIPPED -> Icons.Default.FastForward
                    ScheduleStatus.DROPPED -> Icons.Default.Cancel
                    else -> Icons.Outlined.RadioButtonUnchecked
                },
                contentDescription = "Status",
                tint = Color.White,
                modifier = Modifier.size(18.dp)
            )
            
            DropdownMenu(
                expanded = showStatusMenu,
                onDismissRequest = { showStatusMenu = false }
            ) {
                ScheduleStatus.values().forEach { statusOption ->
                    DropdownMenuItem(
                        text = { Text(statusOption.name) },
                        onClick = {
                            onStatusChange(statusOption)
                            showStatusMenu = false
                        }
                    )
                }
            }
        }
    }
}
'''
    content += helpers

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
