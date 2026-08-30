import re

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.foundation.gestures.detectVerticalDragGestures")
content = content.replace("androidx.compose.ui.input.pointer.pointerInput", "pointerInput")
content = content.replace("androidx.compose.foundation.gestures.detectVerticalDragGestures", "detectVerticalDragGestures")

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'w') as f:
    f.write(content)
