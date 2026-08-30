import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# 1. Update signature
content = content.replace("private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase) {", "private suspend fun recalculateAllLanes(db: com.example.data.AppDatabase, exemptTaskId: String? = null) {")

# 2. Update updateDailySchedule call
content = content.replace("db.dailyScheduleDao().updateSchedule(schedule)\n            recalculateAllLanes(db)", "db.dailyScheduleDao().updateSchedule(schedule)\n            recalculateAllLanes(db, exemptTaskId = schedule.id)")

# 3. Update the lane logic
target_lane_logic = """        for (task in activeTasks) {
            var lane = 0
            while (true) {"""

replacement_lane_logic = """        for (task in activeTasks) {
            var lane = if (task.id == exemptTaskId) task.laneIndex else 0
            while (true) {"""

content = content.replace(target_lane_logic, replacement_lane_logic)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
