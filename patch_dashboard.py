import re

with open("app/src/main/java/com/example/ui/screens/TrackerDashboardScreen.kt", "r") as f:
    content = f.read()

# Add imports
if "import androidx.compose.foundation.ExperimentalFoundationApi" not in content:
    content = content.replace("import androidx.compose.foundation.border", "import androidx.compose.foundation.border\nimport androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable")

# Update OptIn
if "@OptIn(ExperimentalMaterial3Api::class)" in content and "@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)" not in content:
    content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun TrackerDashboardScreen", "@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)\n@Composable\nfun TrackerDashboardScreen")

# Add state variable
state_vars_old = """    var showSheet by remember { mutableStateOf(false) }
    var selectedTracker by remember { mutableStateOf<TrackerEntity?>(null) }"""
state_vars_new = """    var showSheet by remember { mutableStateOf(false) }
    var selectedTracker by remember { mutableStateOf<TrackerEntity?>(null) }
    var trackerToDelete by remember { mutableStateOf<TrackerEntity?>(null) }"""
content = content.replace(state_vars_old, state_vars_new)

# Update Clickable
clickable_old = """.clickable {
                                selectedTracker = tracker
                            }"""
clickable_new = """.combinedClickable(
                                onClick = { selectedTracker = tracker },
                                onLongClick = { trackerToDelete = tracker }
                            )"""
content = content.replace(clickable_old, clickable_new)

# Add Modal
modal = """
    trackerToDelete?.let { targetTracker ->
        AlertDialog(
            onDismissRequest = { trackerToDelete = null },
            title = { Text("Purge Tracker") },
            text = { 
                Text(
                    "Are you sure you want to permanently delete '[ ${targetTracker.title} ]'? All historical logs and schemas will be destroyed.",
                    color = MaterialTheme.colorScheme.error
                ) 
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.deleteTracker(targetTracker)
                        trackerToDelete = null
                    }
                ) { Text("DELETE", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = {
                TextButton(onClick = { trackerToDelete = null }) { Text("CANCEL") }
            }
        )
    }
}
@OptIn"""
content = re.sub(r'}\s*@OptIn', modal, content)

with open("app/src/main/java/com/example/ui/screens/TrackerDashboardScreen.kt", "w") as f:
    f.write(content)

