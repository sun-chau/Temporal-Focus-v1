import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

# Add editEntireSeries state
target_var = "    var occurrenceCount by remember { mutableStateOf(draft.occurrenceCount) }"
replacement_var = """    var occurrenceCount by remember { mutableStateOf(draft.occurrenceCount) }
    var editEntireSeries by remember { mutableStateOf(draft.editingId != null && draft.seriesId != null) }"""
content = content.replace(target_var, replacement_var)

# Change save call
target_save = "viewModel.saveAdvancedDailySchedule(finalDraft)"
replacement_save = "viewModel.saveAdvancedDailySchedule(finalDraft, editEntireSeries)"
content = content.replace(target_save, replacement_save)

# Add Switch
target_col = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {"""

replacement_col = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (draft.editingId != null && draft.seriesId != null) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Edit entire series", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    androidx.compose.material3.Switch(
                        checked = editEntireSeries,
                        onCheckedChange = { editEntireSeries = it }
                    )
                }
                Divider(modifier = Modifier.padding(bottom = 8.dp))
            }
"""
content = content.replace(target_col, replacement_col)

# Replace deleteDailyScheduleSync call ... wait, where is it called?
# Let's find it.
