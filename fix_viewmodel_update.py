import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("    fun markTaskComplete", "    fun updateTask(task: TimerTask) {\n        viewModelScope.launch {\n            repository.updateTask(task)\n        }\n    }\n\n    fun markTaskComplete")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
