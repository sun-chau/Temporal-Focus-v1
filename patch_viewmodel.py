import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add to UiState
if 'val showQuickReminderSheet: Boolean = false' not in content:
    content = content.replace('val showSeconds: Boolean = true,', 'val showSeconds: Boolean = true,\n    val showQuickReminderSheet: Boolean = false,')

# Add setQuickReminderSheet
if 'fun setQuickReminderSheet' not in content:
    content = content.replace('fun setCreatingChronometer(isCreating: Boolean) {', 'fun setQuickReminderSheet(show: Boolean) {\n        _uiState.update { it.copy(showQuickReminderSheet = show) }\n    }\n\n    fun setCreatingChronometer(isCreating: Boolean) {')

# Add addQuickReminder
if 'fun addQuickReminder' not in content:
    content = content.replace('fun updateTimerTask(task: TimerTask) {', '''fun addQuickReminder(name: String, time: Long?) {
        viewModelScope.launch {
            val targetTime = time ?: (System.currentTimeMillis() + 86400000L)
            val task = com.example.data.TimerTask(
                name = name,
                targetDateTime = targetTime,
                reminderDateTime = time,
                priority = "Normal",
                tags = "None"
            )
            repository.insertTask(task)
            if (time != null) {
                com.example.receiver.AlarmScheduler.scheduleAlarmsForTask(getApplication(), task, appSettings.chronometerDeadlineOffsetMinutes)
            }
        }
    }

    fun updateTimerTask(task: TimerTask) {''')

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
