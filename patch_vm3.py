import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

start_idx = content.find('fun deleteDailyScheduleSync(id: String) {')
end_idx = content.find('fun updateDailyScheduleDraft', start_idx)

if start_idx != -1 and end_idx != -1:
    new_func = """    fun deleteDailyScheduleSync(id: String, deleteEntireSeries: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val existing = db.dailyScheduleDao().getScheduleSync(id)
            if (existing != null) {
                if (deleteEntireSeries && existing.seriesId != null) {
                    db.dailyScheduleDao().deleteSeries(existing.seriesId)
                } else {
                    db.dailyScheduleDao().deleteSchedule(existing)
                }
                recalculateAllLanes(db)
            }
        }
    }

"""
    with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
        f.write(content[:start_idx] + new_func + content[end_idx:])
