import re
with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "r") as f:
    content = f.read()

# Fix onGloballyPositioned
content = content.replace(".androidx.compose.ui.layout.onGloballyPositioned", ".onGloballyPositioned")
content = content.replace("import androidx.compose.ui.layout.boundsInWindow", "import androidx.compose.ui.layout.boundsInWindow\nimport androidx.compose.ui.layout.onGloballyPositioned")

with open("app/src/main/java/com/example/ui/screens/DailyScheduleScreen.kt", "w") as f:
    f.write(content)
