with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = lines[:176] + [
"        viewModelScope.launch(Dispatchers.IO) {\n",
"            val count = journalDao.getTemplateCount()\n",
"            if (count == 0) {\n",
"                val defaultTemplates = listOf(\n",
"                    com.example.data.JournalTemplate(title = \"The Daily Debrief\", content = \"• Did I execute my schedule as planned today?\\n\\n• What was the friction point that broke my discipline?\\n\\n• How did I handle stress or adversity today?\\n\\n\", isDefault = true),\n",
"                    com.example.data.JournalTemplate(title = \"The Introspective Route\", content = \"• What is a belief or assumption I held today that I should question?\\n\\n• Am I acting out of habit, or out of intention?\\n\\n• What did I learn about myself in today's quiet moments?\\n\\n\", isDefault = true),\n",
"                    com.example.data.JournalTemplate(title = \"The Evening Gratitude\", content = \"• List three specific things that went well today:\\n1. \\n2. \\n3. \\n\\n\", isDefault = true)\n",
"                )\n",
"                defaultTemplates.forEach { journalDao.insertTemplate(it) }\n",
"            }\n",
"            val schedules = database.dailyScheduleDao().getAllSchedulesSync()\n",
"            if (schedules.isEmpty()) {\n",
"                com.example.data.MockDataGenerator.getMockTasks().forEach {\n",
"                    database.dailyScheduleDao().insertSchedule(it)\n",
"                }\n",
"            }\n",
"        }\n",
"        \n",
"        viewModelScope.launch(Dispatchers.IO) {\n",
"            while (true) {\n",
"                val now = System.currentTimeMillis()\n",
"                val autoStatus = appSettings.autoStatusIfMissed\n",
"                if (autoStatus == \"COMPLETED\" || autoStatus == \"SKIPPED\") {\n",
"                    val schedules = _uiState.value.dailySchedules\n",
"                    for (schedule in schedules) {\n",
"                        if (schedule.endTime < now && schedule.status == \"NOT_DONE\") {\n",
"                            val updated = schedule.copy(status = autoStatus)\n",
"                            database.dailyScheduleDao().updateSchedule(updated)\n",
"                        }\n",
"                    }\n",
"                }\n"
] + lines[220:]

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.writelines(new_lines)
