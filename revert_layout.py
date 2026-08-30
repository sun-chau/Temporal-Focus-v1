import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                    Column(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {
                // Timeline Ruler
                androidx.compose.foundation.layout.Box(modifier = Modifier) {
                TimelineRuler(uiState.use24HourFormat)
                }
                   
                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                ) {"""

replacement = """                    Box(modifier = Modifier.fillMaxSize().horizontalScroll(pageScrollState)) {
                // Timeline Ruler
                androidx.compose.foundation.layout.Box(modifier = Modifier) {
                TimelineRuler(uiState.use24HourFormat)
                }
                   
                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                ) {"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
        f.write(content)
    print("Reverted successfully")
else:
    print("Target not found")
