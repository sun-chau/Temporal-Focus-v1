import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

search_str = r'''    var showDescriptionDialog by remember \{ mutableStateOf\(false\) \}
    var showCompletionDialog by remember \{ mutableStateOf\(false\) \}'''

replace_str = '''    var showDescriptionDialog by remember { mutableStateOf(false) }
    var showCompletionDialog by remember { mutableStateOf(false) }
    var showShiftDialog by remember { mutableStateOf(false) }'''

content = re.sub(search_str, replace_str, content)

search_dialogs = r'''    if \(showCompletionDialog\) \{
        AlertDialog\('''

replace_dialogs = '''    if (showShiftDialog) {
        DateTimePickerDialog(
            initialTime = task.targetDateTime,
            onDismiss = { showShiftDialog = false },
            onTimeSelected = { newTargetTime ->
                val shiftedAmount = newTargetTime - task.targetDateTime
                if (shiftedAmount > 0) {
                    val updatedTask = task.copy(
                        targetDateTime = newTargetTime,
                        shiftedAmount = task.shiftedAmount + shiftedAmount
                    )
                    viewModel.updateTask(updatedTask)
                }
                showShiftDialog = false
            }
        )
    }

    if (showCompletionDialog) {
        AlertDialog('''

content = re.sub(search_dialogs, replace_dialogs, content)

# update CircularMenu call
search_menu = r'''                CircularMenu\(
                    onComplete = \{ 
                        if \(isOverdue\) \{
                            showCompletionDialog = true
                        \} else \{
                            viewModel\.markTaskComplete\(task, "ON_TIME"\)
                        \}
                    \},
                    onEdit = \{ /\* TODO \*/ \},
                    onInfo = \{ showDescriptionDialog = true \},
                    onDelete = \{ viewModel\.deleteTask\(task\) \}
                \)'''

replace_menu = '''                CircularMenu(
                    onComplete = { 
                        if (isOverdue) {
                            showCompletionDialog = true
                        } else {
                            viewModel.markTaskComplete(task, "ON_TIME")
                        }
                    },
                    onEdit = { /* TODO */ },
                    onInfo = { showDescriptionDialog = true },
                    onDelete = { viewModel.deleteTask(task) },
                    onShift = { showShiftDialog = true }
                )'''

content = re.sub(search_menu, replace_menu, content)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
