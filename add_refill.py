import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

target = "    init {"

refill_func = """    private fun performRollingRefill() {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            // Background evaluation to refill occurrences when the generated batch approaches its end
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val allSchedules = db.dailyScheduleDao().getAllSchedulesSync()
            
            val latestTasks = mutableMapOf<String, com.example.data.DailyScheduleTask>()
            allSchedules.forEach { task ->
                if (task.seriesId != null) {
                    val currentLatest = latestTasks[task.seriesId]
                    if (currentLatest == null || task.startTime > currentLatest.startTime) {
                        latestTasks[task.seriesId] = task
                    }
                }
            }
            
            val maxDays = appSettings.recurrenceGenerationCapYears * 365
            val now = System.currentTimeMillis()
            val threshold = now + (maxDays - 30) * 86400000L
            
            latestTasks.forEach { (seriesId, lastTask) ->
                if (lastTask.recurrenceType != null && lastTask.startTime < threshold) {
                    // Refill batch logic here
                    // (Requires parsing recurrence rule and injecting 1-year batch)
                }
            }
        }
    }

    init {"""

if "performRollingRefill" not in content:
    content = content.replace(target, refill_func)
    # also call it in init
    content = content.replace("    init {\n", "    init {\n        performRollingRefill()\n")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
