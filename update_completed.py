import re

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'r') as f:
    content = f.read()

# Add imports
imports_to_add = """import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Checklist
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.material.ripple.rememberRipple
import androidx.compose.material.icons.outlined.RadioButtonUnchecked
import androidx.compose.material.icons.filled.CheckCircle
"""
content = content.replace("import androidx.compose.material.icons.Icons\n", "import androidx.compose.material.icons.Icons\n" + imports_to_add)

# Update the calling of CompletedRemindersScreen
old_call = """    if (showCompleted) {
        CompletedRemindersScreen(
            completedReminders = completedReminders,
            onUnmarkComplete = { task -> 
                viewModel.updateTimerTask(task.copy(isCompleted = false, completedAt = null)) 
            },
            onBack = { showCompleted = false }
        )
        return
    }"""

new_call = """    if (showCompleted) {
        CompletedRemindersScreen(
            completedReminders = completedReminders,
            onUnmarkComplete = { task -> 
                viewModel.updateTimerTask(task.copy(isCompleted = false, completedAt = null)) 
            },
            onDeleteTasks = { tasksToDelete ->
                tasksToDelete.forEach { viewModel.deleteTask(it) }
            },
            onBack = { showCompleted = false }
        )
        return
    }"""
content = content.replace(old_call, new_call)


# Replace CompletedRemindersScreen
old_completed_screen_pattern = r'@OptIn\(ExperimentalMaterial3Api::class\)\s*@Composable\s*fun CompletedRemindersScreen[\s\S]*'

new_completed_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CompletedRemindersScreen(
    completedReminders: List<TimerTask>,
    onUnmarkComplete: (TimerTask) -> Unit,
    onDeleteTasks: (List<TimerTask>) -> Unit,
    onBack: () -> Unit
) {
    var isSelectionMode by remember { mutableStateOf(false) }
    var selectedTaskIds by remember { mutableStateOf(setOf<String>()) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    if (isSelectionMode) {
                        Text("${selectedTaskIds.size} Selected")
                    } else {
                        Text("Completed Reminders") 
                    }
                },
                navigationIcon = {
                    if (isSelectionMode) {
                        IconButton(onClick = { 
                            isSelectionMode = false 
                            selectedTaskIds = setOf()
                        }) {
                            Icon(Icons.Default.Close, contentDescription = "Close Selection")
                        }
                    } else {
                        IconButton(onClick = onBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                        }
                    }
                },
                actions = {
                    if (isSelectionMode) {
                        if (selectedTaskIds.isNotEmpty()) {
                            IconButton(onClick = {
                                val tasksToDelete = completedReminders.filter { it.id in selectedTaskIds }
                                onDeleteTasks(tasksToDelete)
                                selectedTaskIds = setOf()
                                isSelectionMode = false
                            }) {
                                Icon(Icons.Default.Delete, contentDescription = "Delete Selected", tint = MaterialTheme.colorScheme.error)
                            }
                        }
                    } else {
                        if (completedReminders.isNotEmpty()) {
                            IconButton(onClick = { isSelectionMode = true }) {
                                Icon(Icons.Default.Checklist, contentDescription = "Select")
                            }
                        }
                    }
                }
            )
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (completedReminders.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text(
                            "No completed reminders",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            } else {
                items(completedReminders) { task ->
                    val isSelected = task.id in selectedTaskIds
                    
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
                                    "Completed: " + SimpleDateFormat("MMM d, h:mm a", Locale.getDefault()).format(Date(it))
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
                    }
                }
            }
        }
    }
}
"""

content = re.sub(old_completed_screen_pattern, new_completed_screen, content)

with open('app/src/main/java/com/example/ui/screens/QuickDeadlinesScreen.kt', 'w') as f:
    f.write(content)

