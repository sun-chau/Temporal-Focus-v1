import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase, exemptTaskId: String? = null) {
        val tasks = db.dailyScheduleDao().getAllSchedulesSync()
        
        val activeTasks = tasks.filter { !it.isFinished }.sortedBy { it.startTime }
        val finishedTasks = tasks.filter { it.isFinished }.sortedBy { it.startTime }
        
        val updatedTasks = mutableListOf<com.example.data.DailyScheduleTask>()
        
        // Active Tasks Float
        val activeLaneEnds = mutableMapOf<Int, Long>()
        for (task in activeTasks) {
            var lane = if (task.id == exemptTaskId) task.laneIndex else 0
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
    }"""


replacement = """    private fun getVisualBounds(task: com.example.data.DailyScheduleTask): Pair<Long, Long> {
        val durationMillis = task.endTime - task.startTime
        val durationMinutes = durationMillis / 60000L
        val endCal = java.util.Calendar.getInstance().apply { timeInMillis = task.endTime }
        val endMinutes = endCal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + endCal.get(java.util.Calendar.MINUTE)
        
        val titleLen = task.title.length
        val tagLen = task.tag.length
        val maxTextLen = maxOf(titleLen.toFloat(), tagLen.toFloat() * 0.8f)
        // Adjust estimated width: 44dp base + 8dp per title char + 28dp for status icon
        val estimatedWidthDp = 44 + 28 + (maxTextLen * 8)
        val visualMinutes = estimatedWidthDp / 1.5f
        val visualDurationMillis = (visualMinutes * 60 * 1000L).toLong()
        
        val alignTextEnd = durationMinutes < 150 && endMinutes > 22 * 60
        
        if (alignTextEnd) {
            val visualStart = task.endTime - maxOf(durationMillis, visualDurationMillis)
            return Pair(minOf(task.startTime, visualStart), task.endTime)
        } else {
            val visualEnd = task.startTime + maxOf(durationMillis, visualDurationMillis)
            return Pair(task.startTime, maxOf(task.endTime, visualEnd))
        }
    }

    private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase, exemptTaskId: String? = null) {
        val tasks = db.dailyScheduleDao().getAllSchedulesSync()
        
        val activeTasks = tasks.filter { !it.isFinished }.sortedBy { it.startTime }
        val finishedTasks = tasks.filter { it.isFinished }.sortedBy { it.startTime }
        
        val updatedTasks = mutableListOf<com.example.data.DailyScheduleTask>()
        
        // Active Tasks Float
        val activeLaneEnds = mutableMapOf<Int, Long>()
        for (task in activeTasks) {
            val visualBounds = getVisualBounds(task)
            var lane = if (task.id == exemptTaskId) task.laneIndex else 0
            while (true) {
                val laneEnd = activeLaneEnds[lane] ?: 0L
                if (visualBounds.first >= laneEnd) {
                    activeLaneEnds[lane] = visualBounds.second
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
            val visualBounds = getVisualBounds(task)
            var lane = maxActiveLane + 1
            while (true) {
                val laneEnd = finishedLaneEnds[lane] ?: 0L
                if (visualBounds.first >= laneEnd) {
                    finishedLaneEnds[lane] = visualBounds.second
                    updatedTasks.add(task.copy(laneIndex = lane))
                    break
                }
                lane++
            }
        }
        
        // Update all tasks in db
        db.dailyScheduleDao().updateSchedules(updatedTasks)
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Target not found")
