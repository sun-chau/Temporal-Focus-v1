import re

with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'r') as f:
    content = f.read()

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
                HorizontalDivider(modifier = Modifier.padding(bottom = 8.dp))
            }
"""
content = content.replace(target_col, replacement_col)
with open('app/src/main/java/com/example/ui/screens/CreateDailyScheduleScreen.kt', 'w') as f:
    f.write(content)
