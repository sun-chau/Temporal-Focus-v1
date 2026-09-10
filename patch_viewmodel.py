import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    fun addQuickDeadline(name: String, time: Long?) {
        viewModelScope.launch {
            val targetTime = time ?: (System.currentTimeMillis() + 86400000L)
            val task = com.example.data.TimerTask(
                name = name,
                targetDateTime = targetTime,
                deadlineDateTime = time,
                priority = "Normal",
                labels = "Reminder"
            )"""

replacement = """    fun addQuickDeadline(name: String, time: Long?, priority: String = "Normal") {
        viewModelScope.launch {
            val targetTime = time ?: (System.currentTimeMillis() + 86400000L)
            val task = com.example.data.TimerTask(
                name = name,
                targetDateTime = targetTime,
                deadlineDateTime = time,
                priority = priority,
                labels = "Reminder"
            )"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
        f.write(content)
    print("Patched MainViewModel")
else:
    print("Could not find target in MainViewModel")

