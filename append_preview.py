import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Add Preview import if not present
if "import androidx.compose.ui.tooling.preview.Preview" not in content:
    content = content.replace("package com.example.ui.screens", "package com.example.ui.screens\n\nimport androidx.compose.ui.tooling.preview.Preview")

preview_code = """

@Preview(showBackground = true, widthDp = 800, heightDp = 400)
@Composable
fun TimelineGravityPreview() {
    val mockTasks = com.example.data.MockDataGenerator.getMockTasks()
    val todayStart = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }.timeInMillis
    
    val endOfDay = todayStart + 24 * 60 * 60 * 1000L - 1L

    androidx.compose.foundation.layout.Box(modifier = Modifier.fillMaxSize().horizontalScroll(rememberScrollState())) {
        androidx.compose.foundation.layout.Box(modifier = Modifier) {
            TimelineRuler(use24HourFormat = true)
        }
        
        androidx.compose.foundation.layout.BoxWithConstraints(
            modifier = Modifier
                .fillMaxHeight()
                .width((24 * 60 * 1.5).dp)
        ) {
            val requiredLanes = mockTasks.maxOfOrNull { it.laneIndex + 1 } ?: 0
            
            TimelineGrid(totalLanes = maxOf(4, requiredLanes))
            
            mockTasks.forEach { schedule ->
                val actualStart = maxOf(todayStart, schedule.startTime)
                val actualEnd = minOf(endOfDay + 1, schedule.endTime)
                
                val startCal = Calendar.getInstance().apply { timeInMillis = actualStart }
                val startMinutes = if (schedule.startTime < todayStart) 0 else startCal.get(Calendar.HOUR_OF_DAY) * 60 + startCal.get(Calendar.MINUTE)
                
                val endMinutes = if (schedule.endTime > endOfDay) 24 * 60 else {
                    val endCal = Calendar.getInstance().apply { timeInMillis = actualEnd }
                    endCal.get(Calendar.HOUR_OF_DAY) * 60 + endCal.get(Calendar.MINUTE)
                }
                
                val durationMinutes = maxOf(10, endMinutes - startMinutes)
                
                val xOffset = (startMinutes * 1.5f).dp
                val yOffset = (schedule.laneIndex * 80 + 4).dp
                val width = (durationMinutes * 1.5f).dp
                
                val isBleedLeft = schedule.startTime < todayStart
                val isBleedRight = schedule.endTime > endOfDay
                
                ScheduleBlock(
                    isWarning = false,
                    modifier = Modifier.offset(x = xOffset, y = yOffset),
                    schedule = schedule,
                    coloredCategoriesEnabled = true,
                    use24HourFormat = true,
                    isBleedLeft = isBleedLeft,
                    isBleedRight = isBleedRight,
                    dragModifier = Modifier,
                    blockWidth = width,
                    onClick = {},
                    onStatusChange = {}
                )
            }
        }
    }
}
"""

if "fun TimelineGravityPreview(" not in content:
    content += preview_code

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
