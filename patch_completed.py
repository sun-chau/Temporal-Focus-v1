import re

with open("app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt", "r") as f:
    content = f.read()

target = """                    val isSelected = task.id in selectedTaskIds
                    
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(
                            containerColor = if (isSelected) 
                                MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f) 
                            else 
                                MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                        )
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
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
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            if (isSelectionMode) {
                                Icon(
                                    imageVector = if (isSelected) Icons.Filled.CheckCircle else Icons.Outlined.RadioButtonUnchecked,
                                    contentDescription = "Select",
                                    tint = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.padding(end = 16.dp)
                                )
                            }
                            
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = task.name,
                                    style = MaterialTheme.typography.titleMedium,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                                )
                                val timeString = task.completedAt?.let {
                                    "Completed: " + SimpleDateFormat(if (use24HourFormat) "MMM d, HH:mm" else "MMM d, h:mm a", Locale.getDefault()).format(Date(it))
                                } ?: "Completed"
                                
                                Text(
                                    text = timeString,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f)
                                )
                            }
                            if (!isSelectionMode) {
                                IconButton(onClick = { onUnmarkComplete(task) }) {
                                    Icon(
                                        imageVector = Icons.Outlined.Refresh,
                                        contentDescription = "Unmark Complete",
                                        tint = MaterialTheme.colorScheme.secondary
                                    )
                                }
                            }
                        }
                    }"""

replacement = """                    val isSelected = task.id in selectedTaskIds
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
                    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt", "w") as f:
        f.write(content)
    print("Patched CompletedRemindersScreen")
else:
    print("Could not find CompletedRemindersScreen target")
