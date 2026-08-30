import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

old_daily = """            } else {
                val cal = java.util.Calendar.getInstance().apply { timeInMillis = draft.startTime }
                var occurrences = 0
                val limit = if (draft.occurrenceCount <= 0) Int.MAX_VALUE else draft.occurrenceCount
                
                // Cap iteration to avoid infinite loops (max 3650 days = 10 years check)
                var iterations = 0
                if (targetSeriesId == null) { targetSeriesId = java.util.UUID.randomUUID().toString() }
                val maxDays = appSettings.recurrenceGenerationCapYears * 365
                while (occurrences < limit && iterations < maxDays) {
                    var match = false
                    when (draft.recurrenceType) {
                        com.example.data.RecurrenceType.DAILY -> {
                            match = (iterations % draft.dailyInterval.coerceIn(1, 120)) == 0
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
                                        // Technically end of year is Dec 31, but if month is selected as Dec...
                                        // Let's just say it's the last day of the selected month
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
                        val currentTarget = cal.timeInMillis
                        val taskId = if (occurrences == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                        
                        db.dailyScheduleDao().insertSchedule(
                            com.example.data.DailyScheduleTask(
                                id = taskId,
                                title = draft.title,
                                startTime = currentTarget,
                                endTime = currentTarget + duration,
                                tag = draft.tag,
                                seriesId = targetSeriesId,
                                recurrenceType = draft.recurrenceType.name
                            )
                        )
                        occurrences++
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 1)
                    iterations++
                }
            }"""

new_daily = """            } else {
                if (targetSeriesId == null) { targetSeriesId = java.util.UUID.randomUUID().toString() }
                val maxDays = appSettings.recurrenceGenerationCapYears * 365
                
                val pattern = draft.toRecurrencePattern()
                val occurrences = pattern.generateOccurrences(draft.startTime, maxIterations = maxDays)
                
                occurrences.forEachIndexed { index, currentTarget ->
                    val taskId = if (index == 0 && draft.editingId != null) draft.editingId else java.util.UUID.randomUUID().toString()
                    
                    db.dailyScheduleDao().insertSchedule(
                        com.example.data.DailyScheduleTask(
                            id = taskId,
                            title = draft.title,
                            startTime = currentTarget,
                            endTime = currentTarget + duration,
                            tag = draft.tag,
                            seriesId = targetSeriesId,
                            recurrenceType = draft.recurrenceType.name
                        )
                    )
                }
            }"""

if old_daily in content:
    content = content.replace(old_daily, new_daily)
else:
    print("WARNING: Could not find old_daily pattern.")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
