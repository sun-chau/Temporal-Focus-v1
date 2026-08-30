import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

start_idx = content.find('fun deleteDailySchedule(schedule: DailyScheduleTask) {')
end_idx = content.find('fun insertJournalEntry', start_idx)

if start_idx != -1 and end_idx != -1:
    new_func = """    fun deleteDailySchedule(schedule: DailyScheduleTask, deleteEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            if (deleteEntireSeries && schedule.seriesId != null) {
                db.dailyScheduleDao().deleteSeries(schedule.seriesId)
            } else {
                db.dailyScheduleDao().deleteSchedule(schedule)
            }
            recalculateAllLanes(db)
        }
    }
    
"""
    with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
        f.write(content[:start_idx] + new_func + content[end_idx:])
