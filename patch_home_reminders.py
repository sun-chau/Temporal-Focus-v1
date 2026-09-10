import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

imports_target = """import com.example.ui.components.UniversalTimePickerDialog
import java.util.Calendar"""
imports_replacement = """import com.example.ui.components.UniversalTimePickerDialog
import java.util.Calendar
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items"""
content = content.replace(imports_target, imports_replacement)

state_target = """    val focusRequester = remember { FocusRequester() }"""
state_replacement = """    val focusRequester = remember { FocusRequester() }
    
    val activeTasks by viewModel.activeTasks.collectAsState()
    val quickDeadlines = activeTasks.filter { it.labels == "Reminder" }.sortedBy { it.deadlineDateTime ?: Long.MAX_VALUE }"""
content = content.replace(state_target, state_replacement)

box_target = """        Box(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Home,
                    contentDescription = null,
                    modifier = Modifier.size(64.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "Coming Soon",
                    style = MaterialTheme.typography.titleLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }"""
box_replacement = """        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            if (quickDeadlines.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillParentMaxSize(), contentAlignment = Alignment.Center) {
                        Text(
                            text = "[ NO ACTIVE REMINDERS ]",
                            fontFamily = FontFamily.Monospace,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            } else {
                items(quickDeadlines, key = { it.id }) { task ->
                    com.example.ui.components.TerminalReminderRow(
                        task = task,
                        use24HourFormat = uiState.use24HourFormat,
                        onComplete = { viewModel.markTaskComplete(it) }
                    )
                }
            }
        }"""
content = content.replace(box_target, box_replacement)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
print("Patched HomeScreen list")
