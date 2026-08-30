import re
with open("app/src/main/java/com/example/data/DailyScheduleDao.kt", "r") as f:
    content = f.read()

new_methods = """
    @Query("SELECT * FROM daily_schedules ORDER BY startTime ASC")
    fun getAllSchedulesSync(): List<DailyScheduleTask>
    
    @Update
    suspend fun updateSchedules(schedules: List<DailyScheduleTask>)
"""
content = content.replace("fun getScheduleSync(id: String): DailyScheduleTask?", "fun getScheduleSync(id: String): DailyScheduleTask?\n" + new_methods)

with open("app/src/main/java/com/example/data/DailyScheduleDao.kt", "w") as f:
    f.write(content)
