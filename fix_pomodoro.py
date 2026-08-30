import re

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("import detectDragGestures", "import androidx.compose.foundation.gestures.detectDragGestures")

with open('app/src/main/java/com/example/ui/screens/PomodoroScreen.kt', 'w') as f:
    f.write(content)
