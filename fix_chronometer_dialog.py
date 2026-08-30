import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

# Add a state for dialog
state_str = '''    var showDescriptionDialog by remember { mutableStateOf(false) }
    var showCompletionDialog by remember { mutableStateOf(false) }'''
content = content.replace('    var showDescriptionDialog by remember { mutableStateOf(false) }', state_str)

# Modify the CircularMenu complete action
old_circular = r'''                CircularMenu\(
                    onComplete = \{ viewModel\.markTaskComplete\(task\) \},
                    onEdit = \{ 
                        viewModel\.setEditingTask\(task\)
                        viewModel\.setCreatingChronometer\(true\)
                    \},
                    onInfo = \{ showDescriptionDialog = true \},
                    onDelete = \{ viewModel\.deleteTask\(task\) \}
                \)'''
new_circular = '''                CircularMenu(
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
                    onDelete = { viewModel.deleteTask(task) }
                )'''
content = re.sub(old_circular, new_circular, content)

# Add the dialog UI at the end of ChronometerItem
dialog_ui = '''    if (showCompletionDialog) {
        AlertDialog(
            onDismissRequest = { showCompletionDialog = false },
            title = { Text("Task Completion") },
            text = { Text("This task is overdue. How would you like to mark it?") },
            confirmButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    viewModel.markTaskComplete(task, "ON_TIME")
                }) {
                    Text("On time (just marked late)")
                }
            },
            dismissButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    viewModel.markTaskComplete(task, "LATE")
                }) {
                    Text("Definitely late")
                }
            }
        )
    }
}
'''
content = re.sub(r'    \}\n\}\n', dialog_ui, content, count=1)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
