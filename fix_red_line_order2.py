import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target_re = re.compile(r'(\s+)(}\s+)(}\s+)(}\s+if \(showDatePicker\))')

replacement = r"""\1    // Current Time Indicator
\1    if (page == actualTodayPage) {
\1        val cal = java.util.Calendar.getInstance()
\1        val currentMinutes = cal.get(java.util.Calendar.HOUR_OF_DAY) * 60 + cal.get(java.util.Calendar.MINUTE)
\1        val xOffset = (currentMinutes * 1.5f).dp
\1        
\1        androidx.compose.foundation.layout.Box(
\1            modifier = Modifier
\1                .offset(x = xOffset)
\1                .width(2.dp)
\1                .fillMaxHeight()
\1                .background(androidx.compose.ui.graphics.Color.Red)
\1                .onGloballyPositioned { coordinates ->
\1                    val windowBounds = coordinates.boundsInWindow()
\1                    isNowLineVisible = windowBounds.right > 0 && windowBounds.left < screenWidthPx
\1                }
\1        )
\1    }
\2\3\4"""

content = target_re.sub(replacement, content, count=1)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
print("Red line appended to bottom")
