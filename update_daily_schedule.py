import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# 1. Update TopAppBar title to show selected date
target_title = 'title = { Text("Daily Schedule") },'
replacement_title = """title = { 
                    val dateFormatted = java.text.SimpleDateFormat("MMMM d, yyyy", java.util.Locale.getDefault()).format(java.util.Date(selectedDateMillis))
                    Text(dateFormatted) 
                },"""
content = content.replace(target_title, replacement_title)

# 2. Remove "Midnight" texts
# We want to remove:
#                        Text(
#                            text = "Midnight",
#                            style = MaterialTheme.typography.labelSmall,
#                            color = MaterialTheme.colorScheme.outlineVariant,
#                            modifier = Modifier.align(Alignment.TopStart).padding(start = 4.dp, top = 4.dp)
#                        )
# And the other one with TopEnd.
content = re.sub(r'\s*Text\(\s*text = "Midnight",\s*style = MaterialTheme\.typography\.labelSmall,\s*color = MaterialTheme\.colorScheme\.outlineVariant,\s*modifier = Modifier\.align\(Alignment\.Top(Start|End)\)\.padding\(.*?\)\s*\)', '', content)

# 3. Update TimelineGrid thickness and opacity
# Find TimelineGrid
target_grid = """@Composable
fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    val totalWidth = (totalMinutes * 1.5).dp
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 1.5).dp
        // Major tick line
        Box(
            modifier = Modifier
                .offset(x = offset)
                .width(2.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.08f))
        )
        // Minor tick line
        if (hour < 24) {
            val minorOffset = offset + (30 * 1.5).dp
            Box(
                modifier = Modifier
                    .offset(x = minorOffset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.04f))
            )
        }
    }
    
    // Horizontal lanes dividers
    for (lane in 0..totalLanes) {
        val offset = (lane * 80).dp
        Box(
            modifier = Modifier
                .offset(y = offset)
                .fillMaxWidth()
                .height(1.dp)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f))
        )
    }
}"""

replacement_grid = """@Composable
fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 1.5).dp
        // Major tick line (thicker)
        Box(
            modifier = Modifier
                .offset(x = offset)
                .width(2.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.2f))
        )
        // Minor tick line (thinner)
        if (hour < 24) {
            val minorOffset = offset + (30 * 1.5).dp
            Box(
                modifier = Modifier
                    .offset(x = minorOffset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
            )
        }
    }
    
    // Horizontal lanes dividers
    for (lane in 0..totalLanes) {
        val offset = (lane * 80).dp
        Box(
            modifier = Modifier
                .offset(y = offset)
                .fillMaxWidth()
                .height(1.dp)
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
        )
    }
}"""
content = content.replace(target_grid, replacement_grid)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
