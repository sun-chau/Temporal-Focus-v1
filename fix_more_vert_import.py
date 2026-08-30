import re

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.material.icons.outlined.MoreVert" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.MoreVert", "import androidx.compose.material.icons.filled.MoreVert\nimport androidx.compose.material.icons.outlined.MoreVert")

with open("app/src/main/java/com/example/ui/screens/ChronometerScreen.kt", "w") as f:
    f.write(content)
