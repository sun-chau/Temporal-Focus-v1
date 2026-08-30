import re

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "r") as f:
    content = f.read()

# Modify the SwipeToDismissBoxValue.StartToEnd case
# We need to hoist state to the component.
# Actually, since it's a composable, we can just add a state var showCompletionDialog.

new_logic = '''    var showCompletionDialog by remember { mutableStateOf(false) }

    val dismissState = rememberSwipeToDismissBoxState(
        confirmValueChange = { dismissValue ->
            when (dismissValue) {
                SwipeToDismissBoxValue.StartToEnd -> {
                    if (isLapsed) {
                        showCompletionDialog = true
                        false // don't dismiss yet, wait for dialog
                    } else {
                        onComplete("ON_TIME")
                        true
                    }
                }
                SwipeToDismissBoxValue.EndToStart -> {
                    onDelete()
                    true
                }
                else -> false
            }
        },
        positionalThreshold = { it * 0.4f }
    )'''

content = re.sub(r'    val dismissState = rememberSwipeToDismissBoxState\([\s\S]+?positionalThreshold = \{ it \* 0\.4f \}\n    \)', new_logic, content)

# Change onComplete signature to (String) -> Unit
content = content.replace(
    'onComplete: () -> Unit,',
    'onComplete: (String) -> Unit,'
)

# Call onComplete with "ON_TIME" in other places if any, but ManageTimerItem has none else.
# Add the dialog at the end of ManageTimerItem
dialog_ui = '''    if (showCompletionDialog) {
        AlertDialog(
            onDismissRequest = { showCompletionDialog = false },
            title = { Text("Task Completion") },
            text = { Text("This task is overdue. How would you like to mark it?") },
            confirmButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    onComplete("ON_TIME")
                }) {
                    Text("On time (just marked late)")
                }
            },
            dismissButton = {
                TextButton(onClick = {
                    showCompletionDialog = false
                    onComplete("LATE")
                }) {
                    Text("Definitely late")
                }
            }
        )
    }
}
'''
content = content.replace("    }\n}\n", dialog_ui, 1)

# Now update the ManageTimersScreen calls to ManageTimerItem
content = content.replace(
    '                                onComplete = { viewModel.markTaskComplete(task) },',
    '                                onComplete = { status -> viewModel.markTaskComplete(task, status) },'
)

with open("app/src/main/java/com/example/ui/screens/ManageTimersScreen.kt", "w") as f:
    f.write(content)
