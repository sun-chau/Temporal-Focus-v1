import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

# We need to find the dialog_ui I accidentally inserted and remove it.
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
content = content.replace(dialog_ui, "    }\n}\n")

# Now properly insert the dialog into `ChronometerItem`
# `ChronometerItem` ends before `fun ChronometerStatsOverlay`. We can find `fun ChronometerStatsOverlay` and insert it just above.

content = content.replace(
    "@Composable\nfun ChronometerStatsOverlay",
    dialog_ui + "\n@Composable\nfun ChronometerStatsOverlay"
)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
