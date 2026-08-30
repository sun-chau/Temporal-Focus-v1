import re

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "r") as f:
    content = f.read()

delete_btn = """            if (draft.editingId != null) {
                OutlinedButton(
                    onClick = {
                        viewModel.deleteDailyScheduleSync(draft.editingId)
                        viewModel.clearDailyScheduleDraft()
                        onDiscardAndBack()
                    },
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.error)
                ) {
                    Text("Delete Schedule", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold)
                }
            }
"""

content = content.replace("            // Recurring Section", delete_btn + "\n            // Recurring Section")

with open("app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt", "w") as f:
    f.write(content)
