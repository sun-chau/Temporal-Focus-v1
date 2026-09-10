import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_grid = """fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 2.0).dp
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
            val minorOffset = offset + (30 * 2.0).dp
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

replacement_grid = """fun TimelineGrid(totalLanes: Int) {
    val totalMinutes = 24 * 60
    
    for (hour in 0..24) {
        val offset = (hour * 60 * 2.0).dp
        // Major tick line
        Box(
            modifier = Modifier
                .offset(x = offset)
                .width(1.dp)
                .fillMaxHeight()
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.25f))
        )
        // Minor tick line
        if (hour < 24) {
            val minorOffset = offset + (30 * 2.0).dp
            Box(
                modifier = Modifier
                    .offset(x = minorOffset)
                    .width(1.dp)
                    .fillMaxHeight()
                    .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f))
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
                .background(MaterialTheme.colorScheme.onSurface.copy(alpha = 0.25f))
        )
    }
}"""

content = content.replace(target_grid, replacement_grid)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Grid Patched")
