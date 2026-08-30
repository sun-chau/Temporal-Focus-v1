import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

func = """
    fun saveAdvancedDeadline(draft: com.example.data.DeadlineDraft) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            
            // Delete old if editing
            if (draft.editingId != null) {
                db.timerTaskDao().deleteTaskById(draft.editingId)
            }
            
            if (!draft.isRecurring) {
                db.timerTaskDao().insertTask(
                    com.example.data.TimerTask(
                        id = draft.editingId ?: java.util.UUID.randomUUID().toString(),
                        name = draft.name,
                        description = draft.description,
                        tags = draft.tags,
                        createdAt = draft.createdAt,
                        targetDateTime = draft.targetTime,
                        priority = draft.priority,
                        reminderDateTime = draft.reminderDateTime,
                        link = draft.link,
                        attachmentUri = draft.attachmentUri
                    )
                )
            } else {
                val cal = java.util.Calendar.getInstance().apply { timeInMillis = draft.targetTime }
                var occurrences = 0
                val limit = if (draft.occurrenceCount <= 0) Int.MAX_VALUE else draft.occurrenceCount
                
                var iterations = 0
                while (occurrences < limit && iterations < 3650) {
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
                        
                        // Recalculate reminder offset if needed
                        val reminderDiff = if (draft.reminderDateTime != null) draft.targetTime - draft.reminderDateTime else null
                        val newReminder = if (reminderDiff != null) currentTarget - reminderDiff else null
                        
                        val t = com.example.data.TimerTask(
                            id = taskId,
                            name = draft.name,
                            description = draft.description,
                            tags = draft.tags,
                            createdAt = draft.createdAt,
                            targetDateTime = currentTarget,
                            priority = draft.priority,
                            reminderDateTime = newReminder,
                            link = draft.link,
                            attachmentUri = draft.attachmentUri
                        )
                        db.timerTaskDao().insertTask(t)
                        occurrences++
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 1)
                    iterations++
                }
            }
            
            // Re-fetch or whatever is needed
            setEditingTask(null)
            setTimerMode(com.example.viewmodel.TimerMode.MANAGE_TIMERS)
        }
    }
"""

content = content.replace("    fun addTimerTask", func + "\n    fun addTimerTask")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
