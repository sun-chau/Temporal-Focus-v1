import re

with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "r") as f:
    content = f.read()

target = """                        DropdownMenu(
                            expanded = showExportMenu,
                            onDismissRequest = { showExportMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Export as Markdown (.md)") },
                                onClick = {
                                    showExportMenu = false
                                    mdExportLauncher.launch("journal_entry.md")
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Export as PDF (.pdf)") },
                                onClick = {
                                    showExportMenu = false
                                    pdfExportLauncher.launch("journal_entry.pdf")
                                }
                            )
                        }
                    }
                    IconButton(onClick = { isEditMode = !isEditMode }) {"""

replacement = """                        DropdownMenu(
                            expanded = showExportMenu,
                            onDismissRequest = { showExportMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Export as Markdown (.md)") },
                                onClick = {
                                    showExportMenu = false
                                    mdExportLauncher.launch("journal_entry.md")
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Export as PDF (.pdf)") },
                                onClick = {
                                    showExportMenu = false
                                    pdfExportLauncher.launch("journal_entry.pdf")
                                }
                            )
                        }
                    }
                    var showDeleteConfirm by remember { mutableStateOf(false) }
                    if (showDeleteConfirm) {
                        AlertDialog(
                            onDismissRequest = { showDeleteConfirm = false },
                            title = { Text("Delete Entry") },
                            text = { Text("Are you sure you want to delete this journal entry?") },
                            confirmButton = {
                                TextButton(onClick = {
                                    viewModel.deleteJournalEntry(entry)
                                    hasBeenSaved = true // prevent auto-save on close
                                    onClose()
                                }) { Text("Delete", color = MaterialTheme.colorScheme.error) }
                            },
                            dismissButton = {
                                TextButton(onClick = { showDeleteConfirm = false }) { Text("Cancel") }
                            }
                        )
                    }
                    IconButton(onClick = { showDeleteConfirm = true }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete")
                    }
                    IconButton(onClick = { isEditMode = !isEditMode }) {"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/PrivateJournalScreen.kt", "w") as f:
        f.write(content)
    print("Patched delete button")
else:
    print("Could not find delete target")

