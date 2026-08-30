import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''                CircularMenu\(
                    onComplete = \{ 
                        if \(isOverdue\) \{
                            showCompletionDialog = true
                        \} else \{
                            viewModel\.markTaskComplete\(task, "ON_TIME"\)
                        \}
                    \},
                    onEdit = \{ 
                        viewModel\.setEditingTask\(task\)
                        viewModel\.setCreatingChronometer\(true\)
                    \},
                    onInfo = \{ showDescriptionDialog = true \},
                    onDelete = \{ viewModel\.deleteTask\(task\) \}
                \)'''

replace_str = '''                CircularMenu(
                    onComplete = { 
                        if (isOverdue) {
                            showCompletionDialog = true
                        } else {
                            viewModel.markTaskComplete(task, "ON_TIME")
                        }
                    },
                    onEdit = { 
                        viewModel.setEditingTask(task)
                        viewModel.setCreatingChronometer(true)
                    },
                    onInfo = { showDescriptionDialog = true },
                    onDelete = { viewModel.deleteTask(task) },
                    onShift = { showShiftDialog = true }
                )'''

content = re.sub(search_str, replace_str, content)
with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
