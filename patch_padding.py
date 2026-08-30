import re

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

target = """                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width((24 * 60 * 1.5).dp)
                ) {"""

replacement = """                // Canvas Body
                androidx.compose.foundation.layout.BoxWithConstraints(
                    modifier = Modifier
                        .fillMaxHeight()
                        .padding(top = 32.dp)
                        .width((24 * 60 * 1.5).dp)
                ) {"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
        f.write(content)
    print("Patched padding successfully")
else:
    print("Target not found")
