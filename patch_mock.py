import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """        viewModelScope.launch(Dispatchers.IO) {
            val count = journalDao.getTemplateCount()
            if (count == 0) {"""

replacement = """        viewModelScope.launch(Dispatchers.IO) {
            val count = journalDao.getTemplateCount()
            if (count == 0) {
                val defaultTemplates = listOf(
                    com.example.data.JournalTemplate(title = "The Daily Debrief", content = "• Did I execute my schedule as planned today?\\n\\n• What was the friction point that broke my discipline?\\n\\n• How did I handle stress or adversity today?\\n\\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Introspective Route", content = "• What is a belief or assumption I held today that I should question?\\n\\n• Am I acting out of habit, or out of intention?\\n\\n• What did I learn about myself in today's quiet moments?\\n\\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Evening Gratitude", content = "• List three specific things that went well today:\\n1. \\n2. \\n3. \\n\\n", isDefault = true)
                )
                defaultTemplates.forEach { journalDao.insertTemplate(it) }
            }
            
            val schedules = database.dailyScheduleDao().getAllSchedulesSync()
            if (schedules.isEmpty()) {
                com.example.data.MockDataGenerator.getMockTasks().forEach {
                    database.dailyScheduleDao().insertSchedule(it)
                }
            }
        }
        
        // This stops the target matching from failing"""

content = re.sub(r'        viewModelScope\.launch\(Dispatchers\.IO\) \{\n            val count = journalDao\.getTemplateCount\(\)\n            if \(count == 0\) \{[^\}]*\}', replacement.split("//")[0], content)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
