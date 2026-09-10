import re

with open("app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt", "r") as f:
    content = f.read()

target_start = content.find("items(completedReminders) { task ->")
target_end = content.find("                }\n            }\n        }\n    }\n}") + len("                }\n            }\n        }\n    }\n}")

if target_start != -1 and target_end != -1:
    target = content[target_start:target_end]
    replacement = """items(completedReminders, key = { it.id }) { task ->
                    val isSelected = task.id in selectedTaskIds
                    val threatColor = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                    
                    val priorityTag = when (task.priority) {
                        "CRITICAL" -> "[ CRITICAL ] "
                        "MID" -> "[ MID ] "
                        "LOW" -> "[ LOW ] "
                        else -> ""
                    }
                    val nameText = "$priorityTag${task.name}".uppercase(Locale.getDefault())

                    val timeString = task.completedAt?.let {
                        val format = if (use24HourFormat) "HH:mm MMM d" else "h:mm a MMM d"
                        "[ COMPLETED: " + SimpleDateFormat(format, Locale.getDefault()).format(Date(it)).uppercase(Locale.getDefault()) + " ]"
                    } ?: "[ COMPLETED ]"

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, if (isSelected) MaterialTheme.colorScheme.primary else threatColor, androidx.compose.ui.graphics.RectangleShape)
                            .clickable(
                                enabled = isSelectionMode,
                                onClick = {
                                    if (isSelected) {
                                        selectedTaskIds = selectedTaskIds - task.id
                                    } else {
                                        selectedTaskIds = selectedTaskIds + task.id
                                    }
                                }
                            )
                            .padding(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        if (isSelectionMode) {
                            Text(
                                text = if (isSelected) "[ X ]" else "[   ]",
                                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                                color = if (isSelected) MaterialTheme.colorScheme.primary else threatColor,
                                modifier = Modifier.padding(end = 8.dp)
                            )
                        }
                        
                        Column(modifier = Modifier.weight(1f).padding(end = 8.dp)) {
                            Text(
                                text = nameText,
                                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                                color = threatColor
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = timeString,
                                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                                style = MaterialTheme.typography.bodySmall,
                                color = threatColor
                            )
                        }
                        if (!isSelectionMode) {
                            Text(
                                text = "[ REVERT ]",
                                fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                                color = MaterialTheme.colorScheme.secondary,
                                modifier = Modifier.clickable { onUnmarkComplete(task) }.padding(4.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}"""
    content = content.replace(target, replacement)
    
    # Also fix spacing on LazyColumn
    lc_target = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        )"""
    lc_replacement = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        )"""
    content = content.replace(lc_target, lc_replacement)
    
    with open("app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Not found target_start or end")
