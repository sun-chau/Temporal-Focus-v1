with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = []
inside = False
for line in lines:
    if "com.example.data.JournalTemplate(title = \"The Daily Debrief\"" in line:
        new_lines.append("                    com.example.data.JournalTemplate(title = \"The Daily Debrief\", content = \"• Did I execute my schedule as planned today?\\n\\n• What was the friction point that broke my discipline?\\n\\n• How did I handle stress or adversity today?\\n\\n\", isDefault = true),\n")
    elif "com.example.data.JournalTemplate(title = \"The Introspective Route\"" in line:
        new_lines.append("                    com.example.data.JournalTemplate(title = \"The Introspective Route\", content = \"• What is a belief or assumption I held today that I should question?\\n\\n• Am I acting out of habit, or out of intention?\\n\\n• What did I learn about myself in today's quiet moments?\\n\\n\", isDefault = true),\n")
    elif "com.example.data.JournalTemplate(title = \"The Evening Gratitude\"" in line:
        new_lines.append("                    com.example.data.JournalTemplate(title = \"The Evening Gratitude\", content = \"• List three specific things that went well today:\\n1. \\n2. \\n3. \\n\\n\", isDefault = true)\n")
        new_lines.append("                )\n")
        new_lines.append("                defaultTemplates.forEach { journalDao.insertTemplate(it) }\n")
        new_lines.append("            }\n")
        new_lines.append("            \n")
        new_lines.append("            val schedules = database.dailyScheduleDao().getAllSchedulesSync()\n")
        new_lines.append("            if (schedules.isEmpty()) {\n")
        new_lines.append("                com.example.data.MockDataGenerator.getMockTasks().forEach {\n")
        new_lines.append("                    database.dailyScheduleDao().insertSchedule(it)\n")
        new_lines.append("                }\n")
        new_lines.append("            }\n")
        inside = True
    elif inside:
        if "}" in line.strip() and "val schedules =" not in line:
            new_lines.append(line)
            inside = False
        # skip lines if we were in the middle of replacing it
    else:
        new_lines.append(line)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.writelines(new_lines)
