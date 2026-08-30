import re
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

recalculate_func = """
    private fun recalculateAllLanes(db: com.example.data.AppDatabase) {
        val tasks = db.dailyScheduleDao().getAllSchedulesSync()
        
        val activeTasks = tasks.filter { !it.isFinished }.sortedBy { it.startTime }
        val finishedTasks = tasks.filter { it.isFinished }.sortedBy { it.startTime }
        
        val updatedTasks = mutableListOf<com.example.data.DailyScheduleTask>()
        
        // Active Tasks Float
        val activeLaneEnds = mutableMapOf<Int, Long>()
        for (task in activeTasks) {
            var lane = 0
            while (true) {
                val laneEnd = activeLaneEnds[lane] ?: 0L
                if (task.startTime >= laneEnd) {
                    activeLaneEnds[lane] = task.endTime
                    updatedTasks.add(task.copy(laneIndex = lane))
                    break
                }
                lane++
            }
        }
        
        val maxActiveLane = if (activeLaneEnds.isEmpty()) -1 else activeLaneEnds.keys.maxOrNull() ?: -1
        
        // Completion Drop
        val finishedLaneEnds = mutableMapOf<Int, Long>()
        for (task in finishedTasks) {
            var lane = maxActiveLane + 1
            while (true) {
                val laneEnd = finishedLaneEnds[lane] ?: 0L
                if (task.startTime >= laneEnd) {
                    finishedLaneEnds[lane] = task.endTime
                    updatedTasks.add(task.copy(laneIndex = lane))
                    break
                }
                lane++
            }
        }
        
        // Update all tasks in db
        db.dailyScheduleDao().updateSchedules(updatedTasks)
    }
"""

content = content.replace("fun addDailySchedule(", recalculate_func + "\n    fun addDailySchedule(")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
