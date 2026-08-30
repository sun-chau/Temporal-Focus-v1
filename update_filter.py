import re

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'r') as f:
    content = f.read()

old_filter = "val quickDeadlines = activeTasks.filter { it.deadlineDateTime != null }.sortedBy { it.deadlineDateTime }"
new_filter = "val quickDeadlines = activeTasks.filter { it.labels == \"Reminder\" || it.deadlineDateTime != null }.sortedBy { it.deadlineDateTime ?: Long.MAX_VALUE }"

content = content.replace(old_filter, new_filter)

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'w') as f:
    f.write(content)
