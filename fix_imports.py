with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'r') as f:
    content = f.read()

content = content.replace("import pointerInput\nimport detectVerticalDragGestures", "import androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.foundation.gestures.detectVerticalDragGestures")
content = content.replace("} { _, dragAmount ->", "} { change, dragAmount ->")

with open('app/src/main/java/com/example/ui/components/UniversalTimePickerDialog.kt', 'w') as f:
    f.write(content)
