import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

# 1. Add missing imports
more_imports = """
import com.example.ui.screens.getDayOfWeekName
import com.example.ui.screens.getWeekName
import com.example.ui.screens.getMonthName
import com.example.ui.screens.parseDateString
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.text.style.TextAlign
import java.util.Calendar
import com.example.data.MonthlyType
import com.example.data.AnnuallyType
"""
if "import java.util.Calendar" not in content:
    content = content.replace("import com.example.data.RecurrenceType", "import com.example.data.RecurrenceType\n" + more_imports)

# 2. Extract state block
start_idx = content.find("    // Recurring")
end_idx = content.find("    val formatDateTime = { time: Long ->")

replace_vars = """    // Recurring
    var isRecurring by remember { mutableStateOf(false) }
    var recurrenceType by remember { mutableStateOf(RecurrenceType.DAILY) }
    var dailyInterval by remember { mutableStateOf(1) }
    var weeklyDays by remember { mutableStateOf(setOf<Int>()) }
    
    var monthlyType by remember { mutableStateOf(MonthlyType.DATES) }
    var monthlyDates by remember { mutableStateOf(setOf<Int>()) }
    var monthlyWeek by remember { mutableStateOf(1) }
    var monthlyDayOfWeek by remember { mutableStateOf(Calendar.SUNDAY) }

    var annuallyType by remember { mutableStateOf(AnnuallyType.DATES) }
    var annuallyMonth by remember { mutableStateOf(Calendar.JANUARY) }
    var annuallyDates by remember { mutableStateOf(setOf<Int>()) }
    var annuallyWeek by remember { mutableStateOf(1) }
    var annuallyDayOfWeek by remember { mutableStateOf(Calendar.SUNDAY) }
    
    var occurrenceCount by remember { mutableStateOf(1) }
    
    var minusHolding by remember { mutableStateOf(false) }
    var plusHolding by remember { mutableStateOf(false) }
    var dailyMinusHolding by remember { mutableStateOf(false) }
    var dailyPlusHolding by remember { mutableStateOf(false) }

    LaunchedEffect(minusHolding) {
        if (minusHolding) {
            if (occurrenceCount > 0) occurrenceCount--
            kotlinx.coroutines.delay(500)
            while (minusHolding && occurrenceCount > 0) {
                occurrenceCount--
                kotlinx.coroutines.delay(100)
            }
        }
    }

    LaunchedEffect(plusHolding) {
        if (plusHolding) {
            occurrenceCount++
            kotlinx.coroutines.delay(500)
            while (plusHolding) {
                occurrenceCount++
                kotlinx.coroutines.delay(100)
            }
        }
    }

    LaunchedEffect(dailyMinusHolding) {
        if (dailyMinusHolding) {
            if (dailyInterval > 1) dailyInterval--
            kotlinx.coroutines.delay(500)
            while (dailyMinusHolding && dailyInterval > 1) {
                dailyInterval--
                kotlinx.coroutines.delay(100)
            }
        }
    }

    LaunchedEffect(dailyPlusHolding) {
        if (dailyPlusHolding) {
            dailyInterval++
            kotlinx.coroutines.delay(500)
            while (dailyPlusHolding) {
                dailyInterval++
                kotlinx.coroutines.delay(100)
            }
        }
    }
    
    val dynamicString = remember(
        isRecurring, recurrenceType, dailyInterval, weeklyDays,
        monthlyType, monthlyDates, monthlyWeek, monthlyDayOfWeek,
        annuallyType, annuallyMonth, annuallyDates, annuallyWeek, annuallyDayOfWeek, occurrenceCount
    ) {
        if (!isRecurring) return@remember "Does not repeat"
        
        val countStr = if (occurrenceCount <= 0) " indefinitely." else if (occurrenceCount > 1) " for $occurrenceCount occurrences." else " once."
        
        when (recurrenceType) {
            RecurrenceType.DAILY -> {
                if (dailyInterval == 1) "Repeats every day$countStr"
                else "Repeats every $dailyInterval days$countStr"
            }
            RecurrenceType.WEEKLY -> {
                if (weeklyDays.isEmpty()) "Repeats weekly on no days$countStr"
                else {
                    val daysStr = weeklyDays.sorted().joinToString(", ") { getDayOfWeekName(it) }
                    "Repeats weekly on $daysStr$countStr"
                }
            }
            RecurrenceType.MONTHLY -> {
                val condition = when (monthlyType) {
                    MonthlyType.DATES -> {
                        if (monthlyDates.isEmpty()) "no dates"
                        else "dates ${monthlyDates.sorted().joinToString(", ")}"
                    }
                    MonthlyType.LAST_DAY -> "the last day of the month"
                    MonthlyType.DAY_OF_WEEK -> {
                        val weekName = getWeekName(monthlyWeek)
                        val dayName = getDayOfWeekName(monthlyDayOfWeek)
                        "the $weekName $dayName"
                    }
                }
                "Repeats every month on $condition$countStr"
            }
            RecurrenceType.ANNUALLY -> {
                val monthName = getMonthName(annuallyMonth)
                val condition = when (annuallyType) {
                    AnnuallyType.DATES -> {
                        if (annuallyDates.isEmpty()) "no dates"
                        else "dates ${annuallyDates.sorted().joinToString(", ")} of $monthName"
                    }
                    AnnuallyType.END_OF_YEAR -> "the end of the year (Dec 31)"
                    AnnuallyType.DAY_OF_WEEK -> {
                        val weekName = getWeekName(annuallyWeek)
                        val dayName = getDayOfWeekName(annuallyDayOfWeek)
                        "the $weekName $dayName of $monthName"
                    }
                }
                "Repeats annually on $condition$countStr"
            }
            else -> "Does not repeat"
        }
    }
    
"""

content = content[:start_idx] + replace_vars + content[end_idx:]


# Search for the block starting with "if (editingTask != null) {" up to "viewModel.setEditingTask(null)"
save_block_start = content.find("if (editingTask != null) {")
save_block_end = content.find("viewModel.setEditingTask(null)", save_block_start)

replace_save = """                    viewModel.saveAdvancedDeadline(
                        com.example.data.DeadlineDraft(
                            name = if (name.isBlank()) "Untitled Task" else name,
                            description = description.takeIf { it.isNotBlank() },
                            tags = selectedTags.joinToString(","),
                            targetTime = targetTime,
                            createdAt = createdAt,
                            isRecurring = isRecurring,
                            recurrenceType = recurrenceType,
                            dailyInterval = dailyInterval,
                            weeklyDays = weeklyDays,
                            monthlyType = monthlyType,
                            monthlyDates = monthlyDates,
                            monthlyWeek = monthlyWeek,
                            monthlyDayOfWeek = monthlyDayOfWeek,
                            annuallyType = annuallyType,
                            annuallyMonth = annuallyMonth,
                            annuallyDates = annuallyDates,
                            annuallyWeek = annuallyWeek,
                            annuallyDayOfWeek = annuallyDayOfWeek,
                            occurrenceCount = occurrenceCount,
                            editingId = editingTask?.id,
                            priority = priority,
                            reminderDateTime = reminderDateTime,
                            link = link.takeIf { it.isNotBlank() },
                            attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                        )
                    )
                    """
content = content[:save_block_start] + replace_save + content[save_block_end:]


# Strip old UI and add new UI
with open("/tmp/ds_recurrence_ui_clean.txt", "r") as f:
    ui_block = f.read()
    
start_ui = content.find("            // Recurring Setup")
if start_ui != -1:
    content = content[:start_ui]
else:
    print("UI block not found!")
    
ui_block = ui_block.strip()
if ui_block.endswith("}"):
    ui_block = ui_block[:-1].strip()
    
wrapped_ui = """            item {
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
"""
# Find the second occurrence of "when (recurrenceType) {"
idx1 = ui_block.find("when (recurrenceType) {")
idx2 = ui_block.find("when (recurrenceType) {", idx1 + 1)
daily_block = ui_block[idx2:]

wrapped_ui += daily_block

# But wrapped_ui is just the body.
content += wrapped_ui + "\n            }\n        }\n    }\n}\n"

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
