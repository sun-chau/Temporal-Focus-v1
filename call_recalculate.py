import re
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# For addDailyScheduleFromDraft
content = content.replace("clearDailyScheduleDraft()", "recalculateAllLanes(db)\n        clearDailyScheduleDraft()")

# For addDailySchedule
content = re.sub(r"db\.dailyScheduleDao\(\)\.insertSchedule\(\n\s*DailyScheduleTask\(title = title, startTime = startTime, endTime = endTime, tag = tag\)\n\s*\)", "db.dailyScheduleDao().insertSchedule(\n                    DailyScheduleTask(title = title, startTime = startTime, endTime = endTime, tag = tag)\n                )\n                recalculateAllLanes(db)", content)
content = re.sub(r"cal\.add\(java\.util\.Calendar\.DAY_OF_YEAR, 1\)\n\s*\}", "cal.add(java.util.Calendar.DAY_OF_YEAR, 1)\n                }\n                recalculateAllLanes(db)", content)

# For updateDailySchedule
content = content.replace("db.dailyScheduleDao().updateSchedule(schedule)", "db.dailyScheduleDao().updateSchedule(schedule)\n            recalculateAllLanes(db)")

# For deleteDailySchedule
content = content.replace("db.dailyScheduleDao().deleteSchedule(schedule)", "db.dailyScheduleDao().deleteSchedule(schedule)\n            recalculateAllLanes(db)")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
