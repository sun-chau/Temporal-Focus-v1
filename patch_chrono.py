import re

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "r") as f:
    content = f.read()

# Replace the variables
search_vars = """        // Recurring
    var recurrenceType by remember { mutableStateOf(editingTask?.let { runCatching { RecurrenceType.valueOf(it.recurrenceType) }.getOrDefault(RecurrenceType.NONE) } ?: RecurrenceType.NONE) }
    var customDaysInterval by remember { mutableStateOf(editingTask?.customDaysInterval?.toString() ?: "") }
    var maxRepetitions by remember { mutableStateOf(editingTask?.maxRepetitions?.toString() ?: "") }
    var specificDays by remember { mutableStateOf(editingTask?.specificDays?.split(",")?.filter { it.isNotEmpty() }?.map { it.toInt() }?.toSet() ?: setOf<Int>()) } // 1-7 for weekdays, 1-31 for month dates
    
    var expandedRecurrence by remember { mutableStateOf(false) }"""

replace_vars = """        // Recurring
    var isRecurring by remember { mutableStateOf(false) }
    var recurrenceType by remember { mutableStateOf(RecurrenceType.DAILY) }
    var dailyInterval by remember { mutableStateOf(1) }
    var weeklyDays by remember { mutableStateOf(setOf<Int>()) }
    
    var monthlyType by remember { mutableStateOf(com.example.data.MonthlyType.DATES) }
    var monthlyDates by remember { mutableStateOf(setOf<Int>()) }
    var monthlyWeek by remember { mutableStateOf(1) }
    var monthlyDayOfWeek by remember { mutableStateOf(java.util.Calendar.SUNDAY) }

    var annuallyType by remember { mutableStateOf(com.example.data.AnnuallyType.DATES) }
    var annuallyMonth by remember { mutableStateOf(java.util.Calendar.JANUARY) }
    var annuallyDates by remember { mutableStateOf(setOf<Int>()) }
    var annuallyWeek by remember { mutableStateOf(1) }
    var annuallyDayOfWeek by remember { mutableStateOf(java.util.Calendar.SUNDAY) }
    
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
                    com.example.data.MonthlyType.DATES -> {
                        if (monthlyDates.isEmpty()) "no dates"
                        else "dates ${monthlyDates.sorted().joinToString(", ")}"
                    }
                    com.example.data.MonthlyType.LAST_DAY -> "the last day of the month"
                    com.example.data.MonthlyType.DAY_OF_WEEK -> {
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
                    com.example.data.AnnuallyType.DATES -> {
                        if (annuallyDates.isEmpty()) "no dates"
                        else "dates ${annuallyDates.sorted().joinToString(", ")} of $monthName"
                    }
                    com.example.data.AnnuallyType.END_OF_YEAR -> "the end of the year (Dec 31)"
                    com.example.data.AnnuallyType.DAY_OF_WEEK -> {
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

content = content.replace(search_vars, replace_vars)

# Replace the save logic
search_save = """                                    viewModel.addTimerTask(
                                        name = name,
                                        description = description.takeIf { it.isNotBlank() },
                                        tags = selectedTags.joinToString(","),
                                        targetDate = targetTime,
                                        createdAt = createdAt,
                                        recurrenceType = recurrenceType.name,
                                        customDaysInterval = customDaysInterval.toIntOrNull(),
                                        maxRepetitions = maxRepetitions.toIntOrNull(),
                                        specificDays = specificDays.joinToString(","),
                                        priority = priority,
                                        reminderDateTime = reminderDateTime,
                                        link = link.takeIf { it.isNotBlank() },
                                        attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                                    )"""

replace_save = """                                    viewModel.saveAdvancedDeadline(
                                        com.example.data.DeadlineDraft(
                                            name = name,
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
                                            editingId = null,
                                            priority = priority,
                                            reminderDateTime = reminderDateTime,
                                            link = link.takeIf { it.isNotBlank() },
                                            attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                                        )
                                    )"""

content = content.replace(search_save, replace_save)

search_update = """                                    viewModel.updateTimerTask(editingTask.copy(
                                        name = name,
                                        description = description.takeIf { it.isNotBlank() },
                                        tags = selectedTags.joinToString(","),
                                        targetDateTime = targetTime,
                                        createdAt = createdAt,
                                        recurrenceType = recurrenceType.name,
                                        customDaysInterval = customDaysInterval.toIntOrNull(),
                                        maxRepetitions = maxRepetitions.toIntOrNull(),
                                        specificDays = specificDays.joinToString(","),
                                        priority = priority,
                                        reminderDateTime = reminderDateTime,
                                        link = link.takeIf { it.isNotBlank() },
                                        attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                                    ))"""

replace_update = """                                    viewModel.saveAdvancedDeadline(
                                        com.example.data.DeadlineDraft(
                                            name = name,
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
                                            editingId = editingTask.id,
                                            priority = priority,
                                            reminderDateTime = reminderDateTime,
                                            link = link.takeIf { it.isNotBlank() },
                                            attachmentUri = attachmentUri.takeIf { it.isNotBlank() }
                                        )
                                    )"""

content = content.replace(search_update, replace_update)


# Replace the recurring setup UI
# I need to match everything from "// Recurring Setup" to the end of the file.
pattern = r"            // Recurring Setup\n            item \{.*?(?=\s*\}\s*\})\}[\s\S]*\}\s*\}"
import sys

# Instead of regex, I'll find the line index and truncate
lines = content.split('\n')
start_idx = -1
for i, line in enumerate(lines):
    if "            // Recurring Setup" in line:
        start_idx = i
        break

if start_idx != -1:
    lines = lines[:start_idx]

content = '\n'.join(lines)

with open("app/src/main/java/com/example/ui/screens/CreateChronometerScreen.kt", "w") as f:
    f.write(content)
