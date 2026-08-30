import sys

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

loop_code = """
        viewModelScope.launch {
            while (true) {
                val now = System.currentTimeMillis()
                val autoStatus = appSettings.autoStatusIfMissed
                if (autoStatus == "COMPLETED" || autoStatus == "SKIPPED") {
                    val schedules = _uiState.value.dailySchedules
                    for (schedule in schedules) {
                        if (schedule.endTime < now && schedule.status == "NOT_DONE") {
                            val updated = schedule.copy(status = autoStatus)
                            db.dailyScheduleDao().updateSchedule(updated)
                        }
                    }
                }
                delay(60000)
            }
        }
"""

if "database.dailyScheduleDao().getAllSchedules().collect {" in content:
    content = content.replace("database.dailyScheduleDao().getAllSchedules().collect { schedules ->", loop_code + "\n            database.dailyScheduleDao().getAllSchedules().collect { schedules ->")
else:
    print("Could not find collect block")
    sys.exit(1)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
