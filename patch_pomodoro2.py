import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.foundation.gestures.detectDragGestures" not in content:
    content = content.replace("import androidx.compose.foundation.gestures.detectTapGestures",
                              "import androidx.compose.foundation.gestures.detectTapGestures\nimport androidx.compose.foundation.gestures.detectDragGestures")

content = content.replace("androidx.compose.foundation.gestures.detectDragGestures", "detectDragGestures")
content = content.replace("PomodoroPhase.SHORT_BREAK", "PomodoroPhase.BREAK")

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
