import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

bad_dialog = '''    if (showCompletionDialog) {
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
}'''

content = content.replace(bad_dialog, "")

# Find the end of ChronometerItem
# ChronometerItem ends with:
#             Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
#                 Text("ID: ${task.id.toString().take(6)}...", color = Color.Gray, fontSize = 12.sp)
#                 Text("In Progress", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
#             }
#         }
#     }
# }
# We want to replace the last } with the dialog and then a }

search_str = '''            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("ID: ${task.id.toString().take(6)}...", color = Color.Gray, fontSize = 12.sp)
                Text("In Progress", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}'''

replace_str = '''            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("ID: ${task.id.toString().take(6)}...", color = Color.Gray, fontSize = 12.sp)
                Text("In Progress", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
    
    if (showCompletionDialog) {
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
}'''

content = content.replace(search_str, replace_str)

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
