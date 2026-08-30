with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() in [
        "import androidx.compose.ui.input.pointer.pointerInput",
        "import androidx.compose.foundation.gestures.detectHorizontalDragGestures",
        "import androidx.compose.ui.draw.drawBehind",
        "import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft",
        "import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight",
        "import androidx.compose.foundation.gestures.awaitEachGesture",
        "import androidx.compose.foundation.gestures.awaitFirstDown",
        "import androidx.compose.ui.input.pointer.positionChange"
    ]:
        continue
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.writelines(new_lines)
