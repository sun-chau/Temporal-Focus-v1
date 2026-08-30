with open("app/src/main/java/com/example/data/DailyScheduleTask.kt", "r") as f:
    content = f.read()

if "val laneIndex: Int = 0" not in content:
    content = content.replace("val status: String = ScheduleStatus.NOT_DONE.name", "val status: String = ScheduleStatus.NOT_DONE.name,\n    val laneIndex: Int = 0,\n    val isFinished: Boolean = false")
    with open("app/src/main/java/com/example/data/DailyScheduleTask.kt", "w") as f:
        f.write(content)
