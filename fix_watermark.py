import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

# 1. Update alpha in AnalyticsWatermark from 0.05f to 0.15f
# And add safe drawing padding
old_text_style = """    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 24.sp,
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.05f)
    )

    Column(modifier = Modifier.fillMaxSize().padding(32.dp)) {"""

new_text_style = """    val textStyle = androidx.compose.ui.text.TextStyle(
        fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
        fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
        fontSize = 24.sp,
        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.15f)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(top = 48.dp, bottom = 48.dp, start = 24.dp, end = 24.dp)
    ) {"""

content = content.replace(old_text_style, new_text_style)

# 2. Add Spacer before Main Timer Card to push the layout down
old_timer = """            // Main Timer Card
            Box("""
new_timer = """            Spacer(modifier = Modifier.height(64.dp))
            // Main Timer Card
            Box("""
content = content.replace(old_timer, new_timer)

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
