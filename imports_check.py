import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

imports = [
    "import androidx.compose.ui.input.pointer.pointerInput",
    "import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress",
    "import androidx.compose.ui.hapticfeedback.HapticFeedbackType",
    "import androidx.compose.ui.platform.LocalHapticFeedback"
]

for imp in imports:
    if imp not in content:
        content = content.replace("import androidx.compose.ui.input.nestedscroll.nestedScroll", f"import androidx.compose.ui.input.nestedscroll.nestedScroll\n{imp}")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
