import re

with open("app/src/main/java/com/example/data/TimerTask.kt", "r") as f:
    content = f.read()

content = content.replace("val recurring: String? = null", "val recurring: String? = null,\n    val completionStatus: String? = null")

with open("app/src/main/java/com/example/data/TimerTask.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/AppDatabase.kt", "r") as f:
    content = f.read()

content = content.replace("version = 4", "version = 5")

with open("app/src/main/java/com/example/data/AppDatabase.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "fun markTaskComplete(task: TimerTask) {",
    "fun markTaskComplete(task: TimerTask, completionStatus: String? = null) {"
)
content = content.replace(
    "isCompleted = true, completedAt = System.currentTimeMillis()",
    "isCompleted = true, completedAt = System.currentTimeMillis(), completionStatus = completionStatus"
)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
