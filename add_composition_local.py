import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

column_pattern = r'Column\(\s*modifier = Modifier\s*\.fillMaxSize\(\)\s*\.offset \{ androidx\.compose\.ui\.unit\.IntOffset\(overscrollOffset\.toInt\(\), 0\) \}\s*\.horizontalScroll\(horizontalScrollState\)\s*\) \{'
replacement = """androidx.compose.runtime.CompositionLocalProvider(androidx.compose.foundation.LocalOverscrollConfiguration provides null) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .offset { androidx.compose.ui.unit.IntOffset(overscrollOffset.toInt(), 0) }
                        .horizontalScroll(horizontalScrollState)
                ) {"""
content = re.sub(column_pattern, replacement, content)

# Now we added one open brace. We need to add one closing brace.
content = re.sub(r'\}\n\s*\}\n\s*\}\n\s*if \(reschedulingSchedule != null\)', '}\n    }\n    }\n    }\n    if (reschedulingSchedule != null)', content)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
