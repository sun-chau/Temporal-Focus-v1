import re
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target_start = "            if (count == 0) {"
target_end = "            val schedules = database.dailyScheduleDao().getAllSchedulesSync()"

start_idx = content.find(target_start)
end_idx = content.find(target_end)

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx]
    after = content[end_idx:]
    middle = """            if (count == 0) {
                val defaultTemplates = listOf(
                    com.example.data.JournalTemplate(title = "The Daily Debrief", content = "• Did I execute my schedule as planned today?\\n\\n• What was the friction point that broke my discipline?\\n\\n• How did I handle stress or adversity today?\\n\\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Introspective Route", content = "• What is a belief or assumption I held today that I should question?\\n\\n• Am I acting out of habit, or out of intention?\\n\\n• What did I learn about myself in today's quiet moments?\\n\\n", isDefault = true),
                    com.example.data.JournalTemplate(title = "The Evening Gratitude", content = "• List three specific things that went well today:\\n1. \\n2. \\n3. \\n\\n", isDefault = true)
                )
                defaultTemplates.forEach { journalDao.insertTemplate(it) }
            }
            
"""
    new_content = before + middle + after
    with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
        f.write(new_content)
else:
    print("Could not find start or end index")
