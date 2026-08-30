import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace saveAdvancedDailySchedule
# We will do a robust replacement of the whole function block.
start_idx = content.find('fun saveAdvancedDailySchedule(draft: com.example.data.DailyScheduleDraft) {')
end_idx = content.find('fun deleteDailyScheduleSync', start_idx)

if start_idx != -1 and end_idx != -1:
    new_func = """    fun saveAdvancedDailySchedule(draft: com.example.data.DailyScheduleDraft, editEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val duration = draft.endTime - draft.startTime
            
            var targetSeriesId = draft.seriesId
            
            if (draft.editingId != null) {
                val existing = db.dailyScheduleDao().getScheduleSync(draft.editingId)
                if (existing != null) {
                    if (editEntireSeries && targetSeriesId != null) {
                        // Cascading update
                        val timeDelta = draft.startTime - existing.startTime
                        db.dailyScheduleDao().updateSeries(targetSeriesId, draft.title, draft.tag, timeDelta)
                        recalculateAllLanes(db)
                        clearDailyScheduleDraft()
                        return@launch
                    } else {
                        // Single update
                        if (targetSeriesId != null) {
                            // Break from series
                            db.dailyScheduleDao().breakFromSeries(draft.editingId)
                            targetSeriesId = null // It's now independent
                        }
                        db.dailyScheduleDao().deleteSchedule(existing)
                    }
                }
            }
            
            if (!draft.isRecurring) {
                db.dailyScheduleDao().insertSchedule(
                    com.example.data.DailyScheduleTask(
                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        title = draft.title,
                        startTime = draft.startTime,
                        endTime = draft.endTime,
                        tag = draft.tag,
                        seriesId = targetSeriesId
                    )
                )
            } else {
                if (targetSeriesId == null) {
                    targetSeriesId = java.util.UUID.randomUUID().toString()
                }
                val cal = java.util.Calendar.getInstance().apply { timeInMillis = draft.startTime }
                var occurrences = 0
                val limit = if (draft.occurrenceCount <= 0) Int.MAX_VALUE else draft.occurrenceCount
                
                // The Default Cap: 1 year forward from creation date (or based on settings)
                val maxDays = appSettings.recurrenceGenerationCapYears * 365
                
                var iterations = 0
                while (occurrences < limit && iterations < maxDays) {
                    var match = false
                    when (draft.recurrenceType) {
                        com.example.data.RecurrenceType.DAILY -> {
                            match = (iterations % draft.dailyInterval.coerceAtLeast(1)) == 0
                        }
                        com.example.data.RecurrenceType.WEEKLY -> {
                            val dayOfWeek = cal.get(java.util.Calendar.DAY_OF_WEEK)
                            match = draft.weeklyDays.contains(dayOfWeek)
                        }
                        com.example.data.RecurrenceType.MONTHLY -> {
                            when (draft.monthlyType) {
                                com.example.data.MonthlyType.DATES -> {
                                    val date = cal.get(java.util.Calendar.DAY_OF_MONTH)
                                    match = draft.monthlyDates.contains(date)
                                }
                                com.example.data.MonthlyType.LAST_DAY -> {
                                    val lastDay = cal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH)
                                    match = cal.get(java.util.Calendar.DAY_OF_MONTH) == lastDay
                                }
                                com.example.data.MonthlyType.DAY_OF_WEEK -> {
                                    val dayOfWeek = cal.get(java.util.Calendar.DAY_OF_WEEK)
                                    val weekOfMonth = cal.get(java.util.Calendar.DAY_OF_WEEK_IN_MONTH)
                                    
                                    val targetWeek = if (draft.monthlyWeek == 5) {
                                        // "Last"
                                        val tempCal = cal.clone() as java.util.Calendar
                                        tempCal.set(java.util.Calendar.DAY_OF_MONTH, tempCal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH))
                                        var lastWeek = 0
                                        while (tempCal.get(java.util.Calendar.MONTH) == cal.get(java.util.Calendar.MONTH)) {
                                            if (tempCal.get(java.util.Calendar.DAY_OF_WEEK) == draft.monthlyDayOfWeek) {
                                                lastWeek = tempCal.get(java.util.Calendar.DAY_OF_WEEK_IN_MONTH)
                                                break
                                            }
                                            tempCal.add(java.util.Calendar.DAY_OF_MONTH, -1)
                                        }
                                        lastWeek
                                    } else {
                                        draft.monthlyWeek
                                    }
                                    
                                    match = (dayOfWeek == draft.monthlyDayOfWeek && weekOfMonth == targetWeek)
                                }
                            }
                        }
                        com.example.data.RecurrenceType.ANNUALLY -> {
                            if (cal.get(java.util.Calendar.MONTH) == draft.annuallyMonth) {
                                when (draft.annuallyType) {
                                    com.example.data.AnnuallyType.DATES -> {
                                        val date = cal.get(java.util.Calendar.DAY_OF_MONTH)
                                        match = draft.annuallyDates.contains(date)
                                    }
                                    com.example.data.AnnuallyType.END_OF_YEAR -> {
                                        val lastDay = cal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH)
                                        match = cal.get(java.util.Calendar.DAY_OF_MONTH) == lastDay
                                    }
                                    com.example.data.AnnuallyType.DAY_OF_WEEK -> {
                                        val dayOfWeek = cal.get(java.util.Calendar.DAY_OF_WEEK)
                                        val weekOfMonth = cal.get(java.util.Calendar.DAY_OF_WEEK_IN_MONTH)
                                        
                                        val targetWeek = if (draft.annuallyWeek == 5) {
                                            // "Last"
                                            val tempCal = cal.clone() as java.util.Calendar
                                            tempCal.set(java.util.Calendar.DAY_OF_MONTH, tempCal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH))
                                            var lastWeek = 0
                                            while (tempCal.get(java.util.Calendar.MONTH) == cal.get(java.util.Calendar.MONTH)) {
                                                if (tempCal.get(java.util.Calendar.DAY_OF_WEEK) == draft.annuallyDayOfWeek) {
                                                    lastWeek = tempCal.get(java.util.Calendar.DAY_OF_WEEK_IN_MONTH)
                                                    break
                                                }
                                                tempCal.add(java.util.Calendar.DAY_OF_MONTH, -1)
                                            }
                                            lastWeek
                                        } else {
                                            draft.annuallyWeek
                                        }
                                        match = (dayOfWeek == draft.annuallyDayOfWeek && weekOfMonth == targetWeek)
                                    }
                                }
                            }
                        }
                        com.example.data.RecurrenceType.NONE -> { match = false }
                        else -> { match = false }
                    }
                    
                    if (match) {
                        val currentStart = cal.timeInMillis
                        val currentEnd = currentStart + duration
                        val taskId = if (occurrences == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                        
                        // Calculate seriesEndDate if there's a limit, although we might just calculate it loosely or leave null if unbounded
                        val seriesEnd = if (limit != Int.MAX_VALUE) null else null // Simplified for now, or could pre-calculate
                        
                        db.dailyScheduleDao().insertSchedule(
                            com.example.data.DailyScheduleTask(
                                id = taskId,
                                title = draft.title,
                                startTime = currentStart,
                                endTime = currentEnd,
                                tag = draft.tag,
                                seriesId = targetSeriesId,
                                recurrenceType = draft.recurrenceType.name,
                                seriesEndDate = null
                            )
                        )
                        occurrences++
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 1)
                    iterations++
                }
            }
            recalculateAllLanes(db)
        }
        clearDailyScheduleDraft()
    }
"""
    # Write it out
    with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
        f.write(content[:start_idx] + new_func + content[end_idx-4:])
