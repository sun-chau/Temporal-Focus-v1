import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

func = """    fun deleteDailyScheduleSync(id: String) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val db = com.example.data.AppDatabase.getDatabase(getApplication())
            val existing = db.dailyScheduleDao().getScheduleSync(id)
            if (existing != null) {
                db.dailyScheduleDao().deleteSchedule(existing)
            }
        }
    }
"""

content = content.replace("    fun updateDailyScheduleDraft", func + "\n    fun updateDailyScheduleDraft")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
