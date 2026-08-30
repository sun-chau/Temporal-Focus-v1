with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

content = content.replace("viewModel.updateDailySchedule(schedule.copy(status = newStatus.name))", 
"viewModel.updateDailySchedule(schedule.copy(status = newStatus.name, isFinished = (newStatus == ScheduleStatus.COMPLETED || newStatus == ScheduleStatus.SKIPPED || newStatus == ScheduleStatus.DROPPED)))")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
